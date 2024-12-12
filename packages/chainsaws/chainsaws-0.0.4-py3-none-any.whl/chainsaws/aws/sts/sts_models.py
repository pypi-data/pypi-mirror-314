
from pydantic import BaseModel, Field

from chainsaws.aws.shared.config import APIConfig


class STSAPIConfig(APIConfig):
    """Configuration for STS client."""


class AssumeRoleConfig(BaseModel):
    """Configuration for assuming an IAM role."""

    role_arn: str = Field(..., description="ARN of the role to assume")
    role_session_name: str = Field(...,
                                   description="Identifier for the assumed role session")
    duration_seconds: int = Field(
        3600,  # 1 hour
        description="Duration of the session in seconds (900-43200)",
        ge=900,
        le=43200,
    )
    external_id: str | None = Field(
        None,
        description="Unique identifier for role assumption",
    )
    policy: dict | None = Field(
        None,
        description="IAM policy to further restrict the assumed role",
    )
    tags: dict[str, str] | None = Field(
        None,
        description="Session tags to pass to the assumed role",
    )


class AssumedRoleCredentials(BaseModel):
    """Credentials for an assumed role."""

    access_key_id: str = Field(..., description="Temporary access key ID")
    secret_access_key: str = Field(...,
                                   description="Temporary secret access key")
    session_token: str = Field(..., description="Temporary session token")
    expiration: str = Field(...,
                            description="Timestamp when credentials expire")


class GetCallerIdentityResponse(BaseModel):
    """Response from get-caller-identity."""

    account: str = Field(..., description="AWS account ID")
    arn: str = Field(..., description="ARN of the caller")
    user_id: str = Field(..., description="Unique identifier of the caller")


class GetFederationTokenConfig(BaseModel):
    """Configuration for getting a federation token."""

    name: str = Field(..., description="Name of the federated user")
    duration_seconds: int = Field(
        43200,  # 12 hours
        description="Duration of the credentials in seconds (900-129600)",
        ge=900,
        le=129600,
    )
    policy: dict | None = Field(
        None,
        description="IAM policy for federated user",
    )
    tags: dict[str, str] | None = Field(
        None,
        description="Session tags for federated user",
    )


class FederationTokenCredentials(BaseModel):
    """Credentials for a federated user."""

    access_key_id: str = Field(..., description="Temporary access key ID")
    secret_access_key: str = Field(...,
                                   description="Temporary secret access key")
    session_token: str = Field(..., description="Temporary session token")
    expiration: str = Field(...,
                            description="Timestamp when credentials expire")
    federated_user_arn: str = Field(...,
                                    description="ARN of the federated user")
    federated_user_id: str = Field(..., description="ID of the federated user")
