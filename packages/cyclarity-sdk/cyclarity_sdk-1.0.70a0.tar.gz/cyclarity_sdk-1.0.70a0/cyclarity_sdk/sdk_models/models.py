from typing import Optional, Any
from pydantic import BaseModel
from enum import Enum
from cyclarity_sdk.sdk_models.types import ExecutionStatus  # noqa


''' Test step definitions'''


class ExecutionMetadata(BaseModel):
    execution_id: str
    agent_id: Optional[str] = None
    test_id: str
    step_id: Optional[str] = None
    step_name: Optional[str] = None
    step_version: Optional[str] = None
    iteration_index: Optional[str] = "0"


class ExecutionState(BaseModel):
    '''Data structure to be send via topic::execution-state'''
    execution_metadata: ExecutionMetadata
    percentage: int
    status: ExecutionStatus
    error_message: Optional[str] = ''


class RunningEnvType(str, Enum):
    IOT = "iot_device"
    BATCH = "batch"


'''Execution definitions'''


class PackageType(str, Enum):
    # Supported types for test step deployment
    PIP = "PIP"
    ZIP = "ZIP"


class MessageType(str, Enum):
    # Supported types for test step deployment
    LOG = "LOG"
    TEST_STATE = "TEST_STATE"
    EXECUTION_STATE = "EXECUTION_STATE"
    FINDING = "FINDING"
    TEST_ARTIFACT = "TEST_ARTIFACT"
    EXECUTION_OUTPUT = "EXECUTION_OUTPUT"


class CyclarityFile(BaseModel):
    '''CyclarityFile is a model for using files as in params for component'''
    file_name: str
    _path: str  # Private attribute

    def __init__(self, file_name: str, path: str):
        super().__init__(file_name=file_name)
        self._path = path  # Initialize the private _path attribute


class DynamicInput(BaseModel):
    '''DynamicInput let you get output dynamically during component runtime'''
    var_name: str
    _component_id: str
    _value: Any

    @property
    def value(self):
        return self._value
