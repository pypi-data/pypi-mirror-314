
import logging
import threading
import queue
from cyclarity_sdk.platform_api.logger.models import ExecutionLog, LogInformation, LogPublisher, LogChannel


class ClarityStreamer(logging.Handler):
    def __init__(self, log_publisher: LogPublisher, execution_metadata):
        logging.Handler.__init__(self)
        self.log_publisher = log_publisher
        self.execution_metadata = execution_metadata

        # use queue and thread to avoid deadlocks
        self.log_queue = queue.Queue()

        self.running = True  # Flag to indicate if the worker thread should keep running
        self.worker_thread = threading.Thread(target=self._process_logs, daemon=True)
        self.worker_thread.start()

    def __del__(self):
        self.running = False  # Stop adding new logs
        self.worker_thread.join()  # Wait for the worker thread to finish

    def emit(self, record: logging.LogRecord) -> None:

        # Extract channel from the record if it exists
        channel_type = getattr(record, 'channel', None)

        if channel_type:
            log_channel = LogChannel(type=channel_type)
        else:
            log_channel = None

        log_information = LogInformation(logger_name=record.name, log_level=record.levelno,
                                         time_stamp=record.created, message=record.message)
        execution_log = ExecutionLog(metadata=self.execution_metadata, data=log_information, channel=log_channel)
        try:
            self.log_queue.put_nowait(execution_log)
        except queue.Full:
            print("Log queue is full, dropping log message")

    def _process_logs(self):
        while self.running or not self.log_queue.empty():  # Process until not running and queue is empty
            try:
                execution_log = self.log_queue.get(timeout=1)  # Wait for up to 1 second for a new log
                self.log_publisher.publish_log(execution_log)
                self.log_queue.task_done()
            except queue.Empty:  # Raised if the queue is empty after 1 second
                continue
            except Exception as e:
                print("Failed publishing log topic, exception: " + str(e))
