import grpc

from conveyor.pb.application_runs_pb2 import (
    ApplicationRun,
    GetApplicationRunRequest,
    Phase,
)
from conveyor.pb.datafy_pb2 import CancelApplicationRequest
from conveyor.pb.datafy_pb2_grpc import EnvironmentServiceStub

from .task_state import ApplicationRunTaskState


class ContainerTaskState(ApplicationRunTaskState):

    def __init__(
        self,
        *,
        task_name: str,
        application_run_id: str,
        environment_id: str,
        project_id: str,
        container_app_name: str,
    ):
        super().__init__(
            task_name=task_name,
            application_run_id=application_run_id,
            environment_id=environment_id,
            project_id=project_id,
        )
        self.container_app_name = container_app_name

    def cancel(self, channel: grpc.Channel) -> bool:
        environment_service = EnvironmentServiceStub(channel)
        environment_service.CancelApplication(
            CancelApplicationRequest(
                environment_id=self.environment_id,
                container_app_id=self.container_app_name,
            )
        )
        return self.get_application_run(channel).phase == Phase.Failed
