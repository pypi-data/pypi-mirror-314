import logging
import traceback
from collections import defaultdict
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta
from types import TracebackType
from typing import Any

from croniter import croniter

logger = logging.getLogger(__name__)


@dataclass
class TaskGroup:
    """Task group information."""

    name: str
    cron: str
    tasks: set[Callable]


class GlobalExecutor:
    """Global thread pool executor manager."""

    def __init__(self, max_workers: int = 8) -> None:
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._futures: list[Future] = []
        self._task_groups: dict[str, TaskGroup] = {}
        self._group_futures: dict[str, list[Future]] = defaultdict(list)

    def submit(self, func: Callable, group_name: str = "default") -> Future:
        """Submit task to thread pool."""
        future = self._executor.submit(func)
        self._futures.append(future)
        self._group_futures[group_name].append(future)
        return future

    def join(self, group_name: str | None = None) -> None:
        """Wait for tasks to complete.

        Args:
            group_name: Optional group name to wait for specific group

        """
        futures = (
            self._group_futures.get(group_name, [])
            if group_name
            else self._futures
        )

        for future in futures:
            try:
                future.result()
            except Exception as e:
                logger.exception("Task execution failed: %s", str(e))
                raise

    def register_group(self, name: str, cron: str) -> None:
        """Register a new task group."""
        self._task_groups[name] = TaskGroup(name=name, cron=cron, tasks=set())

    def add_task_to_group(self, group_name: str, task: Callable) -> None:
        """Add task to group."""
        if group_name in self._task_groups:
            self._task_groups[group_name].tasks.add(task)


# Global executor instance
_executor = GlobalExecutor()


def join(group_name: str | None = None) -> None:
    """Global join function."""
    _executor.join(group_name)


class TaskRunner:
    """Task runner returned by ScheduledTask context manager."""

    def __init__(self, should_run: bool, group_name: str) -> None:
        self.should_run = should_run
        self.group_name = group_name

    def __call__(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """Execute the task if scheduled."""
        if not self.should_run:
            return

        try:
            # Add task to group for tracking
            _executor.add_task_to_group(self.group_name, func)

            # Wrap function with args and kwargs
            def task(): return func(*args, **kwargs)
            _executor.submit(task, self.group_name)

            logger.debug(
                "Scheduled task %s in group %s",
                func.__name__,
                self.group_name,
            )
        except Exception as e:
            logger.exception(
                "Failed to schedule task %s in group %s: %s",
                func.__name__,
                self.group_name,
                str(e),
            )
            raise


class ScheduledTask:
    """Cron-based task scheduler with context management."""

    def __init__(self, cron_expression: str, group_name: str | None = None) -> None:
        """Initialize scheduled task.

        Args:
            cron_expression: Cron expression for scheduling
            group_name: Optional group name for task grouping

        """
        self.cron_expression = cron_expression
        self.group_name = group_name or f"group_{id(self)}"
        _executor.register_group(self.group_name, cron_expression)

    def should_run(self) -> bool:
        """Check if task should run based on cron schedule."""
        now = datetime.now() + timedelta(seconds=5)
        iter = croniter(self.cron_expression, now)
        prev_schedule = iter.get_prev(datetime)

        return all(
            getattr(prev_schedule, unit) == getattr(now, unit)
            for unit in ["year", "month", "day", "hour", "minute"]
        )

    def __enter__(self) -> TaskRunner:
        """Enter context manager and return task runner."""
        return TaskRunner(self.should_run(), self.group_name)

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """Exit context manager and handle any errors."""
        if exc_type:
            traceback_str = "".join(
                traceback.format_exception(exc_type, exc_val, exc_tb),
            )
            logger.error(
                "Error in scheduled task group %s: %s\n%s",
                self.group_name,
                str(exc_val),
                traceback_str,
            )
            return True
        return False


class ScheduleCron:
    """Helper for creating cron expressions."""

    @staticmethod
    def daily(hour: int = 0, minute: int = 0) -> str:
        """Daily schedule at specific time."""
        return f"cron({minute} {hour} * * ? *)"

    @staticmethod
    def weekly(day_of_week: int, hour: int = 0, minute: int = 0) -> str:
        """Weekly schedule at specific time."""
        return f"cron({minute} {hour} ? * {day_of_week} *)"

    @staticmethod
    def monthly(day_of_month: int, hour: int = 0, minute: int = 0) -> str:
        """Monthly schedule at specific time."""
        return f"cron({minute} {hour} {day_of_month} * ? *)"


def generate_schedule_name(
    function_name: str,
    prefix: str | None = None,
) -> str:
    """Generate unique schedule name."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    name_parts = [part for part in [prefix, function_name, timestamp] if part]
    return "-".join(name_parts)
