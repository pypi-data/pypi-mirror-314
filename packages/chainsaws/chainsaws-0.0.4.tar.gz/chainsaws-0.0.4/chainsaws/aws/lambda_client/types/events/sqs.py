"""SQS (Simple Queue Service) event types for AWS Lambda."""
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel


class SQSAttributes(BaseModel):
    """Message system attributes.

    Args:
        ApproximateReceiveCount (str, optional): Number of times message was received.
        SentTimestamp (str, optional): When the message was sent to the queue.
        SenderId (str, optional): AWS account number of the message sender.
        ApproximateFirstReceiveTimestamp (str, optional): When message was first received.
        SequenceNumber (str, optional): Sequence number (FIFO queues only).
        MessageGroupId (str, optional): Message group ID (FIFO queues only).
        MessageDeduplicationId (str, optional): Deduplication ID (FIFO queues only).
        DeadLetterQueueSourceArn (str, optional): ARN of source DLQ.
        AWSTraceHeader (str, optional): X-Ray tracing header.
    """
    ApproximateReceiveCount: str | None = None
    SentTimestamp: str | None = None
    SenderId: str | None = None
    ApproximateFirstReceiveTimestamp: str | None = None
    SequenceNumber: Optional[str] = None
    MessageGroupId: Optional[str] = None
    MessageDeduplicationId: Optional[str] = None
    DeadLetterQueueSourceArn: str | None = None
    AWSTraceHeader: str | None = None


class SQSMessageAttribute(BaseModel):
    """Custom message attribute.

    Args:
        binaryValue (str, optional): Binary attribute value.
        dataType (str): The attribute data type.
        stringValue (str): String attribute value.
        stringListValues (List[str]): List of string values.
        binaryListValues (List[str]): List of binary values.

    Reference:
        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_MessageAttributeValue.html
    """
    binaryValue: Optional[str] = None
    dataType: Literal["String", "Number", "Binary"]
    stringValue: str
    stringListValues: List[str]
    binaryListValues: List[str]


class SQSMessage(BaseModel):
    """Individual SQS message.

    Args:
        messageId (str, optional): Unique identifier for the message.
        receiptHandle (str, optional): Handle used to delete the message.
        body (str, optional): The message body.
        attributes (SQSAttributes, optional): System attributes.
        messageAttributes (Dict[str, SQSMessageAttribute], optional): Custom attributes.
        md5OfBody (str, optional): MD5 hash of the message body.
        md5OfMessageAttributes (str, optional): MD5 hash of message attributes.
        eventSource (str, optional): The AWS service that generated the event.
        eventSourceARN (str, optional): ARN of the SQS queue.
        awsRegion (str, optional): AWS region of the queue.

    Reference:
        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_Message.html
    """
    messageId: str | None = None
    receiptHandle: str | None = None
    body: str | None = None
    attributes: SQSAttributes | None = None
    messageAttributes: Dict[str, SQSMessageAttribute] | None = None
    md5OfBody: str | None = None
    md5OfMessageAttributes: str | None = None
    eventSource: str | None = None
    eventSourceARN: str | None = None
    awsRegion: str | None = None


class SQSEvent(BaseModel):
    """Event sent by SQS to Lambda.

    Args:
        Records (List[SQSMessage]): The list of SQS messages.

    Reference:
        https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html
    """
    Records: List[SQSMessage]
