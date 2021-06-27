import time
from io import TextIOWrapper
from typing import ContextManager, Optional, Type


class Monitoring:
    MONITORING_LOG_PATH = '.data/monitoring.log'
    _file: TextIOWrapper

    def initialize(self):
        self._file = open(self.MONITORING_LOG_PATH, mode='a')

    def finalize(self):
        self._file.close()

    def report_operation_time(self, operation: str, time: float) -> None:
        self._file.write(f'{operation}, {time}\n')
        self._file.flush()

    def monitor_execution(self, operation: str):
        return ExecutionMonitor(self, operation)


class ExecutionMonitor(ContextManager):
    _start_time: float
    _monitoring: Monitoring
    _operation: str
    _aborted: bool

    def __init__(self, monitoring: Monitoring, operation: str) -> None:
        self._monitoring = monitoring
        self._operation = operation
        self._aborted = False

    def __enter__(self):
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, exec_type: Optional[Type[BaseException]], *_):
        if not self._aborted and exec_type is None:
            elapsed_time = time.perf_counter() - self._start_time
            self._monitoring.report_operation_time(self._operation, elapsed_time)

    def abort(self):
        self._aborted = True
