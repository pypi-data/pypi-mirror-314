"""Models for AWS SQS operations."""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from chainsaws.aws.shared.config import APIConfig


class SQSAPIConfig(APIConfig):
    """Configuration for SQS client."""



class SQSMessageAttributes(BaseModel):
    """SQS message attributes."""

    data_type: str = Field(..., alias="DataType")
    string_value: str = Field(..., alias="StringValue")


class SQSMessage(BaseModel):
    """SQS message structure."""

    queue_url: str
    message_body: str
    delay_seconds: int | None = None
    message_attributes: dict[str, SQSMessageAttributes] | None = None
    message_deduplication_id: str | None = None
    message_group_id: str | None = None


class SQSResponse(BaseModel):
    """Single message response."""

    message_id: str = Field(..., alias="MessageId")
    sequence_number: str | None = Field(None, alias="SequenceNumber")
    md5_of_message_body: str = Field(..., alias="MD5OfMessageBody")
    md5_of_message_attributes: str | None = Field(
        None, alias="MD5OfMessageAttributes")


class SQSBatchResultEntry(BaseModel):
    """Batch operation result entry."""

    id: str = Field(..., alias="Id")
    message_id: str = Field(..., alias="MessageId")
    md5_of_message_body: str = Field(..., alias="MD5OfMessageBody")


class SQSMessageBatchResponse(BaseModel):
    """Batch operation response."""

    successful: list[SQSBatchResultEntry] = Field(..., alias="Successful")
    failed: list[dict[str, Any]] = Field(..., alias="Failed")


class SQSReceivedMessage(BaseModel):
    """Received message structure."""

    message_id: str = Field(..., alias="MessageId")
    receipt_handle: str = Field(..., alias="ReceiptHandle")
    body: str = Field(..., alias="Body")
    md5_of_body: str = Field(..., alias="MD5OfBody")
    attributes: dict[str, str] | None = Field(None, alias="Attributes")
    message_attributes: dict[str, SQSMessageAttributes] | None = Field(
        None, alias="MessageAttributes")


class SQSReceiveMessageResponse(BaseModel):
    """Receive message operation response."""

    messages: list[SQSReceivedMessage] = Field(..., alias="Messages")


class SQSQueueAttributes(BaseModel):
    """Queue attributes."""

    delay_seconds: int = Field(0, alias="DelaySeconds")
    maximum_message_size: int = Field(..., alias="MaximumMessageSize")
    message_retention_period: int = Field(..., alias="MessageRetentionPeriod")
    visibility_timeout: int = Field(..., alias="VisibilityTimeout")
    created_timestamp: datetime = Field(..., alias="CreatedTimestamp")
    last_modified_timestamp: datetime = Field(...,
                                              alias="LastModifiedTimestamp")
    queue_arn: str = Field(..., alias="QueueArn")
    approximate_number_of_messages: int = Field(
        ..., alias="ApproximateNumberOfMessages")
    approximate_number_of_messages_not_visible: int = Field(
        ..., alias="ApproximateNumberOfMessagesNotVisible")
