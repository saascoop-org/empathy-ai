import json
import logging
from time import perf_counter
from typing import Callable, TypeVar

from empathy_engine.schemas import WorkflowStepMetric

T = TypeVar("T")

LOGGER_NAME = "empathy_engine"


def get_logger():
    return logging.getLogger(LOGGER_NAME)


def log_event(logger, event: str, **fields):
    safe_fields = {"event": event, **fields}
    logger.info(json.dumps(safe_fields, sort_keys=True))


class WorkflowTimer:

    def __init__(self):
        self.started_at = perf_counter()
        self.steps: list[WorkflowStepMetric] = []

    def measure(self, name: str, callback: Callable[[], T]) -> T:
        started_at = perf_counter()
        try:
            return callback()
        finally:
            duration_ms = (perf_counter() - started_at) * 1000
            self.steps.append(
                WorkflowStepMetric(
                    name=name,
                    duration_ms=round(duration_ms, 3),
                )
            )

    def total_duration_ms(self) -> float:
        return round((perf_counter() - self.started_at) * 1000, 3)
