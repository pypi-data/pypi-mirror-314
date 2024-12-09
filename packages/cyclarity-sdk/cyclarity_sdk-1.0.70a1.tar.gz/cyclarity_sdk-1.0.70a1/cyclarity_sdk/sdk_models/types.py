from enum import Enum

''' Test step definitions'''


class ExecutionStatus(str, Enum):
    TIMEOUT = "TIMEOUT"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED_SUCCESSFULLY = "COMPLETED"
    COMPLETED_WITH_ERROR = "FAILED"
    STOPPED = "STOPPED"


class ExecutionResult(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    NOT_EVALUATED = "NOT_EVALUATED"
