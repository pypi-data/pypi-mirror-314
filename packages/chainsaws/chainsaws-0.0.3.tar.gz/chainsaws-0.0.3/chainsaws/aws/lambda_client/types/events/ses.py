"""SES (Simple Email Service) event types for AWS Lambda."""


from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field


class SESMailHeader(BaseModel):
    """Email header information.

    Args:
        name (str): The header name.
        value (str): The header value.
    """
    name: str
    value: str


class SESMailCommonHeaders(BaseModel):
    """Common email headers.

    Args:
        returnPath (str): The return path for the email.
        from_ (Optional[List[str]]): The from address(es).
        date (str): The email date.
        to (Optional[List[str]]): The recipient address(es).
        cc (Optional[List[str]]): The CC address(es).
        bcc (Optional[List[str]]): The BCC address(es).
        sender (Optional[List[str]]): The sender address(es).
        replyTo (Optional[List[str]]): The reply-to address(es).
        messageId (str): The message ID.
        subject (str): The email subject.
    """
    returnPath: str
    from_: Optional[List[str]] = Field(None, alias="from")
    date: str
    to: Optional[List[str]] = None
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    sender: Optional[List[str]] = None
    replyTo: Optional[List[str]] = None
    messageId: str
    subject: str


class SESMail(BaseModel):
    """Information about the email message.

    Args:
        timestamp (str): When the message was received.
        source (str): The sender's email address.
        messageId (str): The message ID.
        destination (List[str]): The recipient addresses.
        headersTruncated (bool): Whether headers were truncated.
        headers (List[SESMailHeader]): The email headers.
        commonHeaders (SESMailCommonHeaders): Common email headers.
    """
    timestamp: str
    source: str
    messageId: str
    destination: List[str]
    headersTruncated: bool
    headers: List[SESMailHeader]
    commonHeaders: SESMailCommonHeaders


class SESReceiptStatus(BaseModel):
    """Status of an email verification check.

    Args:
        status (str): The verification status (PASS/FAIL/GRAY).
    """
    status: Literal["PASS", "FAIL", "GRAY"]


# SES Receipt Actions
class SESReceiptS3Action(BaseModel):
    """Action to save email to S3."""
    type: Literal["S3"]
    topicArn: Optional[str] = None
    bucketName: str
    objectKey: str


class SESReceiptSnsAction(BaseModel):
    """Action to publish to SNS."""
    type: Literal["SNS"]
    topicArn: str


class SESReceiptBounceAction(BaseModel):
    """Action to bounce the email."""
    type: Literal["Bounce"]
    topicArn: Optional[str] = None
    smtpReplyCode: str
    statusCode: str
    message: str
    sender: str


class SESReceiptLambdaAction(BaseModel):
    """Action to invoke a Lambda function."""
    type: Literal["Lambda"]
    topicArn: Optional[str] = None
    functionArn: str
    invocationType: str


class SESReceiptStopAction(BaseModel):
    """Action to stop processing rules."""
    type: Literal["Stop"]
    topicArn: Optional[str] = None


class SESReceiptWorkMailAction(BaseModel):
    """Action to send to WorkMail."""
    type: Literal["WorkMail"]
    topicArn: Optional[str] = None
    organizationArn: str


class SESReceipt(BaseModel):
    """Information about the email receipt and processing.

    Args:
        recipients (List[str]): The recipient addresses.
        timestamp (str): When the receipt was processed.
        spamVerdict (SESReceiptStatus): Spam check result.
        dkimVerdict (SESReceiptStatus): DKIM verification result.
        processingTimeMillis (int): Processing time in milliseconds.
        action (Union[...]): The action taken on the email.
        spfVerdict (SESReceiptStatus): SPF verification result.
        virusVerdict (SESReceiptStatus): Virus scan result.
        dmarcVerdict (SESReceiptStatus): DMARC verification result.
        dmarcPolicy (str): The DMARC policy (none/quarantine/reject).
    """
    recipients: List[str]
    timestamp: str
    spamVerdict: SESReceiptStatus
    dkimVerdict: SESReceiptStatus
    processingTimeMillis: int
    action: Union[
        SESReceiptS3Action,
        SESReceiptSnsAction,
        SESReceiptBounceAction,
        SESReceiptLambdaAction,
        SESReceiptStopAction,
        SESReceiptWorkMailAction,
        Dict[str, Any],  # For unknown action types
    ]
    spfVerdict: SESReceiptStatus
    virusVerdict: SESReceiptStatus
    dmarcVerdict: SESReceiptStatus
    dmarcPolicy: Literal["none", "quarantine", "reject"]


class SESMessage(BaseModel):
    """Complete information about an email message.

    Args:
        mail (SESMail): Information about the email.
        receipt (SESReceipt): Information about the receipt processing.

    Reference:
        https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-notifications-contents.html
    """
    mail: SESMail
    receipt: SESReceipt


class SESEventRecord(BaseModel):
    """Individual SES event record.

    Args:
        eventVersion (str): The event version.
        ses (SESMessage): The SES message information.
        eventSource (str): The AWS service that generated the event.
    """
    eventVersion: str
    ses: SESMessage
    eventSource: str


class SESEvent(BaseModel):
    """Event sent by SES to Lambda.

    Args:
        Records (List[SESEventRecord]): The list of SES records.

    Reference:
        https://docs.aws.amazon.com/lambda/latest/dg/services-ses.html
    """
    Records: List[SESEventRecord]
