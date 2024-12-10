"""
Integrated Logging
Used to get logger object or initialize a class logger
"""

import logging
import os
import sys
from enum import Flag, auto
from logging import handlers as logging_handlers
from typing import Optional
from cyclarity_sdk.sdk_models import ExecutionMetadata
from cyclarity_sdk.platform_api.logger.models import LogPublisher


class LogHandlerType(Flag):
    SCREEN = auto()
    FILE = auto()
    MQTT = auto()
    REST = auto()
    IN_VEHICLE = SCREEN | FILE | MQTT
    CLI = FILE | SCREEN
    E2E = FILE | SCREEN | REST


class ClarityLoggerFactory:
    log_publisher: LogPublisher
    log_backup_count: int = 10
    execution_metadata: ExecutionMetadata
    log_files_dir: str = "/tmp/results/logs"
    is_initialized: bool = False
    streamer_pending_loggers: set[str] = set()

    @classmethod
    def init_logging(cls, log_publisher: LogPublisher, execution_metadata: ExecutionMetadata):  # noqa

        cls.log_publisher = log_publisher
        cls.execution_metadata = execution_metadata
        if not os.path.exists(cls.log_files_dir):
            os.makedirs(cls.log_files_dir)

        for logger_name in cls.streamer_pending_loggers:
            from cyclarity_sdk.platform_api.logger.clarity_streamer import ClarityStreamer  # noqa
            logger = logging.getLogger(logger_name)
            streamer_handler = ClarityStreamer(
                log_publisher=cls.log_publisher, execution_metadata=cls.execution_metadata)
            logger.addHandler(streamer_handler)

        cls.streamer_pending_loggers.clear()

        cls.is_initialized = True

    @classmethod
    def _get_handlers(cls, logger_name: str, handler_type: LogHandlerType):
        handlers = []
        if LogHandlerType.SCREEN in handler_type:
            cout_stream_handler = logging.StreamHandler(stream=sys.stdout)
            cout_stream_handler.setFormatter(logging.Formatter(
                '[%(asctime)s] {%(filename)s:%(lineno)d} %(name)s:%(levelname)s - %(message)s'))
            handlers.append(cout_stream_handler)

        if LogHandlerType.FILE in handler_type and logger_name is not None:
            if not os.path.exists(cls.log_files_dir):
                os.makedirs(cls.log_files_dir)
            log_file_path = os.path.join(
                cls.log_files_dir, f"{logger_name}.log")
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            file_handler = logging_handlers.RotatingFileHandler(
                backupCount=cls.log_backup_count,
                filename=log_file_path
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s] {%(filename)s:%(lineno)d}"
                    " %(name)s:%(levelname)s - %(message)s"
                )
            )
            handlers.append(file_handler)

        if cls.is_initialized:
            from cyclarity_sdk.platform_api.logger.clarity_streamer import ClarityStreamer  # noqa
            streamer_handler = ClarityStreamer(
                log_publisher=cls.log_publisher, execution_metadata=cls.execution_metadata)  # noqa
            handlers.append(streamer_handler)
        elif LogHandlerType.MQTT in handler_type:
            cls.streamer_pending_loggers.add(logger_name)

        return handlers

    @classmethod
    def get_logger(cls, name: Optional[str] = None, level: int = logging.INFO, handler_type: LogHandlerType = LogHandlerType.FILE, override=False):  # noqa
        """get the default logger object used across clarity-in-vehicle projects # noqa

            Args:
                name (str, optional): Logger name. Defaults to None.
                level (optional): Logging level. Defaults to INFO.
                handler_type (Enum, optional): Log handler(s) to register. Default to File.
                override(Bool, optional): if true replace current handlers in Logger

            Returns:
                logging.Logger: initialized logger object.
            """

        logger = logging.getLogger(name)

        if 0 != len(logger.handlers) and not override:  # means logger with this name was already initialized # noqa
            return logger

        # Remove all handlers associated with the logger

        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        if level is not None:
            logger.setLevel(level)

        handlers = cls._get_handlers(name, handler_type)

        for handler in handlers:
            logger.addHandler(handler)

        return logger
