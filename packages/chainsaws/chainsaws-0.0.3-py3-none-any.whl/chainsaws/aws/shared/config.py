
from pydantic import BaseModel, Field

from chainsaws.aws.shared.session import AWSCredentials


class APIConfig(BaseModel):
    """Configuration for AWS Configs.
    Used as a parent class for AWS service config classes.
    """

    credentials: AWSCredentials | None = Field(
        default=None,
        description="AWS credentials dictionary",
    )
    region: str | None = Field(
        default="ap-northeast-2",
        description="AWS region",
    )
