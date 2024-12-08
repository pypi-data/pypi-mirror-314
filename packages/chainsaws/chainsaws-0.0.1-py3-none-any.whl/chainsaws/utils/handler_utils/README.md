# AWS Lambda Handler Utilities

A collection of utilities for AWS Lambda handlers that provides structured request handling, error management, and response formatting.

## Features

- **Simplified Lambda Handler Development**

  - Automatic request parsing and validation
  - Standardized response formatting
  - Comprehensive error handling
  - Built-in logging and monitoring support

- **Type Safety**

  - Full type hints support
  - Pydantic model validation
  - IDE-friendly development

- **Error Management**
  - Structured error responses
  - External error notification support
  - Configurable error tracking
  - Traceback management

## Installation

```bash
pip install chainsaws
```

## Quick Start

```python
from chainsaws.utils.handler_utils import aws_lambda_handler, get_body

@aws_lambda_handler()
def handler(event, context):
    # Automatically parses and validates the request body
    body = get_body(event)

    return {
        "message": "Success",
        "data": body
    }
```

## Core Components

### Event Model (LambdaEvent)

The `LambdaEvent` class provides a structured way to handle AWS Lambda event inputs:

```python
from chainsaws.utils.handler_utils import LambdaEvent

class LambdaEvent(BaseModel):
    body: Optional[str]                    # Request body (raw string)
    headers: Dict[str, str]                # HTTP headers
    requestContext: RequestContext         # Request context with identity info

    # Additional fields are allowed (e.g., queryStringParameters, pathParameters)
    model_config = ConfigDict(extra='allow')
```

Example usage:

```python
@aws_lambda_handler()
def handler(event, context):
    # Parse event
    event_data = LambdaEvent.model_validate(event)

    # Access event data
    body = event_data.get_json_body()      # Parsed JSON body
    headers = event_data.headers           # Request headers
    source_ip = event_data.requestContext.get_source_ip()  # Client IP

    return {"data": process_request(body)}
```

### Response Model (LambdaResponse)

The `LambdaResponse` class handles response formatting with proper headers and structure:

```python
from chainsaws.utils.handler_utils import LambdaResponse

class LambdaResponse(BaseModel):
    statusCode: int = 200                  # HTTP status code
    headers: ResponseHeaders               # Response headers with CORS
    body: str                             # Response body (JSON string)
    isBase64Encoded: bool = False         # Base64 encoding flag
```

Response creation:

```python
# Automatic creation via decorator
@aws_lambda_handler()
def handler(event, context):
    return {
        "data": "success",                 # Will be automatically formatted
        "meta": {"count": 42}
    }

    # Manual creation
    response = LambdaResponse.create(
        body={"message": "success"},
        content_type='application/json',
        status_code=200,
        charset='UTF-8'
    )
```

### Utility Functions

```python
from chainsaws.utils.handler_utils import get_body, get_headers, get_source_ip

# Get parsed JSON body
body = get_body(event)                     # Returns Dict[str, Any] or None

# Get request headers
headers = get_headers(event)               # Returns Dict[str, str]

# Get client IP
client_ip = get_source_ip(event)          # Returns str
```

## Response Format

### Successful Response

```json
{
  "statusCode": 200,
  "headers": {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Credentials": true,
    "Content-Type": "application/json; charset=UTF-8"
  },
  "body": {
    "rslt_cd": "S00000",
    "rslt_msg": "Call Success",
    "duration": 0.001,
    "data": {
      "your": "response data"
    }
  },
  "isBase64Encoded": false
}
```

### Error Response

```json
{
  "statusCode": 200,
  "headers": {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Credentials": true,
    "Content-Type": "application/json; charset=UTF-8"
  },
  "body": {
    "rslt_cd": "S99999",
    "rslt_msg": "Error message",
    "duration": 0.002,
    "traceback": "Error traceback..."
  },
  "isBase64Encoded": false
}
```

## Advanced Usage

### Custom Error Handling

```python
from chainsaws.utils.error_utils import AppError

def notify_slack(error_message: str):
    # Your error notification logic
    slack_client.post_message(error_message)

@aws_lambda_handler(error_receiver=notify_slack)
def handler(event, context):
    try:
        # Validate request
        body = get_body(event)
        if not body:
            raise AppError("B00001", "Missing request body")

        # Process request
        result = process_data(body)
        return {"data": result}

    except ValueError as e:
        raise AppError("B00002", str(e))
```

### Type Hints Support

```python
from typing import Dict, Any
from chainsaws.utils.handler_utils import LambdaEvent, LambdaResponse

def process_event(event_data: LambdaEvent) -> Dict[str, Any]:
    body = event_data.get_json_body()
    return {"processed": body}

def handler(event: Dict[str, Any], context: Any) -> LambdaResponse:
    event_data = LambdaEvent.model_validate(event)
    result = process_event(event_data)
    return {"data": result}
```

## Best Practices

1. **Use Type Validation**

   ```python
   from pydantic import BaseModel

   class UserRequest(BaseModel):
       name: str
       age: int

   @aws_lambda_handler()
   def handler(event, context):
       body = get_body(event)
       user_data = UserRequest.model_validate(body)
       return {"user": user_data.model_dump()}
   ```

2. **Handle Different Content Types**

   ```python
   @aws_lambda_handler(content_type='application/xml')
   def handler(event, context):
       return {"data": "<root>XML response</root>"}
   ```

3. **Custom Error Handling**

   ```python
   @aws_lambda_handler(
       error_receiver=notify_slack,
       ignore_app_errors=[NOT_FOUND_ERROR]
   )
   def handler(event, context):
       try:
           return process_request(get_body(event))
       except ResourceNotFoundError:
           raise AppError("B00404", "Resource not found")
   ```

4. **Request Context Usage**
   ```python
   @aws_lambda_handler()
   def handler(event, context):
       event_data = LambdaEvent.model_validate(event)
       return {
           "client_ip": event_data.requestContext.get_source_ip(),
           "request_id": event_data.requestContext.request_id
       }
   ```
