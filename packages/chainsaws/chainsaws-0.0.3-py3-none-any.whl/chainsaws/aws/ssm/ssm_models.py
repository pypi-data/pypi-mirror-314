from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from chainsaws.aws.shared.config import APIConfig


class SSMAPIConfig(APIConfig):
    """Configuration for SSM client."""


class ParameterConfig(BaseModel):
    """Configuration for SSM Parameter."""

    name: str = Field(..., description="Parameter name")
    value: str = Field(..., description="Parameter value")
    type: Literal["String", "StringList", "SecureString"] = Field(
        "String",
        description="Parameter type",
    )
    description: str | None = Field(
        None, description="Parameter description")
    tier: Literal["Standard", "Advanced", "Intelligent-Tiering"] = Field(
        "Standard",
        description="Parameter tier",
    )
    tags: dict[str, str] | None = Field(
        None,
        description="Resource tags",
    )
    overwrite: bool = Field(
        False,
        description="Whether to overwrite existing parameter",
    )


class Parameter(BaseModel):
    """SSM Parameter details."""

    name: str = Field(..., description="Parameter name")
    type: str = Field(..., description="Parameter type")
    value: str = Field(..., description="Parameter value")
    version: int = Field(..., description="Parameter version")
    last_modified_date: datetime = Field(...,
                                         description="Last modification date")
    arn: str = Field(..., description="Parameter ARN")
    data_type: str = Field(..., description="Parameter data type")


class CommandConfig(BaseModel):
    """Configuration for SSM Run Command."""

    targets: list[dict[str, list[str]]] = Field(
        ...,
        description="Target instances (by tags or instance IDs)",
    )
    document_name: str = Field(
        ...,
        description="SSM document name to execute",
    )
    parameters: dict[str, list[str]] | None = Field(
        None,
        description="Command parameters",
    )
    comment: str | None = Field(
        None,
        description="Command comment",
    )
    timeout_seconds: int = Field(
        3600,
        description="Command timeout in seconds",
        ge=60,
        le=172800,
    )


class CommandInvocation(BaseModel):
    """SSM Command invocation details."""

    command_id: str = Field(..., description="Command ID")
    instance_id: str = Field(..., description="Target instance ID")
    status: str = Field(..., description="Command status")
    status_details: str = Field(..., description="Detailed status")
    standard_output_content: str | None = Field(
        None,
        description="Command output",
    )
    standard_error_content: str | None = Field(
        None,
        description="Command error output",
    )


class AutomationExecutionConfig(BaseModel):
    """Configuration for SSM Automation execution."""

    document_name: str = Field(..., description="Automation document name")
    parameters: dict[str, list[str]] | None = Field(
        None,
        description="Automation parameters",
    )
    target_parameter_name: str | None = Field(
        None,
        description="Parameter name for rate control",
    )
    targets: list[dict[str, list[str]]] | None = Field(
        None,
        description="Automation targets",
    )
    max_concurrency: str = Field(
        "1",
        description="Max concurrent executions",
    )
    max_errors: str = Field(
        "1",
        description="Max allowed errors",
    )


class AutomationExecution(BaseModel):
    """SSM Automation execution details."""

    automation_execution_id: str = Field(..., description="Execution ID")
    document_name: str = Field(..., description="Document name")
    status: str = Field(..., description="Execution status")
    start_time: datetime = Field(..., description="Start time")
    end_time: datetime | None = Field(None, description="End time")
    outputs: dict | None = Field(None, description="Execution outputs")
    failure_message: str | None = Field(None, description="Failure message")


class SessionConfig(BaseModel):
    """Configuration for Session Manager."""

    target: str = Field(..., description="Target instance ID")
    document_name: str = Field(
        "AWS-StartInteractiveCommand",
        description="Session document name",
    )
    parameters: dict[str, list[str]] | None = Field(
        None,
        description="Session parameters",
    )
    reason: str | None = Field(None, description="Session start reason")


