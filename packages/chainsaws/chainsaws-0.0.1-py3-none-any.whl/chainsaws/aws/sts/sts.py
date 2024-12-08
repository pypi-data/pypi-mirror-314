import logging

from chainsaws.aws.shared import session
from chainsaws.aws.sts._sts_internal import STS
from chainsaws.aws.sts.sts_models import (
    AssumedRoleCredentials,
    AssumeRoleConfig,
    FederationTokenCredentials,
    GetCallerIdentityResponse,
    GetFederationTokenConfig,
    STSAPIConfig,
)

logger = logging.getLogger(__name__)


class STSAPI:
    """High-level STS API for AWS security token operations."""

    def __init__(self, config: STSAPIConfig | None = None) -> None:
        """Initialize STS client.

        Args:
            config: Optional STS configuration

        """
        self.config = config or STSAPIConfig()
        self.boto3_session = session.get_boto_session(
            self.config.credentials if self.config.credentials else None,
        )
        self.sts = STS(
            boto3_session=self.boto3_session,
            config=config,
        )

    def assume_role(
        self,
        role_arn: str,
        role_session_name: str,
        duration_seconds: int = 3600,
        external_id: str | None = None,
        policy: dict | None = None,
        tags: dict[str, str] | None = None,
    ) -> AssumedRoleCredentials:
        """Assume an IAM role.

        Args:
            role_arn: ARN of the role to assume
            role_session_name: Identifier for the assumed role session
            duration_seconds: Duration of the session (900-43200 seconds)
            external_id: Optional unique identifier for role assumption
            policy: Optional IAM policy to further restrict the assumed role
            tags: Optional session tags

        Returns:
            AssumedRoleCredentials containing temporary credentials

        """
        config = AssumeRoleConfig(
            role_arn=role_arn,
            role_session_name=role_session_name,
            duration_seconds=duration_seconds,
            external_id=external_id,
            policy=policy,
            tags=tags,
        )
        return self.sts.assume_role(config)

    def get_caller_identity(self) -> GetCallerIdentityResponse:
        """Get details about the IAM user or role making the call.

        Returns:
            GetCallerIdentityResponse containing caller details

        """
        return self.sts.get_caller_identity()

    def get_federation_token(
        self,
        name: str,
        duration_seconds: int = 43200,
        policy: dict | None = None,
        tags: dict[str, str] | None = None,
    ) -> FederationTokenCredentials:
        """Get temporary credentials for federated users.

        Args:
            name: Name of the federated user
            duration_seconds: Duration of the credentials (900-129600 seconds)
            policy: Optional IAM policy for federated user
            tags: Optional session tags

        Returns:
            FederationTokenCredentials containing temporary credentials

        """
        config = GetFederationTokenConfig(
            name=name,
            duration_seconds=duration_seconds,
            policy=policy,
            tags=tags,
        )
        return self.sts.get_federation_token(config)
