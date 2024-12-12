"""Amazon MQ event types for AWS Lambda."""


from typing import List, Optional, Set
from pydantic import BaseModel


class MQMessageDestination(BaseModel):
    """Destination information for an MQ message.

    Args:
        physicalname (str): The physical name of the destination (queue or topic).
    """
    physicalname: str


class MQMessage(BaseModel):
    """Individual message from Amazon MQ.

    Args:
        messageID (str): Unique identifier for the message.
        messageType (str): Type of the message.
        data (str): Base64-encoded message content.
        connectionId (str): ID of the connection that received the message.
        redelivered (Optional[bool]): Whether this message was previously delivered.
        persistent (Optional[bool]): Whether the message is persistent.
        destination (MQMessageDestination): Where the message was sent.
        timestamp (int): When the message was sent.
        brokerInTime (int): When the broker received the message.
        brokerOutTime (int): When the broker sent the message to Lambda.
    """
    messageID: str
    messageType: str
    data: str
    connectionId: str
    redelivered: Optional[bool] = None
    persistent: Optional[bool] = None
    destination: MQMessageDestination
    timestamp: int
    brokerInTime: int
    brokerOutTime: int


class MQEvent(BaseModel):
    """Event sent by Amazon MQ to Lambda.

    Args:
        eventSource (str): The AWS service that generated this event (e.g., "aws:mq").
        eventSourceArn (str): The ARN of the MQ broker.
        messages (Set[List[MQMessage]]): Messages from the broker, grouped by batch.

    Reference:
        https://docs.aws.amazon.com/lambda/latest/dg/with-mq.html
    """
    eventSource: str
    eventSourceArn: str
    messages: Set[List[MQMessage]]