class SessionDetails(BaseModel):
    """Session Manager session details."""

    session_id: str = Field(..., description="Session ID")
    target: str = Field(..., description="Target instance ID")
    status: str = Field(..., description="Session status")
    reason: str | None = Field(None, description="Session reason")
    start_date: datetime = Field(..., description="Session start time")
    end_date: datetime | None = Field(None, description="Session end time")


class PatchBaselineConfig(BaseModel):
    """Configuration for Patch baseline."""

    name: str = Field(..., description="Baseline name")
    operating_system: str = Field(..., description="OS type")
    approval_rules: dict = Field(..., description="Patch approval rules")
    description: str | None = Field(
        None, description="Baseline description")
    tags: dict[str, str] | None = Field(None, description="Resource tags")


class PatchSummary(BaseModel):
    """Patch operation summary."""

    instance_id: str = Field(..., description="Instance ID")
    patch_group: str = Field(..., description="Patch group")
    baseline_id: str = Field(..., description="Patch baseline ID")
    status: str = Field(..., description="Patching status")
    operation_type: str = Field(..., description="Patch operation type")
    critical_missing: int = Field(0, description="Critical patches missing")
    security_missing: int = Field(0, description="Security patches missing")
    installed_count: int = Field(0, description="Installed patches count")
    installed_rejected: int = Field(0, description="Rejected patches count")


class StateConfig(BaseModel):
    """Configuration for State Manager association."""

    name: str = Field(..., description="Association name")
    document_name: str = Field(..., description="SSM document name")
    targets: list[dict[str, list[str]]
                  ] = Field(..., description="Association targets")
    schedule_expression: str = Field(..., description="Schedule expression")
    parameters: dict[str, list[str]] | None = Field(
        None,
        description="Association parameters",
    )
    automation_target_parameter_name: str | None = Field(
        None,
        description="Target parameter for automation",
    )


class StateAssociation(BaseModel):
    """State Manager association details."""

    association_id: str = Field(..., description="Association ID")
    name: str = Field(..., description="Association name")
    status: str = Field(..., description="Association status")
    last_execution_date: datetime | None = Field(
        None,
        description="Last execution date",
    )
    overview: dict = Field(..., description="Execution overview")


class InventoryConfig(BaseModel):
    """Configuration for Inventory collection."""

    instance_id: str = Field(..., description="Instance ID")
    type_name: str = Field(..., description="Inventory type")
    schema_version: str = Field(..., description="Schema version")
    capture_time: str = Field(..., description="Data capture time")
    content: dict = Field(..., description="Inventory content")


class MaintenanceWindowConfig(BaseModel):
    """Configuration for Maintenance Window."""

    name: str = Field(..., description="Window name")
    schedule: str = Field(..., description="CRON/Rate expression")
    duration: int = Field(..., description="Window duration in hours")
    cutoff: int = Field(..., description="Cutoff time in hours")
    allow_unregistered_targets: bool = Field(
        default=False,
        description="Allow unregistered targets",
    )
    tags: dict[str, str] | None = Field(None, description="Resource tags")


class MaintenanceWindow(BaseModel):
    """Maintenance Window details."""

    window_id: str = Field(..., description="Window ID")
    name: str = Field(..., description="Window name")
    status: str = Field(..., description="Window status")
    enabled: bool = Field(..., description="Window enabled state")
    schedule: str = Field(..., description="Schedule expression")
    duration: int = Field(..., description="Duration in hours")
    cutoff: int = Field(..., description="Cutoff in hours")
    next_execution_time: str | None = Field(
        None,
        description="Next scheduled execution",
    )


class MaintenanceTask(BaseModel):
    """Maintenance Window task."""

    window_id: str = Field(..., description="Window ID")
    task_id: str = Field(..., description="Task ID")
    task_type: str = Field(..., description="Task type")
    targets: list[dict] = Field(..., description="Task targets")
    task_arn: str = Field(..., description="Task ARN")
    service_role_arn: str = Field(..., description="Service role ARN")
    status: str = Field(..., description="Task status")
    priority: int = Field(..., description="Task priority")
    max_concurrency: str = Field(..., description="Max concurrent executions")
    max_errors: str = Field(..., description="Max allowed errors")
