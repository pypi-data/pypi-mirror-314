import logging
from typing import Any

from boto3.session import Session
from botocore.config import Config

from chainsaws.aws.firehose.firehose_models import DeliveryStreamRequest, FirehoseAPIConfig

logger = logging.getLogger(__name__)


class Firehose:
    """Low-level Kinesis Firehose client wrapper."""

    def __init__(
        self,
        boto3_session: Session,
        config: FirehoseAPIConfig | None = None,
    ) -> None:
        self.config = config or FirehoseAPIConfig()

        client_config = Config(
            region_name=self.config.region,
            retries={"max_attempts": self.config.max_retries},
            connect_timeout=self.config.timeout,
            read_timeout=self.config.timeout,
        )

        self.client = boto3_session.client(
            "firehose",
            config=client_config,
            region_name=self.config.region,
        )

    def create_delivery_stream(
        self,
        request: DeliveryStreamRequest,
    ) -> dict[str, Any]:
        """Create Kinesis Firehose delivery stream."""
        try:
            params = {
                "DeliveryStreamName": request.name,
                "S3DestinationConfiguration": {
                    "RoleARN": request.s3_config.role_arn,
                    "BucketARN": request.s3_config.bucket_arn,
                    "Prefix": f"{request.s3_config.prefix}/",
                    "ErrorOutputPrefix": f"{request.s3_config.error_prefix}/",
                },
            }

            if request.tags:
                params["Tags"] = [
                    {"Key": k, "Value": v}
                    for k, v in request.tags.items()
                ]

            return self.client.create_delivery_stream(**params)

        except Exception as e:
            logger.exception(f"Failed to create delivery stream: {e!s}")
            raise

    def put_record(
        self,
        stream_name: str,
        data: Any,
    ) -> dict[str, Any]:
        """Put record into delivery stream."""
        try:
            return self.client.put_record(
                DeliveryStreamName=stream_name,
                Record={"Data": data},
            )
        except Exception as ex:
            logger.exception(f"Failed to put record: {ex!s}")
            raise

    def put_record_batch(
        self,
        stream_name: str,
        records: list[Any],
    ) -> dict[str, Any]:
        """Put multiple records into delivery stream.

        Args:
            stream_name: Name of the delivery stream
            records: List of records to put. The length of records should be maximum 500.

        Returns:
            Dict containing response with FailedPutCount and RequestResponses

        Note:
            Maximum batch size is 500 records

        """
        try:
            if len(records) > 500:
                msg = "Maximum batch size is 500 records"
                raise ValueError(msg)

            return self.client.put_record_batch(
                DeliveryStreamName=stream_name,
                Records=[{"Data": record} for record in records],
            )
        except Exception as ex:
            logger.exception(f"Failed to put record batch: {ex!s}")
            raise
