from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from chainsaws.aws.shared.config import APIConfig


class LogLevel(str, Enum):
    """Log levels for CloudWatch Logs."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class RetentionDays(int, Enum):
    """Available retention periods for log groups."""

    ONE_DAY = 1
    THREE_DAYS = 3
    FIVE_DAYS = 5
    ONE_WEEK = 7
    TWO_WEEKS = 14
    ONE_MONTH = 30
    TWO_MONTHS = 60
    THREE_MONTHS = 90
    FOUR_MONTHS = 120
    FIVE_MONTHS = 150
    SIX_MONTHS = 180
    ONE_YEAR = 365
    FOREVER = 0


class CloudWatchAPIConfig(APIConfig):
    """Configuration for CloudWatch Logs API."""

    default_region: str = Field(
        "ap-northeast-2",
        description="Default AWS region",
    )
    max_retries: int = Field(
        3,
        description="Maximum number of API retry attempts",
    )


class LogGroupConfig(BaseModel):
    """Configuration for log group creation."""

    log_group_name: str = Field(..., description="Log group name")
    retention_days: RetentionDays | None = Field(
        None,
        description="Log retention period in days",
    )
    kms_key_id: str | None = Field(
        None,
        description="KMS key ID for encryption",
    )
    tags: dict[str, str] = Field(
        default_factory=dict,
        description="Tags for the log group",
    )


class LogStreamConfig(BaseModel):
    """Configuration for log stream creation."""

    log_group_name: str = Field(..., description="Log group name")
    log_stream_name: str = Field(..., description="Log stream name")


class LogEvent(BaseModel):
    """Single log event."""

    timestamp: datetime = Field(..., description="Event timestamp")
    message: str = Field(..., description="Log message")
    level: LogLevel | None = Field(
        LogLevel.INFO,
        description="Log level",
    )


class PutLogsConfig(BaseModel):
    """Configuration for putting log events."""

    log_group_name: str = Field(..., description="Log group name")
    log_stream_name: str = Field(..., description="Log stream name")
    events: list[LogEvent] = Field(..., description="Log events to put")
    sequence_token: str | None = Field(
        None,
        description="Sequence token for next batch",
    )


class GetLogsConfig(BaseModel):
    """Configuration for getting log events."""

    log_group_name: str = Field(..., description="Log group name")
    log_stream_name: str = Field(..., description="Log stream name")
    start_time: datetime | None = Field(
        None,
        description="Start time for log retrieval",
    )
    end_time: datetime | None = Field(
        None,
        description="End time for log retrieval",
    )
    limit: int | None = Field(
        None,
        description="Maximum number of log events to return",
    )
    next_token: str | None = Field(
        None,
        description="Token for next batch of logs",
    )


class FilterPattern(BaseModel):
    """Log filter pattern."""

    pattern: str = Field(..., description="Filter pattern")
    fields: list[str] = Field(
        default_factory=list,
        description="Fields to extract",
    )


class MetricFilter(BaseModel):
    """Metric filter configuration."""

    filter_name: str = Field(..., description="Filter name")
    log_group_name: str = Field(..., description="Log group name")
    filter_pattern: FilterPattern = Field(..., description="Filter pattern")
    metric_namespace: str = Field(...,
                                  description="CloudWatch metric namespace")
    metric_name: str = Field(..., description="CloudWatch metric name")
    metric_value: str = Field(..., description="Metric value")
    default_value: float | None = Field(
        None,
        description="Default value when pattern doesn't match",
    )


class SubscriptionFilter(BaseModel):
    """Subscription filter configuration."""

    filter_name: str = Field(..., description="Filter name")
    log_group_name: str = Field(..., description="Log group name")
    filter_pattern: FilterPattern = Field(..., description="Filter pattern")
    destination_arn: str = Field(
        ...,
        description="ARN of destination (Lambda, Kinesis, etc.)",
    )
    role_arn: str | None = Field(
        None,
        description="IAM role ARN for subscription",
    )
    distribution: str | None = Field(
        None,
        description="Distribution for the subscription",
    )


class QueryStatus(str, Enum):
    """Status of CloudWatch Logs Insights query."""

    SCHEDULED = "Scheduled"
    RUNNING = "Running"
    COMPLETE = "Complete"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    TIMEOUT = "Timeout"


class QuerySortBy(str, Enum):
    """Sort options for query results."""

    TIME_ASC = "timestamp asc"
    TIME_DESC = "timestamp desc"
    LOG_ASC = "@log asc"
    LOG_DESC = "@log desc"


class LogsInsightsQuery(BaseModel):
    """Configuration for CloudWatch Logs Insights query."""

    query_string: str = Field(..., description="Query string")
    log_group_names: list[str] = Field(..., description="Log groups to query")
    start_time: datetime = Field(..., description="Start time")
    end_time: datetime = Field(..., description="End time")
    limit: int | None = Field(None, description="Maximum results to return")
    sort_by: QuerySortBy | None = Field(
        QuerySortBy.TIME_DESC,
        description="Sort order for results",
    )


class QueryResult(BaseModel):
    """Result of a CloudWatch Logs Insights query."""

    query_id: str = Field(..., description="Query ID")
    status: QueryStatus = Field(..., description="Query status")
    statistics: dict[str, Any] = Field(
        default_factory=dict,
        description="Query statistics",
    )
    results: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Query results",
    )
