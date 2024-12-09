import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from conveyor import grpc
from conveyor.auth import get_api_url
from conveyor.pb.application_runs_pb2 import (
    ApplicationRun,
    GetApplicationRunRequest,
    Phase,
)
from conveyor.pb.application_runs_pb2_grpc import ApplicationRunsServiceStub

logger = logging.getLogger(__name__)


class ApplicationRunResult:
    def __init__(
        self,
        *,
        failed: bool,
        task_name: str,
        environment_id: str,
        project_id: str,
        application_run_id: str,
    ):
        self.failed = failed
        self.task_name = (task_name,)
        self.environment_id = environment_id
        self.project_id = project_id
        self.application_run_id = application_run_id

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self

    def has_failed(self) -> bool:
        return self.failed

    def conveyor_url(self) -> str:
        return f"{get_api_url()}/projects/{self.project_id}/environments/{self.environment_id}/apprun/{self.application_run_id}/logs/default"


class TaskState(ABC):

    @abstractmethod
    def get_application_run_result(self, channel: grpc.Channel) -> ApplicationRunResult:
        raise NotImplementedError

    @abstractmethod
    def cancel(self, channel: grpc.Channel) -> bool:
        raise NotImplementedError

    @abstractmethod
    def has_finished(self, channel: grpc.Channel) -> bool:
        raise NotImplementedError

    @abstractmethod
    def has_failed(self, channel: grpc.Channel) -> bool:
        raise NotImplementedError


class ApplicationRunTaskState(TaskState, ABC):
    def __init__(
        self,
        *,
        task_name: str,
        application_run_id: str,
        environment_id: str,
        project_id: str,
    ):
        self.task_name = task_name
        self.application_run_id = application_run_id
        self.environment_id = environment_id
        self.project_id = project_id
        self.created = datetime.now(timezone.utc)

    def get_application_run_result(self, channel: grpc.Channel) -> ApplicationRunResult:
        return ApplicationRunResult(
            failed=self.has_failed(channel),
            task_name=self.task_name,
            environment_id=self.environment_id,
            project_id=self.project_id,
            application_run_id=self.application_run_id,
        )

    def has_finished(self, channel: grpc.Channel) -> bool:
        logger.debug(f"Checking if job with id: {self.application_run_id} has finished")
        try:
            app_run = self.get_application_run(channel)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
                if self.created + timedelta(seconds=60) < datetime.now(timezone.utc):
                    raise Exception("The job was not found after 1 minute")
                logger.debug(f"Job not found, we assume it has not started yet")
                return False
            raise rpc_error

        return self._is_finished_state(app_run)

    def has_failed(self, channel: grpc.Channel) -> bool:
        app_run = self.get_application_run(channel)
        return self._is_failed_state(app_run)

    @staticmethod
    def _is_failed_state(app_run: ApplicationRun) -> bool:
        return app_run.phase == Phase.Failed or app_run.phase == Phase.Canceled

    def get_application_run(self, channel: grpc.Channel) -> ApplicationRun:
        service = ApplicationRunsServiceStub(channel)
        return service.GetApplicationRunByApplicationId(
            GetApplicationRunRequest(application_id=self.application_run_id)
        )

    @staticmethod
    def _is_finished_state(app_run: ApplicationRun) -> bool:
        return (
            app_run.phase == Phase.Succeeded
            or app_run.phase == Phase.Canceled
            or app_run.phase == Phase.Failed
        )
