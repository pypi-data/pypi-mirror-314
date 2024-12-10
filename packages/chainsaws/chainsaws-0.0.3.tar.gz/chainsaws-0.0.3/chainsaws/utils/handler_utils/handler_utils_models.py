"""Models for AWS Lambda handler utilities.

Defines request and response structures for Lambda functions.
"""
import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from chainsaws.utils.dict_utils.dict_utils import convert_decimal_to_number


class RequestContext(BaseModel):
    """AWS API Gateway request context."""

    identity: dict[str, Any] = Field(default_factory=dict)
    request_id: str | None = None

    def get_source_ip(self) -> str | None:
        """Get source IP address from request context."""
        return self.identity.get("sourceIp", None)


class ResponseHeaders(BaseModel):
    """API Gateway response headers."""

    Access_Control_Allow_Origin: str = Field(
        default="*", alias="Access-Control-Allow-Origin")
    Access_Control_Allow_Headers: str = Field(
        default="*", alias="Access-Control-Allow-Headers")
    Access_Control_Allow_Credentials: bool = Field(
        default=True, alias="Access-Control-Allow-Credentials")
    Access_Control_Allow_Methods: str = Field(
        default="*", alias="Access-Control-Allow-Methods")
    Content_Type: str = Field(default="application/json", alias="Content-Type")
    charset: str = Field(default="UTF-8")


class HandlerConfig(BaseModel):
    """Handler wrapper configuration."""

    error_receiver: Any | None = None
    content_type: str = "application/json"
    use_traceback: bool = True
    ignore_app_errors: list = Field(default_factory=list)


class LambdaEvent(BaseModel):
    """AWS Lambda event structure."""

    body: str | None = None
    headers: dict[str, str] = Field(default_factory=dict)
    request_context: RequestContext = Field(default_factory=RequestContext)

    model_config = ConfigDict(
        extra="allow",
        arbitrary_types_allowed=True,
    )

    def get_json_body(self) -> dict[str, Any] | None:
        """Get JSON body from event."""
        if not self.body:
            return None
        try:
            return json.loads(self.body)
        except json.JSONDecodeError:
            return None


class LambdaResponse(BaseModel):
    """AWS Lambda response structure."""

    status_code: int = 200
    headers: ResponseHeaders
    body: str
    is_base64_encoded: bool = False

    @classmethod
    def create(cls, body: dict[str, Any] | str, **kwargs: dict[str, Any] | str) -> "LambdaResponse":
        """Create formatted response."""
        headers = ResponseHeaders(**kwargs)
        body_str = json.dumps(convert_decimal_to_number(
            body), default=str) if isinstance(body, dict) else str(body)
        return cls(headers=headers, body=body_str)
