
from pydantic import BaseModel, Field

from chainsaws.aws.shared.config import APIConfig


class FirehoseAPIConfig(APIConfig):
    """Kinesis Firehose configuration."""

    max_retries: int = Field(
        3,
        description="Maximum number of API call retries",
    )
    timeout: int = Field(
        30,
        description="Timeout for API calls in seconds",
    )


class S3DestinationConfig(BaseModel):
    """S3 destination configuration."""

    role_arn: str = Field(..., description="IAM role ARN for Firehose")
    bucket_name: str = Field(..., description="S3 bucket name")
    prefix: str = Field(..., description="Object key prefix")
    error_prefix: str = Field(
        "error",
        description="Error output prefix",
    )

    @property
    def bucket_arn(self) -> str:
        return f"arn:aws:s3:::{self.bucket_name}"


class DeliveryStreamRequest(BaseModel):
    """Delivery stream creation request."""

    name: str
    s3_config: S3DestinationConfig
    tags: dict[str, str] | None = None
