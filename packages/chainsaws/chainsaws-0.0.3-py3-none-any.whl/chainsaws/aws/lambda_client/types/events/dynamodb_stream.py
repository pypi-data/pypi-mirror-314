"""DynamoDB Stream event types for AWS Lambda."""


from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel


class AttributeValue(BaseModel):
    """DynamoDB attribute value representation.

    Args:
        B (str, optional): Binary data.
        BS (List[str], optional): Set of binary values.
        BOOL (bool, optional): Boolean value.
        L (List, optional): List of values.
        M (Dict, optional): Map of attribute names and values.
        N (str, optional): Number as string.
        NS (List[str], optional): Set of number strings.
        NULL (bool, optional): Null value indicator.
        S (str, optional): String value.
        SS (List[str], optional): Set of strings.

    Reference:
        https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_AttributeValue.html
    """
    B: Optional[str] = None
    BS: Optional[List[str]] = None
    BOOL: Optional[bool] = None
    L: Optional[List] = None
    M: Optional[Dict] = None
    N: Optional[str] = None
    NS: Optional[List[str]] = None
    NULL: bool | None = None
    S: Optional[str] = None
    SS: Optional[List[str]] = None


class StreamRecord(BaseModel):
    """Information about a DynamoDB Stream record.

    Args:
        ApproximateCreationDateTime (int, optional): The approximate time the record was created.
        Keys (Dict[str, AttributeValue], optional): The primary key attributes for the DynamoDB item.
        NewImage (Dict[str, AttributeValue], optional): The item's attributes after the change.
        OldImage (Dict[str, AttributeValue], optional): The item's attributes before the change.
        SequenceNumber (str, optional): A unique identifier for the stream record.
        SizeBytes (int, optional): The size of the stream record in bytes.
        StreamViewType (str, optional): Determines what information is written to the stream.

    Reference:
        https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_StreamRecord.html
    """
    ApproximateCreationDateTime: Optional[int] = None
    Keys: Optional[Dict[str, AttributeValue]] = None
    NewImage: Optional[Dict[str, AttributeValue]] = None
    OldImage: Optional[Dict[str, AttributeValue]] = None
    SequenceNumber: Optional[str] = None
    SizeBytes: Optional[int] = None
    StreamViewType: Optional[Literal[
        "KEYS_ONLY",
        "NEW_IMAGE",
        "OLD_IMAGE",
        "NEW_AND_OLD_IMAGES",
    ]] = None


class DynamodbRecord(BaseModel):
    """A DynamoDB Stream record.

    Args:
        awsRegion (str, optional): The AWS region where the change occurred.
        dynamodb (StreamRecord, optional): The stream record information.
        eventID (str, optional): A unique identifier for this event.
        eventName (str, optional): The type of change that occurred.
        eventSource (str, optional): The AWS service that generated this event.
        eventSourceARN (str, optional): The ARN of the DynamoDB stream.
        eventVersion (str, optional): The version number of the stream record format.
        userIdentity (Any, optional): Identity information for the user that made the change.

    Reference:
        https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_Record.html
    """
    awsRegion: Optional[str] = None
    dynamodb: Optional[StreamRecord] = None
    eventID: Optional[str] = None
    eventName: Optional[Literal["INSERT", "MODIFY", "REMOVE"]] = None
    eventSource: Optional[str] = None
    eventSourceARN: Optional[str] = None
    eventVersion: Optional[str] = None
    userIdentity: Optional[Any] = None


class DynamoDBStreamEvent(BaseModel):
    """Event sent to Lambda from a DynamoDB Stream.

    Args:
        Records (List[DynamodbRecord]): The list of DynamoDB Stream records.

    Reference:
        https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html
    """
    Records: List[DynamodbRecord]
