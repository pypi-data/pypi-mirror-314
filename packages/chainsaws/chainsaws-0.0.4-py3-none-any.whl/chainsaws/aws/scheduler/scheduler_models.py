
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from chainsaws.aws.lambda_client.lambda_models import LambdaAPIConfig
from chainsaws.aws.shared.config import APIConfig


class SchedulerAPIConfig(APIConfig):
    """EventBridge Scheduler configuration."""

    max_retries: int = Field(
        3,
        description="Maximum number of API call retries",
        ge=0,
    )
    timeout: int = Field(
        30,
        description="Timeout for API calls in seconds",
        ge=1,
    )

    def to_lambda_config(self) -> LambdaAPIConfig:
        """Convert to LambdaAPIConfig."""
        return LambdaAPIConfig(
            credentials=self.credentials,
            region=self.region,
        )


class ScheduleRate(str, Enum):
    """Common schedule rates."""

    EVERY_MINUTE = "rate(1 minute)"
    EVERY_5_MINUTES = "rate(5 minutes)"
    EVERY_15_MINUTES = "rate(15 minutes)"
    EVERY_30_MINUTES = "rate(30 minutes)"
    EVERY_HOUR = "rate(1 hour)"
    EVERY_3_HOURS = "rate(3 hours)"
    EVERY_6_HOURS = "rate(6 hours)"
    EVERY_12_HOURS = "rate(12 hours)"
    EVERY_DAY = "rate(1 day)"


class ScheduleRequest(BaseModel):
    """Schedule creation request."""

    name: str | None = None
    group_name: str
    schedule_expression: str
    lambda_function_arn: str
    description: str | None = None
    enabled: bool = True
    input_data: dict[str, Any] | None = None
