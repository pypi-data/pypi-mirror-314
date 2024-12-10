"""AWS Lambda handler utilities for request/response handling.

This module provides utilities for handling AWS Lambda functions, including:
- Request/response handling
- Error management
- Input validation
- Response formatting

Example:
    from chainsaws.utils.handler_utils import aws_lambda_handler, get_body

    @aws_lambda_handler(error_receiver=notify_slack)
    def handler(event, context):
        body = get_body(event)
        return {
            "message": "Success",
            "data": process_request(body)
        }

"""

from chainsaws.utils.handler_utils.handler_utils import (
    aws_lambda_handler,
    get_body,
    get_headers,
    get_source_ip,
)
from chainsaws.utils.handler_utils.handler_utils_models import (
    LambdaEvent,
    LambdaResponse,
)

__all__ = [
    "LambdaEvent",
    "LambdaResponse",
    "aws_lambda_handler",
    "get_body",
    "get_headers",
    "get_source_ip",
]
