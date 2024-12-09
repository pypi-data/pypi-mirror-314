from abc import ABC, abstractmethod
from datetime import datetime
from enum import IntEnum, Enum
import logging
from typing import Union, Optional

from cyclarity_sdk.sdk_models import ExecutionMetadata, MessageType
from pydantic import BaseModel


class LogLevel(IntEnum):
    CRITICAL = logging.CRITICAL
    FATAL = CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class LogChannelType(str, Enum):
    '''
    Channels are logical separators to the log screens in the UI.
    '''
    START = "START"  # will shown in the default log tab, setup logs which are step independent from execution runner
    END = "END"      # will shown in the default log tab, tear down logs which are step independent from execution runner
    TRACE = "TRACE"  # will shown in the execution TRACE tab.


class LogChannel(BaseModel):
    type: Optional[LogChannelType] = ''
    topic: Optional[str] = ''  # grouping logs by topic name for future use


class LogInformation(BaseModel):
    logger_name: str
    log_level: LogLevel
    time_stamp: datetime
    message: str


class ExecutionLog(BaseModel):
    '''All the needed attributes from logs to sent via mqtt'''
    metadata: ExecutionMetadata
    data: Union[LogInformation, dict]
    type: MessageType = MessageType.LOG
    channel: Optional[LogChannel] = None


class LogPublisher(ABC):
    @abstractmethod
    def publish_log(self, execution_log: ExecutionLog):
        raise NotImplementedError(
            f'publish_log was not defined for class {self.__class__.__name__}')  # noqa
