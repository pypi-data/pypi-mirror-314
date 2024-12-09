import logging
import signal
from functools import partial
from typing import Any, Collection, Mapping, Optional, Sequence, Union, cast

from google.protobuf.timestamp_pb2 import Timestamp

from conveyor import grpc
from conveyor.pb.datafy_pb2 import (
    CancelApplicationRequest,
    ContainerSpec,
    DatafyProjectInfo,
    ListBuildsRequest,
    ListEnvironmentsRequest,
    ListProjectsRequest,
    RunApplicationLogsRequest,
    RunApplicationRequest,
    RunApplicationResponse,
)
from conveyor.pb.datafy_pb2_grpc import EnvironmentServiceStub, ProjectServiceStub
from conveyor.secrets import SecretValue, render_env_vars_crd
from conveyor.types import InstanceLifecycle, InstanceType

from .container_task_state import ContainerTaskState
from .task_runner import (
    ApplicationLogsMixin,
    CancelledException,
    ServiceHelpersMixin,
    TaskRunner,
)
from .task_state import ApplicationRunResult

logger = logging.getLogger(__name__)


class ContainerTaskRunner(TaskRunner, ApplicationLogsMixin, ServiceHelpersMixin):

    def __init__(
        self,
        *,
        task_name: str,
        project_name: str,
        environment_name: str,
        build_id: Optional[str] = None,
        command: Optional[Sequence[str]] = None,
        args: Optional[Sequence[str]] = None,
        env_vars: Optional[Mapping[str, Union[str, SecretValue]]] = None,
        iam_identity: Optional[str] = None,
        instance_type: InstanceType = InstanceType.mx_micro,
        instance_lifecycle: InstanceLifecycle = InstanceLifecycle.spot,
        disk_size: Optional[int] = None,
        disk_mount_path: Optional[str] = None,
        show_output: bool = True,
    ):
        self.task_name = task_name
        self.project_name = project_name
        self._project_id: Optional[str] = None
        self.environment_name = environment_name
        self._environment_id: Optional[str] = None
        self.build_id = build_id
        self.command = command
        self.args = args
        self.env_vars = env_vars
        self.iam_identity = iam_identity
        self.instance_type = instance_type
        self.instance_lifecycle = instance_lifecycle
        self.disk_size = disk_size
        self.disk_mount_path = disk_mount_path
        self.show_output = show_output

    def project_id(self, channel: grpc.Channel) -> str:
        if self._project_id is None:
            self._project_id = self.find_project_id(channel, self.project_name)
        return cast(str, self._project_id)

    def environment_id(self, channel: grpc.Channel) -> str:
        if self._environment_id is None:
            self._environment_id = self.find_environment_id(channel, self.environment_name)
        return cast(str, self._environment_id)

    def run(self) -> ApplicationRunResult:
        with grpc.connect() as channel:
            task_state = self.start_run(channel)

            logger.debug("Fetching the logs")
            req = RunApplicationLogsRequest(
                environment_id=self.environment_id(channel),
                environment_name=self.environment_name,
                project_id=self.project_id(channel),
                container_app_id=task_state.container_app_name,
            )
            # This block makes sure we handle an interrupt while the job is running and cancel it
            # We throw and catch a cancelled exception since otherwise we would wait until the job is canceled on kubernetes
            # which by default takes up to 30s
            try:
                signal.signal(
                    signal.SIGINT,
                    partial(
                        self.handle_interrupt_manual_run,
                        channel,
                        req.environment_id,
                        req.container_app_id,
                    ),
                )
                exit_code = self.tail_logs_with_retry(channel, req)
            except CancelledException:
                return ApplicationRunResult(
                    failed=True,
                    task_name=task_state.task_name,
                    environment_id=req.environment_id,
                    project_id=req.project_id,
                    application_run_id=task_state.application_run_id,
                )
            return ApplicationRunResult(
                failed=exit_code != 0,
                task_name=task_state.task_name,
                environment_id=req.environment_id,
                project_id=req.project_id,
                application_run_id=task_state.application_run_id,
            )

    def start_run(self, channel: grpc.Channel) -> ContainerTaskState:
        request = self.generate_request(channel)
        environment_service = EnvironmentServiceStub(channel)
        response: RunApplicationResponse = environment_service.RunApplication(request)
        return ContainerTaskState(
            task_name=request.task_name,
            application_run_id=response.application_run_id,
            container_app_name=response.container_app_name,
            environment_id=request.environment_id,
            project_id=request.container_spec.datafy_project_info.project_id,
        )

    def generate_request(self, channel: grpc.Channel) -> RunApplicationRequest:
        build_id = self.build_id
        if build_id is None:
            build_id = self.find_build_id(channel, self.project_name)

        container_spec: ContainerSpec = ContainerSpec(
            datafy_project_info=DatafyProjectInfo(
                project_id=self.project_id(channel),
                project_name=self.project_name,
                build_id=build_id,
                environment_id=self.environment_id(channel),
            ),
            image=self.image(channel, build_id=build_id, project_name=self.project_name),
            command=self._ensure_string_sequence(self.command),
            args=self._ensure_string_sequence(self.args),
            env_variables=render_env_vars_crd(self.env_vars),
            instance_type=InstanceType.Name(self.instance_type).replace("_", "."),
            instance_life_cycle=InstanceLifecycle.Name(self.instance_lifecycle),
            aws_role=self.iam_identity,
            azure_application_client_id=self.iam_identity,
            scheduled_by="SDK",
            disk_size=self.disk_size,
            disk_mount_path=self.disk_mount_path,
        )
        return RunApplicationRequest(
            environment_id=self.environment_id(channel),
            container_spec=container_spec,
            task_name=self.task_name,
        )

    @staticmethod
    def _ensure_string_sequence(
        value: Optional[Union[Any, Collection[Any]]]
    ) -> Optional[Sequence[str]]:
        if value is None:
            return None
        if isinstance(value, str):
            return [value]
        if isinstance(value, Collection):
            return [str(element) for element in value]
        else:
            return [str(value)]

    @staticmethod
    def handle_interrupt_manual_run(
        channel: grpc.Channel, environment_id: str, container_app_id: str, sig, frame
    ) -> None:
        logger.debug(
            f"Received interrupt, cancelling the application run with id {container_app_id}"
        )
        try:
            environment_service = EnvironmentServiceStub(channel)
            environment_service.CancelApplication(
                CancelApplicationRequest(
                    environment_id=environment_id, container_app_id=container_app_id
                )
            )
        except grpc.RpcError as e:
            logger.debug(f"Encountered error while cancelling the application:\n{e}")
        raise CancelledException()

    @classmethod
    def copy_logs_request_with_timestamp(
        cls,
        req: RunApplicationLogsRequest,
        latest_message_timestamp: Optional[Timestamp],
    ) -> RunApplicationLogsRequest:
        return RunApplicationLogsRequest(
            environment_id=req.environment_id,
            environment_name=req.environment_name,
            project_id=req.project_id,
            container_app_id=req.container_app_id,
            start_from=latest_message_timestamp,
        )
