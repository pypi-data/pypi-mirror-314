from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from chainsaws.aws.shared.config import APIConfig


class DatabaseEngine(str, Enum):
    """Supported database engines."""

    AURORA_MYSQL = "aurora-mysql"
    AURORA_POSTGRESQL = "aurora-postgresql"
    MYSQL = "mysql"
    POSTGRESQL = "postgres"
    MARIADB = "mariadb"
    ORACLE_SE = "oracle-se"        # Oracle Standard Edition
    ORACLE_SE1 = "oracle-se1"      # Oracle Standard Edition One
    ORACLE_SE2 = "oracle-se2"      # Oracle Standard Edition Two
    ORACLE_EE = "oracle-ee"        # Oracle Enterprise Edition
    SQLSERVER_SE = "sqlserver-se"  # SQL Server Standard Edition
    SQLSERVER_EX = "sqlserver-ex"  # SQL Server Express Edition
    SQLSERVER_WEB = "sqlserver-web"  # SQL Server Web Edition
    SQLSERVER_EE = "sqlserver-ee"  # SQL Server Enterprise Edition


class InstanceClass(str, Enum):
    """Available RDS instance classes."""

    # Burstable Performance Instances
    T3_MICRO = "db.t3.micro"
    T3_SMALL = "db.t3.small"
    T3_MEDIUM = "db.t3.medium"
    T3_LARGE = "db.t3.large"
    T3_XLARGE = "db.t3.xlarge"
    T3_2XLARGE = "db.t3.2xlarge"
    T4G_MICRO = "db.t4g.micro"
    T4G_SMALL = "db.t4g.small"
    T4G_MEDIUM = "db.t4g.medium"
    T4G_LARGE = "db.t4g.large"
    T4G_XLARGE = "db.t4g.xlarge"
    T4G_2XLARGE = "db.t4g.2xlarge"

    # General Purpose Instances
    M5_LARGE = "db.m5.large"
    M5_XLARGE = "db.m5.xlarge"
    M5_2XLARGE = "db.m5.2xlarge"
    M5_4XLARGE = "db.m5.4xlarge"
    M5_8XLARGE = "db.m5.8xlarge"
    M5_12XLARGE = "db.m5.12xlarge"
    M5_16XLARGE = "db.m5.16xlarge"
    M5_24XLARGE = "db.m5.24xlarge"
    M6I_LARGE = "db.m6i.large"
    M6I_XLARGE = "db.m6i.xlarge"
    M6I_2XLARGE = "db.m6i.2xlarge"
    M6I_4XLARGE = "db.m6i.4xlarge"
    M6I_8XLARGE = "db.m6i.8xlarge"
    M6I_12XLARGE = "db.m6i.12xlarge"
    M6I_16XLARGE = "db.m6i.16xlarge"
    M6I_24XLARGE = "db.m6i.24xlarge"
    M6I_32XLARGE = "db.m6i.32xlarge"

    # Memory Optimized Instances
    R5_LARGE = "db.r5.large"
    R5_XLARGE = "db.r5.xlarge"
    R5_2XLARGE = "db.r5.2xlarge"
    R5_4XLARGE = "db.r5.4xlarge"
    R5_8XLARGE = "db.r5.8xlarge"
    R5_12XLARGE = "db.r5.12xlarge"
    R5_16XLARGE = "db.r5.16xlarge"
    R5_24XLARGE = "db.r5.24xlarge"
    R6I_LARGE = "db.r6i.large"
    R6I_XLARGE = "db.r6i.xlarge"
    R6I_2XLARGE = "db.r6i.2xlarge"
    R6I_4XLARGE = "db.r6i.4xlarge"
    R6I_8XLARGE = "db.r6i.8xlarge"
    R6I_12XLARGE = "db.r6i.12xlarge"
    R6I_16XLARGE = "db.r6i.16xlarge"
    R6I_24XLARGE = "db.r6i.24xlarge"
    R6I_32XLARGE = "db.r6i.32xlarge"
    R7G_LARGE = "db.r7g.large"
    R7G_XLARGE = "db.r7g.xlarge"
    R7G_2XLARGE = "db.r7g.2xlarge"
    R7G_4XLARGE = "db.r7g.4xlarge"
    R7G_8XLARGE = "db.r7g.8xlarge"
    R7G_12XLARGE = "db.r7g.12xlarge"
    R7G_16XLARGE = "db.r7g.16xlarge"


