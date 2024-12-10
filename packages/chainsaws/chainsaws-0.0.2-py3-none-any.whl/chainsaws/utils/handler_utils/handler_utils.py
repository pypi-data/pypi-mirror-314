"""AWS Lambda handler utilities for request/response handling and error management.

Provides structured request parsing and response formatting with error handling.
"""

import time
import traceback
from collections.abc import Callable
from functools import wraps
from typing import Any

from chainsaws.utils.error_utils.error_utils import AppError, make_error_description
from chainsaws.utils.handler_utils.handler_utils_models import (
    HandlerConfig,
    LambdaEvent,
    LambdaResponse,
)


def aws_lambda_handler(
    error_receiver: Callable[[str], Any] | None = None,
    content_type: str = "application/json",
    use_traceback: bool = True,
    ignore_app_errors: list[AppError] | None = None,
) -> Callable:
    """Decorator for AWS Lambda handlers with error handling and response formatting.

    Args:
        error_receiver: Callback function for error notifications
        content_type: Response content type
        use_traceback: Include traceback in error responses
        ignore_app_errors: List of AppErrors to ignore for notifications

    Example:
        @aws_lambda_handler(error_receiver=notify_slack)
        def handler(event, context):
            body = LambdaEvent.parse_obj(event).get_json_body()
            return {"message": "Success"}

    """
    config = HandlerConfig(
        error_receiver=error_receiver,
        content_type=content_type,
        use_traceback=use_traceback,
        ignore_app_errors=ignore_app_errors or [],
    )

    def decorator(func: Callable[..., Any]) -> Callable[..., LambdaResponse]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> LambdaResponse:
            start_time = time.time()
            event = args[0] if args else {}

            try:
                result = func(*args, **kwargs) or {}

                if isinstance(result, dict):
                    result.setdefault("rslt_cd", "S00000")
                    result.setdefault("rslt_msg", "Call Success")
                    result["duration"] = time.time() - start_time

                return LambdaResponse.create(result, content_type=config.content_type)

            except AppError as ex:
                result = {
                    "rslt_cd": ex.code,
                    "rslt_msg": ex.message,
                    "duration": time.time() - start_time,
                }

                if config.use_traceback:
                    result["traceback"] = traceback.format_exc()

                if config.error_receiver and ex.code not in {e.code for e in config.ignore_app_errors}:
                    try:
                        message = make_error_description(event)
                        config.error_receiver(message)
                    except Exception as err:
                        result["error_receiver_failed"] = str(err)

                return LambdaResponse.create(result)

            except Exception as ex:
                result = {
                    "rslt_cd": "S99999",
                    "rslt_msg": str(ex),
                    "duration": time.time() - start_time,
                }

                if config.use_traceback:
                    result["traceback"] = traceback.format_exc()

                if config.error_receiver:
                    try:
                        message = make_error_description(event)
                        config.error_receiver(message)
                    except Exception as err:
                        result["error_receiver_failed"] = str(err)

                return LambdaResponse.create(result)

        return wrapper
    return decorator


"""
Utility functions
"""


def get_event_data(event: dict[str, Any]) -> LambdaEvent:
    """Get event data."""
    return LambdaEvent.model_validate(event)


def get_body(event: dict[str, Any]) -> dict[str, Any] | None:
    """Get JSON body from event."""
    return get_event_data(event).get_json_body()


def get_headers(event: dict[str, Any]) -> dict[str, str]:
    """Get request headers."""
    return get_event_data(event).headers


def get_source_ip(event: dict[str, Any]) -> str | None:
    """Get source IP address from event."""
    return get_event_data(event).requestContext.get_source_ip()
