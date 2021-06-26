import time
from io import TextIOWrapper


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


class ExecutionMonitor:
    _start_time: float
    _monitoring: Monitoring
    _operation: str

    def __init__(self, monitoring: Monitoring, operation: str) -> None:
        self._monitoring = monitoring
        self._operation = operation

    def __enter__(self):
        self._start_time = time.perf_counter()

    def __exit__(self, *_):
        elapsed_time = time.perf_counter() - self._start_time
        self._monitoring.report_operation_time(self._operation, elapsed_time)
