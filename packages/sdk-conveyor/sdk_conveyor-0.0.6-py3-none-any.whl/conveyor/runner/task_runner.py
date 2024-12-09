import logging
from abc import ABC, abstractmethod
from typing import Optional

from google.protobuf.timestamp_pb2 import Timestamp

from conveyor import grpc
from conveyor.pb.datafy_pb2 import (
    ListBuildsRequest,
    ListEnvironmentsRequest,
    ListProjectsRequest,
    RunApplicationLogsRequest,
)
from conveyor.pb.datafy_pb2_grpc import EnvironmentServiceStub, ProjectServiceStub
from conveyor.project import get_project_api

from .task_state import TaskState

logger = logging.getLogger(__name__)


class CancelledException(BaseException):
    """Raised when the log streaming was interrupted."""


class TaskRunner(ABC):

    def start(self) -> None:
        """Runs your task."""
        with grpc.connect() as channel:
            self.start_run(channel)

    @abstractmethod
    def start_run(self, channel: grpc.Channel) -> TaskState:
        raise NotImplementedError


class ServiceHelpersMixin:

    @classmethod
    def find_project_id(cls, channel: grpc.Channel, project_name: str) -> str:
        project_service = ProjectServiceStub(channel)
        list_projects_response = project_service.ListProjects(
            ListProjectsRequest(name=project_name)
        )
        if not list_projects_response.projects:
            raise Exception(f"No project found to match the name: {project_name}.")
        if len(list_projects_response.projects) > 1:
            raise Exception(f"Multiple projects found to match the name: {project_name}.")
        return list_projects_response.projects[0].id

    @classmethod
    def find_environment_id(cls, channel: grpc.Channel, environment_name: str) -> str:
        environment_service = EnvironmentServiceStub(channel)
        list_environments_response = environment_service.ListEnvironments(
            ListEnvironmentsRequest(name=environment_name)
        )
        if not list_environments_response.environments:
            raise Exception(f"No environment found to match the name: {environment_name}.")
        if len(list_environments_response.environments) > 1:
            raise Exception(f"Multiple environments found to match the name: {environment_name}.")
        return list_environments_response.environments[0].id

    def find_build_id(self, channel: grpc.Channel, project_name: str) -> str:
        project_service = ProjectServiceStub(channel)
        builds_response = project_service.ListBuilds(
            ListBuildsRequest(project_id=self.find_project_id(channel, project_name))
        )
        builds = builds_response.builds
        if len(builds) == 0:
            raise Exception("No builds found")
        else:
            return builds[0].id

    def image(self, channel: grpc.Channel, *, project_name: str, build_id: str) -> str:
        project_api = get_project_api(channel, self.find_project_id(channel, project_name))
        return (
            f"{project_api.get_registry_url()}/datafy/data-plane/project/{project_name}:{build_id}"
        )


class ApplicationLogsMixin(ABC):
    @classmethod
    @abstractmethod
    def copy_logs_request_with_timestamp(
        cls,
        req: RunApplicationLogsRequest,
        latest_message_timestamp: Optional[Timestamp],
    ) -> RunApplicationLogsRequest:
        raise NotImplementedError

    @classmethod
    def tail_logs_with_retry(cls, channel: grpc.Channel, req: RunApplicationLogsRequest) -> int:
        tries = 0
        latest_message_timestamp: Optional[Timestamp] = None
        while True:
            environment_service = EnvironmentServiceStub(channel)
            try:
                logs_response = environment_service.GetApplicationLogs(
                    cls.copy_logs_request_with_timestamp(req, latest_message_timestamp)
                )
                for log in logs_response:
                    match log.WhichOneof("response"):
                        case "log_line":
                            latest_message_timestamp = log.log_line.timestamp
                            print(log.log_line.log)
                        case "heartbeat":
                            continue
                        case "exit_code":
                            logger.debug(f"Got exit code {log.exit_code}")
                            return log.exit_code
                return 0
            except Exception as e:
                logger.debug("Got exception while tailing logs, reconnecting")
                tries += 1
                if tries >= 10:
                    logger.debug("Tries ten times, stopping")
                    raise e
