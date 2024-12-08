from enum import Enum
from typing import Any

from pydantic import BaseModel, EmailStr, Field

from chainsaws.aws.shared.config import APIConfig


class EmailFormat(str, Enum):
    """Email content format."""

    TEXT = "Text"
    HTML = "Html"
    BOTH = "Both"


class EmailPriority(str, Enum):
    """Email priority level."""

    HIGH = "1"
    NORMAL = "3"
    LOW = "5"


class EmailContent(BaseModel):
    """Email content configuration."""

    subject: str = Field(..., description="Email subject")
    body_text: str | None = Field(None, description="Plain text body")
    body_html: str | None = Field(None, description="HTML body")
    charset: str = Field("UTF-8", description="Content character set")


class EmailAddress(BaseModel):
    """Email address with optional name."""

    email: EmailStr = Field(..., description="Email address")
    name: str | None = Field(None, description="Display name")

    def __str__(self) -> str:
        if self.name:
            return f"{self.name} <{self.email}>"
        return str(self.email)


class SESAPIConfig(APIConfig):
    """Configuration for SES API."""

    default_region: str = Field(
        "ap-northeast-2",
        description="Default AWS region",
    )
    default_sender: EmailAddress | None = Field(
        None,
        description="Default sender address",
    )
    default_format: EmailFormat = Field(
        EmailFormat.BOTH,
        description="Default email format",
    )


class SendEmailConfig(BaseModel):
    """Configuration for sending email."""

    sender: EmailAddress = Field(..., description="Sender address")
    recipients: list[EmailAddress] = Field(...,
                                           description="Recipient addresses")
    cc: list[EmailAddress] | None = Field(None, description="CC addresses")
    bcc: list[EmailAddress] | None = Field(
        None, description="BCC addresses")
    reply_to: list[EmailAddress] | None = Field(
        None, description="Reply-To addresses")
    content: EmailContent = Field(..., description="Email content")
    priority: EmailPriority = Field(
        EmailPriority.NORMAL,
        description="Email priority",
    )
    tags: dict[str, str] = Field(
        default_factory=dict,
        description="Email tags",
    )


class TemplateContent(BaseModel):
    """Email template content."""

    subject: str = Field(..., description="Template subject")
    text: str | None = Field(None, description="Text version template")
    html: str | None = Field(None, description="HTML version template")


class SendTemplateConfig(BaseModel):
    """Configuration for sending templated email."""

    template_name: str = Field(..., description="Template name")
    sender: EmailAddress = Field(..., description="Sender address")
    recipients: list[EmailAddress] = Field(...,
                                           description="Recipient addresses")
    template_data: dict[str,
                        Any] = Field(..., description="Template variables")
    cc: list[EmailAddress] | None = Field(None, description="CC addresses")
    bcc: list[EmailAddress] | None = Field(
        None, description="BCC addresses")
    tags: dict[str, str] = Field(
        default_factory=dict,
        description="Email tags",
    )


class EmailQuota(BaseModel):
    """SES sending quota information."""

    max_24_hour_send: int = Field(..., description="Max sends per 24 hours")
    max_send_rate: float = Field(..., description="Max send rate per second")
    sent_last_24_hours: int = Field(..., description="Sent in last 24 hours")


class BulkEmailRecipient(BaseModel):
    """Recipient for bulk email sending."""

    email: EmailAddress = Field(..., description="Recipient email address")
    template_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Template data for this recipient",
    )
    tags: dict[str, str] = Field(
        default_factory=dict,
        description="Tags for this recipient",
    )


class BulkEmailConfig(BaseModel):
    """Configuration for bulk email sending."""

    sender: EmailAddress = Field(..., description="Sender address")
    recipients: list[BulkEmailRecipient] = Field(
        ..., description="Recipients list")
    template_name: str | None = Field(
        None, description="Template name if using template")
    content: EmailContent | None = Field(
        None, description="Content if not using template")
    batch_size: int = Field(50, description="Number of emails per batch")
    max_workers: int | None = Field(
        None, description="Maximum number of worker threads")
    format: EmailFormat | None = Field(
        None, description="Email format if not using template")
