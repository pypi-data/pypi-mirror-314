from datetime import datetime
from typing import Any, Optional, TypedDict

from pydantic import BaseModel, Field, field_validator

from chainsaws.aws.shared.config import APIConfig


class SecretsManagerAPIConfig(APIConfig):
    """Secrets Manager configuration."""

    max_retries: int = Field(
        3, description="Maximum number of API call retries")
    timeout: int = Field(30, description="Timeout for API calls in seconds")
    retry_modes: dict[str, Any] = Field(
        default_factory=lambda: {
            "max_attempts": 3,
            "mode": "adaptive",
        },
        description="Retry configuration",
    )


class SecretConfig(BaseModel):
    """Secret configuration."""

    name: str = Field(..., description="Secret name")
    description: str | None = Field(None, description="Secret description")
    secret_string: str | None = Field(
        None, description="Secret string value")
    secret_binary: bytes | None = Field(
        None, description="Secret binary value")
    tags: dict[str, str] | None = Field(None, description="Secret tags")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate secret name."""
        secret_name_length_limit = 512
        if not v or len(v) > secret_name_length_limit:
            msg = f"Secret name must be between 1 and {
                secret_name_length_limit} characters"
            raise ValueError(msg)
        return v


class RotationConfig(BaseModel):
    """Secret rotation configuration."""

    rotation_lambda_arn: str = Field(...,
                                     description="Lambda ARN for rotation")
    rotation_rules: dict[str, Any] = Field(
        ...,
        description="Rotation rules including schedule",
    )
    automatically_after_days: int | None = Field(
        None,
        description="Days after which to rotate automatically",
    )


class BatchSecretOperation(BaseModel):
    """Batch operation configuration."""

    secret_ids: list[str] = Field(..., description="List of secret IDs")
    operation: str = Field(..., description="Operation to perform")
    params: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Operation parameters",
    )


class SecretBackupConfig(BaseModel):
    """Secret backup configuration."""

    secret_ids: list[str] = Field(..., description="Secrets to backup")
    backup_path: str = Field(..., description="Backup file path")
    encrypt: bool = Field(True, description="Whether to encrypt backup")
    encryption_key: str | None = Field(None, description="Encryption key")


class SecretFilterConfig(BaseModel):
    """Secret filtering configuration."""

    name_prefix: str | None = Field(
        None, description="Filter by name prefix")
    tags: dict[str, str] | None = Field(None, description="Filter by tags")
    created_after: datetime | None = Field(
        None, description="Filter by creation date")
    last_updated_after: datetime | None = Field(
        None, description="Filter by update date")


class GetSecretResponse(TypedDict):
    """Response from creating a secret."""

    ARN: str
    Name: str
    VersionId: str
    SecretBinary: Optional[bytes] = None  # Exclusive OR
    SecretString: Optional[str] = None  # Exclusive OR
    VersionStages: list[str]
    CreatedDate: float  # unix timestamp