class RDSAPIConfig(APIConfig):
    """Configuration for RDS API."""

    default_region: str = Field(
        "ap-northeast-2",
        description="Default AWS region for RDS operations",
    )
    max_retries: int = Field(
        3,
        description="Maximum number of API retry attempts",
    )


class DatabaseInstanceConfig(BaseModel):
    """Configuration for database instance creation."""

    instance_identifier: str = Field(...,
                                     description="Unique instance identifier")
    engine: DatabaseEngine = Field(..., description="Database engine")
    engine_version: str | None = Field(None, description="Engine version")
    instance_class: InstanceClass = Field(..., description="Instance class")
    allocated_storage: int = Field(
        20, description="Allocated storage in GB", ge=20)
    master_username: str = Field(..., description="Master user name")
    master_password: str = Field(..., description="Master user password")
    vpc_security_group_ids: list[str] = Field(
        ..., description="VPC security group IDs")
    availability_zone: str | None = Field(
        None, description="Preferred availability zone")
    db_subnet_group_name: str | None = Field(
        None, description="DB subnet group name")
    port: int | None = Field(
        None, description="Database port", ge=1150, le=65535)
    db_name: str | None = Field(None, description="Initial database name")
    backup_retention_period: int = Field(
        7, description="Backup retention period in days")
    tags: dict[str, str] = Field(
        default_factory=dict, description="Resource tags")


class DatabaseInstance(BaseModel):
    """Database instance details."""

    instance_identifier: str = Field(..., description="Instance identifier")
    engine: DatabaseEngine = Field(..., description="Database engine")
    status: str = Field(..., description="Instance status")
    endpoint: str | None = Field(None, description="Instance endpoint")
    port: int = Field(..., description="Database port")
    allocated_storage: int = Field(..., description="Allocated storage in GB")
    instance_class: InstanceClass = Field(..., description="Instance class")
    creation_time: datetime = Field(..., description="Instance creation time")
    publicly_accessible: bool = Field(
        ..., description="Public accessibility status")
    vpc_id: str | None = Field(None, description="VPC ID")
    availability_zone: str = Field(..., description="Availability zone")
    tags: dict[str, str] = Field(default_factory=dict, description="Tags")


class QueryConfig(BaseModel):
    """Configuration for database queries."""

    resource_arn: str = Field(..., description="RDS cluster/instance ARN")
    secret_arn: str = Field(...,
                            description="Secrets Manager ARN containing credentials")
    database: str = Field(..., description="Database name")
    schema: str | None = Field(None, description="Schema name")
    sql: str = Field(..., description="SQL query")
    parameters: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Query parameters",
    )
    transaction_id: str | None = Field(
        None,
        description="Transaction ID for transaction operations",
    )


class QueryResult(BaseModel):
    """Query execution result."""

    columns: list[str] = Field(..., description="Column names")
    rows: list[dict[str, Any]] = Field(..., description="Result rows")
    row_count: int = Field(..., description="Number of affected rows")
    generated_fields: list[Any] | None = Field(
        None,
        description="Auto-generated field values",
    )


class TransactionConfig(BaseModel):
    """Configuration for database transactions."""

    resource_arn: str = Field(..., description="RDS cluster/instance ARN")
    secret_arn: str = Field(...,
                            description="Secrets Manager ARN containing credentials")
    database: str = Field(..., description="Database name")
    schema: str | None = Field(None, description="Schema name")
    isolation_level: str | None = Field(
        None,
        description="Transaction isolation level",
    )


