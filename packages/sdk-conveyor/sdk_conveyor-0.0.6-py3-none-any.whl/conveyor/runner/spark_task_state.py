import grpc

from conveyor.pb.application_runs_pb2 import (
    ApplicationRun,
    GetApplicationRunRequest,
    Phase,
)
from conveyor.pb.datafy_pb2 import CancelApplicationRequest
from conveyor.pb.datafy_pb2_grpc import EnvironmentServiceStub

from .task_state import ApplicationRunTaskState


class SparkTaskState(ApplicationRunTaskState):

    def __init__(
        self,
        *,
        task_name: str,
        application_run_id: str,
        environment_id: str,
        project_id: str,
        spark_app_name: str,
    ):
        super().__init__(
            task_name=task_name,
            application_run_id=application_run_id,
            environment_id=environment_id,
            project_id=project_id,
        )
        self.spark_app_name = spark_app_name

    def cancel(self, channel: grpc.Channel) -> bool:
        environment_service = EnvironmentServiceStub(channel)
        environment_service.CancelApplication(
            CancelApplicationRequest(
                environment_id=self.environment_id,
                spark_app_id=self.spark_app_name,
            )
        )
        return self.get_application_run(channel).phase == Phase.Failed
