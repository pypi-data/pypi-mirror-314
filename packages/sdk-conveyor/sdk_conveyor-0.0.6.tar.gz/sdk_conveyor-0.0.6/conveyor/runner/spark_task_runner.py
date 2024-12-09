import logging
import signal
from functools import partial
from typing import Any, Mapping, Optional, Sequence, Union

from google.protobuf.timestamp_pb2 import Timestamp

from conveyor import grpc
from conveyor.pb.datafy_pb2 import (
    CancelApplicationRequest,
    DatafyProjectInfo,
    ListBuildsRequest,
    ListEnvironmentsRequest,
    ListProjectsRequest,
    RunApplicationLogsRequest,
    RunApplicationRequest,
    RunApplicationResponse,
    SparkSpec,
)
from conveyor.pb.datafy_pb2_grpc import EnvironmentServiceStub, ProjectServiceStub
from conveyor.secrets import SecretValue, render_env_vars_crd
from conveyor.types import InstanceLifecycle, InstanceType

from .spark_task_state import SparkTaskState
from .task_runner import (
    ApplicationLogsMixin,
    CancelledException,
    ServiceHelpersMixin,
    TaskRunner,
)
from .task_state import ApplicationRunResult

logger = logging.getLogger(__name__)


class SparkTaskRunner(TaskRunner, ApplicationLogsMixin, ServiceHelpersMixin):

    def __init__(
        self,
        *,
        task_name: str,
        project_name: str,
        environment_name: str,
        build_id: Optional[str] = None,
        application: str = "",
        application_args: Optional[Sequence[Any]] = None,
        conf: Optional[Mapping[str, str]] = None,
        env_vars: Optional[Mapping[str, Union[str, SecretValue]]] = None,
        iam_identity: Optional[str] = None,
        num_executors: Optional[int] = None,
        driver_instance_type: InstanceType = InstanceType.mx_micro,
        executor_instance_type: InstanceType = InstanceType.mx_small,
        instance_lifecycle: InstanceLifecycle = InstanceLifecycle.spot,
        s3_committer: Optional[str] = "file",
        abfs_committer: Optional[str] = "file",
        executor_disk_size: Optional[int] = None,
        mode: Optional[str] = "cluster-v2",
        aws_availability_zone: Optional[str] = None,
        verbose: bool = False,
    ):
        self.task_name = task_name
        self.project_name = project_name
        self._project_id: Optional[str] = None
        self.environment_name = environment_name
        self._environment_id: Optional[str] = None
        self.build_id = build_id
        self.application = application
        self.application_args = application_args or []
        self.conf = conf or {}
        self.env_vars = env_vars
        self.iam_identity = iam_identity
        self.num_executors = num_executors
        self.driver_instance_type = driver_instance_type
        self.executor_instance_type = executor_instance_type
        self.instance_lifecycle = instance_lifecycle
        self.s3_committer = s3_committer
        self.abfs_committer = abfs_committer
        self.executor_disk_size = executor_disk_size
        self.mode = mode
        self.aws_availability_zone = aws_availability_zone
        self.verbose = verbose

    def project_id(self, channel: grpc.Channel) -> str:
        if self._project_id is None:
            self._project_id = self.find_project_id(channel, self.project_name)
        return self._project_id

    def environment_id(self, channel: grpc.Channel) -> str:
        if self._environment_id is None:
            self._environment_id = self.find_environment_id(channel, self.environment_name)
        return self._environment_id

    def run(self) -> ApplicationRunResult:
        with grpc.connect() as channel:
            task_state = self.start_run(channel)

            logger.debug("Fetching the logs")
            req = RunApplicationLogsRequest(
                environment_id=self.environment_id(channel),
                environment_name=self.environment_name,
                project_id=self.project_id(channel),
                spark_app_id=task_state.spark_app_name,
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
                        req.spark_app_id,
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

    def start_run(self, channel: grpc.Channel) -> SparkTaskState:
        request = self.generate_request(channel)
        environment_service = EnvironmentServiceStub(channel)
        response: RunApplicationResponse = environment_service.RunApplication(request)
        return SparkTaskState(
            task_name=request.task_name,
            application_run_id=response.application_run_id,
            spark_app_name=response.spark_app_name,
            environment_id=request.environment_id,
            project_id=request.spark_spec.datafy_project_info.project_id,
        )

    def generate_request(self, channel: grpc.Channel) -> RunApplicationRequest:
        build_id = self.build_id
        if build_id is None:
            build_id = self.find_build_id(channel, self.project_name)

        spark_spec: SparkSpec = SparkSpec(
            image=self.image(channel, build_id=build_id, project_name=self.project_name),
            application=self.application,
            application_args=self.application_args,
            spark_config=self.conf,
            env_variables=render_env_vars_crd(self.env_vars),
            aws_role=self.iam_identity,
            azure_application_client_id=self.iam_identity,
            datafy_project_info=DatafyProjectInfo(
                project_id=self.project_id(channel),
                project_name=self.project_name,
                build_id=build_id,
                environment_id=self.environment_id(channel),
            ),
            mode=self.mode,
            aws_availability_zone=self.aws_availability_zone,
            scheduled_by="SDK",
            instance_life_cycle=InstanceLifecycle.Name(self.instance_lifecycle),
            driver_instance_type=InstanceType.Name(self.driver_instance_type).replace("_", "."),
            executor_instance_type=InstanceType.Name(self.executor_instance_type).replace("_", "."),
            executor_disk_size=self.executor_disk_size,
            number_of_executors=self.num_executors,
            s3_committer=self.s3_committer,
            abfs_committer=self.abfs_committer,
            verbose=self.verbose,
        )
        return RunApplicationRequest(
            environment_id=self.environment_id(channel),
            spark_spec=spark_spec,
            task_name=self.task_name,
        )

    @staticmethod
    def handle_interrupt_manual_run(
        channel: grpc.Channel, environment_id: str, spark_app_id: str, sig, frame
    ) -> None:
        logger.debug(f"Received interrupt, cancelling the application run with id {spark_app_id}")
        try:
            environment_service = EnvironmentServiceStub(channel)
            environment_service.CancelApplication(
                CancelApplicationRequest(environment_id=environment_id, spark_app_id=spark_app_id)
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
            spark_app_id=req.spark_app_id,
            start_from=latest_message_timestamp,
        )