class SnapshotConfig(BaseModel):
    """Configuration for DB snapshots."""

    snapshot_identifier: str = Field(..., description="Snapshot identifier")
    instance_identifier: str = Field(...,
                                     description="Source instance identifier")
    tags: dict[str, str] = Field(
        default_factory=dict, description="Snapshot tags")


class DBSnapshot(BaseModel):
    """Database snapshot details."""

    snapshot_identifier: str = Field(..., description="Snapshot identifier")
    instance_identifier: str = Field(...,
                                     description="Source instance identifier")
    creation_time: datetime = Field(..., description="Snapshot creation time")
    status: str = Field(..., description="Snapshot status")
    engine: DatabaseEngine = Field(..., description="Database engine")
    allocated_storage: int = Field(..., description="Allocated storage in GB")
    availability_zone: str = Field(..., description="Availability zone")
    tags: dict[str, str] = Field(default_factory=dict, description="Tags")


class ParameterGroupConfig(BaseModel):
    """Configuration for DB parameter groups."""

    group_name: str = Field(..., description="Parameter group name")
    family: str = Field(..., description="Parameter group family")
    description: str = Field(..., description="Parameter group description")
    parameters: dict[str, str] = Field(
        default_factory=dict,
        description="Parameter name-value pairs",
    )
    tags: dict[str, str] = Field(default_factory=dict, description="Tags")


class MetricConfig(BaseModel):
    """Configuration for RDS metrics retrieval."""

    instance_identifier: str = Field(..., description="Instance identifier")
    metric_name: str = Field(..., description="CloudWatch metric name")
    start_time: datetime = Field(..., description="Start time for metrics")
    end_time: datetime = Field(..., description="End time for metrics")
    period: int = Field(60, description="Period in seconds")
    statistics: list[str] = Field(
        default_factory=lambda: ["Average"],
        description="Statistics to retrieve",
    )


class ReadReplicaConfig(BaseModel):
    """Configuration for read replicas."""

    source_instance_identifier: str = Field(
        ..., description="Source instance identifier")
    replica_identifier: str = Field(..., description="Replica identifier")
    availability_zone: str | None = Field(
        None, description="Target availability zone")
    instance_class: InstanceClass | None = Field(
        None, description="Replica instance class")
    port: int | None = Field(None, description="Database port")
    tags: dict[str, str] = Field(default_factory=dict, description="Tags")


class BatchExecuteStatementConfig(BaseModel):
    """Configuration for batch SQL statement execution."""

    resource_arn: str = Field(..., description="RDS cluster/instance ARN")
    secret_arn: str = Field(...,
                            description="Secrets Manager ARN containing credentials")
    database: str = Field(..., description="Database name")
    schema: str | None = Field(None, description="Schema name")
    sql: str = Field(..., description="SQL statement to execute")
    parameter_sets: list[list[dict[str, Any]]] = Field(
        ...,
        description="List of parameter sets for batch execution",
    )
    transaction_id: str | None = Field(
        None,
        description="Transaction ID for transaction operations",
    )


class BatchExecuteResult(BaseModel):
    """Result of batch statement execution."""

    update_results: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Results for update operations",
    )
    generated_fields: list[list[Any]] = Field(
        default_factory=list,
        description="Auto-generated field values for each statement",
    )


class ModifyInstanceConfig(BaseModel):
    """Configuration for modifying DB instance."""

    instance_identifier: str = Field(..., description="Instance identifier")
    instance_class: InstanceClass | None = Field(
        None, description="New instance class")
    allocated_storage: int | None = Field(
        None, description="New storage size in GB")
    master_password: str | None = Field(
        None, description="New master password")
    backup_retention_period: int | None = Field(
        None, description="Backup retention days")
    preferred_backup_window: str | None = Field(
        None, description="Preferred backup window")
    preferred_maintenance_window: str | None = Field(
        None, description="Preferred maintenance window")
    multi_az: bool | None = Field(
        None, description="Enable Multi-AZ deployment")
    auto_minor_version_upgrade: bool | None = Field(
        None, description="Auto minor version upgrade")
    apply_immediately: bool = Field(
        False, description="Apply changes immediately")


