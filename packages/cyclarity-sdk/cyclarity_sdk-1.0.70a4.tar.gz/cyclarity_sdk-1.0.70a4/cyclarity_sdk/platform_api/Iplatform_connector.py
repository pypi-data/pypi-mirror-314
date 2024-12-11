from abc import ABC, abstractmethod
from pydantic import BaseModel
from cyclarity_sdk.sdk_models import ExecutionState
from cyclarity_sdk.sdk_models import ExecutionMetadata   # noqa
from cyclarity_sdk.sdk_models.artifacts import TestArtifact  # noqa
from cyclarity_sdk.sdk_models.findings import Finding


class IPlatformConnectorApi(ABC):
    @abstractmethod
    def send_artifact(self, test_artifact: TestArtifact):
        raise NotImplementedError(
            f'send_artifact was not defined for class {self.__class__.__name__}')  # noqa

    @abstractmethod
    def send_finding(self, finding: Finding):
        raise NotImplementedError(
            f'send_finding was not defined for class {self.__class__.__name__}')  # noqa

    @abstractmethod
    def publish_runnable_result(self, result: BaseModel):
        raise NotImplementedError(
            f'publish_output was not defined for class {self.__class__.__name__}')  # noqa

    @abstractmethod
    def send_state(self, execution_state: ExecutionState):
        raise NotImplementedError(
            f'send_state was not defined for class {self.__class__.__name__}')  # noqa

    @abstractmethod
    def get_execution_meta_data(self) -> ExecutionMetadata:
        raise NotImplementedError(
            f'send_state was not defined for class {self.__class__.__name__}')  # noqa

    @abstractmethod
    def set_execution_meta_data(self, execution_metadata: ExecutionMetadata):
        raise NotImplementedError(
            f'send_state was not defined for class {self.__class__.__name__}')  # noqa

    @abstractmethod
    def get_output(self, execution_id: str, test_id: str, component_id: str, output_id=None):
        raise NotImplementedError(
            f'publish_output was not defined for class {self.__class__.__name__}')  # noqa

    @abstractmethod
    def send_data(self, execution_metadata: ExecutionMetadata, data):
        raise NotImplementedError(
            f'publish_output was not defined for class {self.__class__.__name__}')  # noqa
