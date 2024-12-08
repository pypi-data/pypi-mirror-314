from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AppError(BaseModel):
    """Base application error model."""

    code: str = Field(..., description="Error Code of Application Error")
    message: str = Field(..., description="Description of Application Error")
    timestamp: datetime = Field(default_factory=datetime.now)
    details: dict[str, Any] | None = None

    model_config = ConfigDict(frozen=True)

    def __str__(self) -> str:
        """Convert error to string."""
        return f"AppError[{self.code}]: {self.message}"

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary."""
        return self.model_dump()


class RequestIdentity(BaseModel):
    """Request identity information."""

    source_ip: str | None = Field(None, alias="sourceIp")
    user_agent: str | None = Field(None, alias="userAgent")
    user_arn: str | None = Field(None, alias="userArn")


class RequestContext(BaseModel):
    """AWS request context."""

    request_id: str = Field(..., alias="requestId")
    identity: RequestIdentity
    stage: str | None = None
    path: str | None = None
    http_method: str | None = Field(None, alias="httpMethod")


class ErrorEvent(BaseModel):
    """Error event with request context."""

    request_context: RequestContext = Field(..., alias="requestContext")
    body: str | None = None
    path_parameters: dict[str, str] | None = Field(
        None, alias="pathParameters")
    query_string_parameters: dict[str, str] | None = Field(
        None, alias="queryStringParameters")


class ErrorDescription(BaseModel):
    """Structured error description."""

    timestamp: datetime = Field(default_factory=datetime.now)
    source_ip: str | None = None
    request_id: str
    request_payload: str
    error_traceback: str
    cloudwatch_query: str | None = None

    def format(self) -> str:
        """Format error description for display."""
        description = f"""
        *Timestamp: * {self.timestamp.isoformat()}
        *Source IP: * {self.source_ip or 'unknown'}
        *Request ID: * {self.request_id}

        *Request Payload: *
        {self.request_payload}

        *Traceback: *
        {self.error_traceback}
        """.strip()

        if self.cloudwatch_query:
            description += f"\n\n*See more in CloudWatch Logs:*\n```{
                self.cloudwatch_query}```"

        return description
