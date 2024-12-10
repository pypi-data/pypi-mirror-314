"""Error handling utilities for external error monitoring and reporting."""

import pprint
import traceback
from typing import Any

from chainsaws.utils.error_utils.error_utils_models import AppError, ErrorDescription, ErrorEvent

# Constant for max payload length for error message
MAX_PAYLOAD_LENGTH = 3000


def make_error_description(event: dict[str, Any]) -> str:
    """Create formatted error description from event."""
    return _create_error_description(event).format()


def _create_error_description(event: dict[str, Any]) -> ErrorDescription:
    """Internal function to create ErrorDescription instance."""
    try:
        error_event = ErrorEvent.model_validate(event)
        payload_str = _format_payload(event)
        cloudwatch_query = None

        if len(payload_str) > MAX_PAYLOAD_LENGTH:
            payload_str = payload_str[:MAX_PAYLOAD_LENGTH] + "..."
            cloudwatch_query = _generate_cloudwatch_query(
                error_event.request_context.request_id,
            )

        return ErrorDescription(
            source_ip=error_event.request_context.identity.source_ip,
            request_id=error_event.request_context.request_id,
            request_payload=payload_str,
            error_traceback=traceback.format_exc(),
            cloudwatch_query=cloudwatch_query,
        )
    except Exception as e:
        # Fallback for invalid events
        return ErrorDescription(
            request_id="unknown",
            request_payload=str(event),
            error_traceback=f"Event parsing failed: {
                e!s}\n{traceback.format_exc()}",
        )


def _format_payload(event: dict[str, Any]) -> str:
    """Format event payload for display."""
    return pprint.pformat(event, indent=1)


def _generate_cloudwatch_query(request_id: str) -> str:
    """Generate CloudWatch Logs query."""
    return f"""
    fields @timestamp, @message
    | filter requestContext.requestId = "{request_id}"
    | sort @timestamp desc
    | limit 20
    """.strip()


if __name__ == "__main__":
    sample_event = {
        "requestContext": {
            "requestId": "test-request-id",
            "identity": {
                "sourceIp": "127.0.0.1",
                "userAgent": "Mozilla/5.0",
            },
        },
        "body": "test body",
    }


    error = AppError(
        code="S00005",
        message="Invalid S3 Query Command",
        details={"query": "SELECT * FROM invalid_table"},
    )
