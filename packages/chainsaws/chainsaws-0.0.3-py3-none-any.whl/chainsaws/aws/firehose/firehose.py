import io
import json
import logging
from collections.abc import Iterator
from time import sleep
from typing import Any

from chainsaws.aws.firehose._firehose_internal import Firehose
from chainsaws.aws.firehose._firehose_utils import parse_aws_jsons
from chainsaws.aws.firehose.firehose_models import (
    DeliveryStreamRequest,
    FirehoseAPIConfig,
    S3DestinationConfig,
)
from chainsaws.aws.iam import IAMAPI
from chainsaws.aws.s3 import S3API, S3APIConfig
from chainsaws.aws.shared import shared

logger = logging.getLogger(__name__)


class FirehoseAPI:
    """High-level Kinesis Firehose operations."""

    def __init__(
        self,
        delivery_stream_name: str,
        bucket_name: str,
        object_key_prefix: str | None = "logs/",
        error_prefix: str | None = "error",
        config: FirehoseAPIConfig | None = None,
        s3_config: S3APIConfig | None = None,
    ) -> None:
        self.config = config or FirehoseAPIConfig()
        self.delivery_stream_name = delivery_stream_name
        self.bucket_name = bucket_name
        self.object_key_prefix = object_key_prefix
        self.error_prefix = error_prefix

        self.boto3_session = shared.get_boto_session(
            self.config.credentials if self.config.credentials else None,
        )

        self.firehose = Firehose(
            boto3_session=self.boto3_session, config=self.config)
        self.s3_api = S3API(bucket_name=bucket_name, config=s3_config)
        self.iam = IAMAPI(self.boto3_session)

    def create_resource(self, max_retries: int = 3, retry_delay: int = 4) -> None:
        """Initialize Firehose delivery stream with S3 destination."""
        # Create S3 bucket
        self.s3_api.init_s3_bucket()

        role_name = f"RoleKinesisFirehose-{
            self.delivery_stream_name}-{self.bucket_name}"
        role_arn = self._create_role(role_name)
        self._put_role_policy(role_name)

        for attempt in range(max_retries):
            try:
                sleep(retry_delay)

                request = DeliveryStreamRequest(
                    name=self.delivery_stream_name,
                    s3_config=S3DestinationConfig(
                        role_arn=role_arn,
                        bucket_name=self.bucket_name,
                        prefix=self.object_key_prefix,
                        error_prefix=self.error_prefix,
                    ),
                )

                self.firehose.create_delivery_stream(request)
                break

            except Exception as ex:
                if attempt == max_retries - 1:
                    logger.exception(f"Failed to create delivery stream after {
                                 max_retries} attempts")
                    raise
                logger.warning(f"Attempt {attempt + 1} failed: {ex!s}")

    def put_record(self, data: str | bytes | dict | list) -> dict[str, Any]:
        """Put record into delivery stream."""
        if isinstance(data, dict | list):
            data = json.dumps(data)

        return self.firehose.put_record(
            self.delivery_stream_name,
            data,
        )

    def put_record_batch(
        self,
        records: list[str | bytes | dict | list],
        batch_size: int = 500,
        retry_failed: bool = True,
        max_retries: int = 3,
    ) -> dict[str, Any]:
        """Put multiple records into delivery stream with automatic batching.

        Args:
            records: List of records to put (strings, bytes, or JSON-serializable objects)
            batch_size: Maximum size of each batch (default: 500, max: 500)
            retry_failed: Whether to retry failed records (default: True)
            max_retries: Maximum number of retries for failed records (default: 3)

        Returns:
            Dict containing:
                - total_records: Total number of records processed
                - successful_records: Number of successfully delivered records
                - failed_records: List of failed records with their error messages
                - batch_responses: List of raw responses from each batch operation

        Example:
            >>> records = [{"id": i, "message": f"Test {i}"} for i in range(1000)]
            >>> result = firehose.put_record_batch(records)
            >>> print(f"Successfully delivered {result['successful_records']} records")

        """
        if batch_size > 500:
            msg = "Maximum batch size is 500 records"
            raise ValueError(msg)

        prepared_records = [
            json.dumps(record) if isinstance(record, dict | list) else record
            for record in records
        ]

        total_records = len(prepared_records)
        successful_records = 0
        failed_records = []
        batch_responses = []

        for attempt in range(max_retries):
            if not prepared_records:
                break

            current_batch_records = []

            for i in range(0, len(prepared_records), batch_size):
                batch = prepared_records[i:i + batch_size]

                try:
                    response = self.firehose.put_record_batch(
                        self.delivery_stream_name,
                        batch,
                    )
                    batch_responses.append(response)

                    # Process results
                    failed_count = response.get("FailedPutCount", 0)
                    if failed_count > 0:
                        # Collect failed records for retry
                        request_responses = response.get(
                            "RequestResponses", [])
                        for idx, resp in enumerate(request_responses):
                            if "ErrorCode" in resp:
                                failed_records.append({
                                    "record": batch[idx],
                                    "error": resp.get("ErrorMessage", "Unknown error"),
                                    "attempt": attempt + 1,
                                })
                                current_batch_records.append(batch[idx])
                            else:
                                successful_records += 1
                    else:
                        successful_records += len(batch)

                except Exception as ex:
                    logger.exception(f"Batch processing failed: {ex!s}")
                    current_batch_records.extend(batch)
                    failed_records.extend([{
                        "record": record,
                        "error": str(ex),
                        "attempt": attempt + 1,
                    } for record in batch])

            # Update records for next retry attempt
            if retry_failed and current_batch_records:
                prepared_records = current_batch_records
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Retrying {len(prepared_records)} failed records. "
                        f"Attempt {attempt + 2}/{max_retries}",
                    )
                    # Exponential backoff
                    sleep(2 ** attempt)
            else:
                break

        result = {
            "total_records": total_records,
            "successful_records": successful_records,
            "failed_records": failed_records,
            "batch_responses": batch_responses,
        }

        # Log final status
        if failed_records:
            logger.warning(
                f"Completed with {len(failed_records)} failed records out of {
                    total_records}",
            )
        else:
            logger.info(f"Successfully delivered all {total_records} records")

        return result

    def generate_objects(
        self,
        start_after: str | None = None,
        limit: int = 1000,
    ) -> Iterator[dict[str, Any]]:
        """Generate S3 objects in bucket with prefix.

        Args:
            start_after: Optional key to start after
            limit: Maximum number of objects to return per request

        Returns:
            Iterator[Dict[str, Any]]: Iterator of object metadata dictionaries

        """
        return self.s3_api.generate_object_keys(
            start_after=start_after,
            limit=limit,
        )

    def generate_log_json_list(
        self,
        key_start_after: str | None = None,
    ) -> Iterator[tuple[list, str]]:
        """Generate JSON logs from S3 objects.

        Args:
            key_start_after: Optional key to start after

        Returns:
            Iterator[tuple[list, str]]: Iterator of (parsed objects, object key) tuples

        """
        for content in self.generate_objects(key_start_after):
            key = content["Key"]
            buffer = io.BytesIO()

            # Download object to buffer
            with buffer:
                self.s3_api.upload_binary(key, buffer.getvalue())
                buffer.seek(0)
                content = buffer.read().decode("utf-8")
                objects = parse_aws_jsons(content)

                yield objects, key

    def _create_role(self, role_name: str) -> str:
        """Create IAM role for Firehose."""
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {
                    "Service": "firehose.amazonaws.com",
                },
                "Action": "sts:AssumeRole",
            }],
        }

        try:
            role = self.iam.create_role(
                role_name=role_name,
                trust_policy=trust_policy,
                description=f"Role for Kinesis Firehose({self.delivery_stream_name}) to access S3({
                    self.bucket_name})",
            )
            return role["Role"]["Arn"]
        except self.iam.client.exceptions.EntityAlreadyExistsException:
            role = self.iam.get_role(role_name)
            return role["Role"]["Arn"]
        except Exception as e:
            msg = "[FirehoseAPI.create_role] - failed to create role"
            raise Exception(
                msg) from e

    def _put_role_policy(self, role_name: str) -> None:
        """Put S3 access policy to IAM role."""
        policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": [
                    "s3:AbortMultipartUpload",
                    "s3:GetBucketLocation",
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:ListBucketMultipartUploads",
                    "s3:PutObject",
                ],
                "Resource": [
                    f"arn:aws:s3:::{self.bucket_name}",
                    f"arn:aws:s3:::{self.bucket_name}/*",
                ],
            }],
        }

        self.iam.put_role_policy(
            role_name=role_name,
            policy_name="S3AccessPolicy",
            policy_document=policy,
        )
