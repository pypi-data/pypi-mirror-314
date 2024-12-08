import json
import logging
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any

from cryptography.fernet import Fernet

from chainsaws.aws.lambda_client import LambdaAPI, LambdaAPIConfig
from chainsaws.aws.secrets_manager._secrets_manager_internal import SecretsManager
from chainsaws.aws.secrets_manager.secrets_manager_models import (
    BatchSecretOperation,
    RotationConfig,
    SecretBackupConfig,
    SecretConfig,
    SecretFilterConfig,
    SecretsManagerAPIConfig,
)
from chainsaws.aws.shared import shared

logger = logging.getLogger(__name__)


class SecretsManagerAPI:
    """High-level AWS Secrets Manager operations."""

    def __init__(self, config: SecretsManagerAPIConfig | None = None) -> None:
        self.config = config or SecretsManagerAPIConfig()
        self.boto3_session = shared.get_boto_session(
            self.config.credentials if self.config.credentials else None,
        )
        self.secrets = SecretsManager(self.boto3_session, config=self.config)
        self._executor = ThreadPoolExecutor()

    def create_secret(
        self,
        name: str,
        secret_value: str | bytes | dict,
        description: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a new secret."""
        config = SecretConfig(
            name=name,
            description=description,
            secret_string=secret_value if isinstance(
                secret_value, str | dict) else None,
            secret_binary=secret_value if isinstance(
                secret_value, bytes) else None,
            tags=tags,
        )
        return self.secrets.create_secret(config)

    def get_secret(
        self,
        secret_id: str,
        version_id: str | None = None,
        version_stage: str | None = None,
        binary: bool = False,
    ) -> str | dict | bytes:
        """Get secret value."""
        response = self.secrets.get_secret_value(
            secret_id=secret_id,
            version_id=version_id,
            version_stage=version_stage,
        )

        if binary and "SecretBinary" in response:
            return response["SecretBinary"]

        if "SecretString" in response:
            try:
                return json.loads(response["SecretString"])
            except json.JSONDecodeError:
                return response["SecretString"]

        msg = "No secret value found in response"
        raise ValueError(msg)

    def update_secret(
        self,
        secret_id: str,
        secret_value: str | bytes | dict,
        version_stages: list[str] | None = None,
    ) -> dict[str, Any]:
        """Update secret value."""
        return self.secrets.put_secret_value(
            secret_id=secret_id,
            secret_value=secret_value,
            version_stages=version_stages,
        )

    def delete_secret(
        self,
        secret_id: str,
        force: bool = False,
        recovery_window_days: int | None = 30,
    ) -> dict[str, Any]:
        """Delete a secret."""
        return self.secrets.delete_secret(
            secret_id=secret_id,
            force_delete=force,
            recovery_window_in_days=None if force else recovery_window_days,
        )

    def setup_rotation(
        self,
        secret_id: str,
        lambda_arn: str,
        rotation_days: int,
        rotation_rules: dict[str, Any] | None = None,
        lambda_config: LambdaAPIConfig | None = None,
    ) -> dict[str, Any]:
        """Setup automatic secret rotation.

        Args:
            secret_id: Secret ID or ARN
            lambda_arn: Lambda function ARN for rotation
            rotation_days: Number of days between rotations
            rotation_rules: Additional rotation rules

        Returns:
            Dict containing rotation configuration

        Raises:
            ValueError: If lambda_arn is invalid or Lambda function doesn't exist
            Exception: If rotation setup fails

        """
        lambda_client = LambdaAPI(config=lambda_config)
        try:
            # Verify function exists
            lambda_client.get_function(lambda_arn)
        except Exception as ex:
            msg = f"Invalid or non-existent Lambda function ARN: {
                lambda_arn}. Error: {ex}"
            raise ValueError(
                msg) from ex

        config = RotationConfig(
            rotation_lambda_arn=lambda_arn,
            rotation_rules=rotation_rules or {},
            automatically_after_days=rotation_days,
        )

        return self.secrets.rotate_secret(secret_id, config)

    def list_all_secrets(
        self,
        max_results: int | None = None,
    ) -> Iterator[dict[str, Any]]:
        """List all secrets with pagination."""
        paginator = self.secrets.client.get_paginator("list_secrets")

        params = {}
        if max_results:
            params["PaginationConfig"] = {"MaxItems": max_results}

        for page in paginator.paginate(**params):
            yield from page.get("SecretList", [])

    def get_secret_metadata(self, secret_id: str) -> dict[str, Any]:
        """Get secret metadata."""
        return self.secrets.describe_secret(secret_id)

    def get_secret_value_if_changed(
        self,
        secret_id: str,
        last_updated: datetime | None = None,
    ) -> str | dict | bytes | None:
        """Get secret value only if it has changed."""
        metadata = self.get_secret_metadata(secret_id)
        secret_updated = metadata.get("LastChangedDate")

        if not last_updated or (secret_updated and secret_updated > last_updated):
            return self.get_secret(secret_id)
        return None

    def batch_operation(self, batch_config: BatchSecretOperation) -> dict[str, Any]:
        """Execute batch operation on multiple secrets in parallel."""
        results = {
            "successful": [],
            "failed": [],
        }

        def execute_operation(secret_id: str) -> dict[str, Any]:
            try:
                if batch_config.operation == "delete":
                    self.delete_secret(secret_id, **batch_config.params)
                    return {"success": True, "secret_id": secret_id}
                if batch_config.operation == "rotate":
                    self.setup_rotation(secret_id, **batch_config.params)
                    return {"success": True, "secret_id": secret_id}
                if batch_config.operation == "update":
                    self.update_secret(secret_id, **batch_config.params)
                    return {"success": True, "secret_id": secret_id}
                return {
                    "success": False,
                    "secret_id": secret_id,
                    "error": f"Unknown operation: {batch_config.operation}",
                }
            except Exception as e:
                return {
                    "success": False,
                    "secret_id": secret_id,
                    "error": str(e),
                }

        with self._executor as executor:
            futures = [
                executor.submit(execute_operation, secret_id)
                for secret_id in batch_config.secret_ids
            ]

            # Collect results
            for future in futures:
                try:
                    result = future.result()
                    if result["success"]:
                        results["successful"].append(result["secret_id"])
                    else:
                        results["failed"].append({
                            "secret_id": result["secret_id"],
                            "error": result["error"],
                        })
                except Exception as e:
                    logger.exception(
                        f"Failed to get result from future: {e!s}")

        return results

    def backup_secrets(self, config: SecretBackupConfig) -> str:
        """Backup secrets to file in parallel."""
        backup_data = {
            "secrets": [],
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0",
            },
        }

        def backup_secret(secret_id: str) -> dict[str, Any] | None:
            try:
                value = self.get_secret(secret_id)
                metadata = self.get_secret_metadata(secret_id)
                return {
                    "id": secret_id,
                    "value": value,
                    "metadata": metadata,
                }
            except Exception as e:
                logger.exception(f"Failed to backup secret {secret_id}: {e!s}")
                return None

        # Execute backups in parallel
        with self._executor as executor:
            futures = [
                executor.submit(backup_secret, secret_id)
                for secret_id in config.secret_ids
            ]

            # Collect results
            for future in futures:
                try:
                    result = future.result()
                    if result:
                        backup_data["secrets"].append(result)
                except Exception as e:
                    logger.exception(f"Failed to get backup result: {e!s}")

        # Encrypt and save backup data
        backup_json = json.dumps(backup_data)

        if config.encrypt:
            key = config.encryption_key or Fernet.generate_key()
            f = Fernet(key)
            encrypted_data = f.encrypt(backup_json.encode())
            with open(config.backup_path, "wb") as f:
                f.write(encrypted_data)
            return key.decode() if config.encryption_key is None else None
        with open(config.backup_path, "w") as f:
            f.write(backup_json)
        return None

    def restore_secrets(
        self,
        backup_path: str,
        encryption_key: str | None = None,
    ) -> dict[str, Any]:
        """Restore secrets from backup."""
        try:
            if encryption_key:
                with open(backup_path, "rb") as f:
                    encrypted_data = f.read()
                f = Fernet(encryption_key.encode())
                backup_json = f.decrypt(encrypted_data).decode()
            else:
                with open(backup_path) as f:
                    backup_json = f.read()

            backup_data = json.loads(backup_json)
            results = {"restored": [], "failed": []}

            def restore_secret(secret: dict[str, Any]) -> dict[str, Any]:
                try:
                    self.create_secret(
                        name=secret["id"],
                        secret_value=secret["value"],
                        description=secret["metadata"].get("Description"),
                    )
                    return {"success": True, "secret_id": secret["id"]}
                except Exception as e:
                    return {
                        "success": False,
                        "secret_id": secret["id"],
                        "error": str(e),
                    }

            # Execute restores in parallel
            with self._executor as executor:
                futures = [
                    executor.submit(restore_secret, secret)
                    for secret in backup_data["secrets"]
                ]

                # Collect results
                for future in futures:
                    try:
                        result = future.result()
                        if result["success"]:
                            results["restored"].append(result["secret_id"])
                        else:
                            results["failed"].append({
                                "secret_id": result["secret_id"],
                                "error": result["error"],
                            })
                    except Exception as e:
                        logger.exception(
                            f"Failed to get restore result: {e!s}")

            return results

        except Exception as e:
            msg = f"Failed to restore secrets: {e}"
            raise Exception(msg) from e

    def filter_secrets(
        self,
        filter_config: SecretFilterConfig,
    ) -> Iterator[dict[str, Any]]:
        """Filter secrets based on criteria."""
        for secret in self.list_all_secrets():
            if filter_config.name_prefix and not secret["Name"].startswith(filter_config.name_prefix):
                continue

            if filter_config.tags:
                secret_tags = {t["Key"]: t["Value"]
                               for t in secret.get("Tags", [])}
                if not all(secret_tags.get(k) == v for k, v in filter_config.tags.items()):
                    continue

            if filter_config.created_after and secret["CreatedDate"] < filter_config.created_after:
                continue

            if filter_config.last_updated_after and secret.get("LastChangedDate", secret["CreatedDate"]) < filter_config.last_updated_after:
                continue

            yield secret
