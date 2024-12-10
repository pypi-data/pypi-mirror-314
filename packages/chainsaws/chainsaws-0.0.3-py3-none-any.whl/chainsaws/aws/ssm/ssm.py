import logging

from chainsaws.aws.shared import session
from chainsaws.aws.ssm._ssm_internal import SSM
from chainsaws.aws.ssm.ssm_models import (
    AutomationExecution,
    AutomationExecutionConfig,
    CommandConfig,
    CommandInvocation,
    Parameter,
    ParameterConfig,
    SSMAPIConfig,
)

logger = logging.getLogger(__name__)


class SSMAPI:
    """High-level SSM API for AWS Systems Manager operations."""

    def __init__(self, config: SSMAPIConfig | None = None) -> None:
        """Initialize SSM client.

        Args:
            config: Optional SSM configuration

        """
        self.config = config or SSMAPIConfig()
        self.boto3_session = session.get_boto_session(
            self.config.credentials if self.config.credentials else None,
        )
        self.ssm = SSM(
            boto3_session=self.boto3_session,
            config=config,
        )

    def put_parameter(
        self,
        name: str,
        value: str,
        param_type: str = "String",
        description: str | None = None,
        tier: str = "Standard",
        tags: dict[str, str] | None = None,
        overwrite: bool = False,
    ) -> Parameter:
        """Create or update SSM parameter.

        Args:
            name: Parameter name
            value: Parameter value
            param_type: Parameter type (String, StringList, SecureString)
            description: Optional parameter description
            tier: Parameter tier (Standard, Advanced, Intelligent-Tiering)
            tags: Optional resource tags
            overwrite: Whether to overwrite existing parameter

        Returns:
            Parameter object containing details

        """
        config = ParameterConfig(
            name=name,
            value=value,
            type=param_type,
            description=description,
            tier=tier,
            tags=tags,
            overwrite=overwrite,
        )
        return self.ssm.put_parameter(config)

    def get_parameter(
        self,
        name: str,
        decrypt: bool = True,
    ) -> Parameter:
        """Get SSM parameter value.

        Args:
            name: Parameter name
            decrypt: Whether to decrypt SecureString parameters

        Returns:
            Parameter object containing value and metadata

        """
        return self.ssm.get_parameter(name, decrypt)

    def delete_parameter(self, name: str) -> None:
        """Delete SSM parameter.

        Args:
            name: Parameter name to delete

        """
        self.ssm.delete_parameter(name)

    def send_command(
        self,
        targets: list[dict[str, list[str]]],
        document_name: str,
        parameters: dict[str, list[str]] | None = None,
        comment: str | None = None,
        timeout_seconds: int = 3600,
    ) -> str:
        """Send SSM command to targets.

        Args:
            targets: List of target specifications
            document_name: SSM document to execute
            parameters: Optional command parameters
            comment: Optional command comment
            timeout_seconds: Command timeout in seconds

        Returns:
            Command ID for tracking execution

        """
        config = CommandConfig(
            targets=targets,
            document_name=document_name,
            parameters=parameters,
            comment=comment,
            timeout_seconds=timeout_seconds,
        )
        return self.ssm.send_command(config)

    def get_command_invocation(
        self,
        command_id: str,
        instance_id: str,
    ) -> CommandInvocation:
        """Get command execution details.

        Args:
            command_id: Command ID to check
            instance_id: Target instance ID

        Returns:
            Command invocation details including status and output

        """
        return self.ssm.get_command_invocation(command_id, instance_id)

    def start_automation(
        self,
        document_name: str,
        parameters: dict[str, list[str]] | None = None,
        target_parameter_name: str | None = None,
        targets: list[dict[str, list[str]]] | None = None,
        max_concurrency: str = "1",
        max_errors: str = "1",
    ) -> str:
        """Start SSM automation execution.

        Args:
            document_name: Automation document name
            parameters: Optional automation parameters
            target_parameter_name: Parameter name for rate control
            targets: Optional automation targets
            max_concurrency: Max concurrent executions
            max_errors: Max allowed errors

        Returns:
            Automation execution ID

        """
        config = AutomationExecutionConfig(
            document_name=document_name,
            parameters=parameters,
            target_parameter_name=target_parameter_name,
            targets=targets,
            max_concurrency=max_concurrency,
            max_errors=max_errors,
        )
        return self.ssm.start_automation(config)

    def get_automation_execution(
        self,
        execution_id: str,
    ) -> AutomationExecution:
        """Get automation execution details.

        Args:
            execution_id: Automation execution ID

        Returns:
            Automation execution details including status and output

        """
        return self.ssm.get_automation_execution(execution_id)