class PerformanceInsightConfig(BaseModel):
    """Configuration for Performance Insights."""

    instance_identifier: str = Field(..., description="Instance identifier")
    start_time: datetime = Field(..., description="Start time for metrics")
    end_time: datetime = Field(..., description="End time for metrics")
    metric_queries: list[dict[str, Any]
                         ] = Field(..., description="Performance metric queries")
    max_results: int | None = Field(
        None, description="Maximum number of results")


class LogType(str, Enum):
    """Available RDS log types."""

    POSTGRESQL = "postgresql"
    POSTGRESQL_UPGRADE = "postgresql.log"
    UPGRADE = "upgrade"
    ERROR = "error"
    GENERAL = "general"
    SLOW = "slowquery"
    AUDIT = "audit"


class EventCategory(str, Enum):
    """RDS event categories."""

    AVAILABILITY = "availability"
    BACKUP = "backup"
    CONFIGURATION_CHANGE = "configuration change"
    CREATION = "creation"
    DELETION = "deletion"
    FAILOVER = "failover"
    FAILURE = "failure"
    MAINTENANCE = "maintenance"
    NOTIFICATION = "notification"
    RECOVERY = "recovery"
    RESTORATION = "restoration"


class EventSubscriptionConfig(BaseModel):
    """Configuration for event subscription."""

    subscription_name: str = Field(..., description="Subscription name")
    sns_topic_arn: str = Field(..., description="SNS topic ARN")
    source_type: str | None = Field(
        None, description="Source type (e.g., db-instance)")
    event_categories: set[EventCategory] = Field(
        default_factory=set, description="Event categories")
    source_ids: list[str] = Field(
        default_factory=list, description="Source identifiers")
    enabled: bool = Field(True, description="Enable subscription")
    tags: dict[str, str] = Field(
        default_factory=dict, description="Subscription tags")


class BackupType(str, Enum):
    """Types of RDS backups."""

    AUTOMATED = "automated"
    MANUAL = "manual"
    SNAPSHOT = "snapshot"


class BackupConfig(BaseModel):
    """Configuration for database backup."""

    instance_identifier: str = Field(..., description="Instance identifier")
    backup_identifier: str = Field(..., description="Backup identifier")
    tags: dict[str, str] = Field(
        default_factory=dict, description="Backup tags")
    backup_type: BackupType = Field(
        BackupType.MANUAL,
        description="Type of backup",
    )
    copy_tags: bool = Field(
        True,
        description="Copy instance tags to backup",
    )


class RestoreConfig(BaseModel):
    """Configuration for database restore."""

    source_identifier: str = Field(..., description="Source backup identifier")
    target_identifier: str = Field(...,
                                   description="Target instance identifier")
    instance_class: InstanceClass | None = Field(
        None,
        description="Instance class for restored instance",
    )
    availability_zone: str | None = Field(
        None,
        description="Target availability zone",
    )
    port: int | None = Field(None, description="Database port")
    multi_az: bool = Field(False, description="Enable Multi-AZ deployment")
    vpc_security_group_ids: list[str] | None = Field(
        None,
        description="VPC security group IDs",
    )
    tags: dict[str, str] = Field(
        default_factory=dict, description="Instance tags")
    point_in_time: datetime | None = Field(
        None,
        description="Point-in-time to restore to",
    )


class BackupWindow(BaseModel):
    """Configuration for backup window."""

    instance_identifier: str = Field(..., description="Instance identifier")
    preferred_window: str = Field(
        ...,
        description="Preferred backup window (UTC)",
    )
    retention_period: int = Field(
        7,
        description="Backup retention period in days",
        ge=1,
        le=35,
    )
