"""API Gateway WebSocket event types for AWS Lambda."""
from typing import Any, Dict, List, Literal
from pydantic import BaseModel


class Identity(BaseModel):
    """Client identity information.

    Args:
        accountId (str, optional): AWS account ID.
        apiKey (str, optional): API key used for the request.
        apiKeyId (str, optional): API key ID.
        caller (str, optional): Caller identity.
        cognitoAuthenticationProvider (str, optional): Cognito authentication provider.
        cognitoAuthenticationType (str, optional): Cognito authentication type.
        cognitoIdentityId (str, optional): Cognito identity ID.
        cognitoIdentityPoolId (str, optional): Cognito identity pool ID.
        sourceIp (str, optional): Client IP address.
        user (str, optional): User identity.
        userAgent (str, optional): Client user agent.
        userArn (str, optional): User ARN.
    """
    accountId: str | None = None
    apiKey: str | None = None
    apiKeyId: str | None = None
    caller: str | None = None
    cognitoAuthenticationProvider: str | None = None
    cognitoAuthenticationType: str | None = None
    cognitoIdentityId: str | None = None
    cognitoIdentityPoolId: str | None = None
    sourceIp: str | None = None
    user: str | None = None
    userAgent: str | None = None
    userArn: str | None = None


class Error(BaseModel):
    """Error information for failed requests.

    Args:
        message (str, optional): Error message.
        messageString (str, optional): Detailed error message.
        validationErrorString (str, optional): Validation error details.
    """
    message: str | None = None
    messageString: str | None = None
    validationErrorString: str | None = None


class RequestContext(BaseModel):
    """WebSocket connection context.

    Args:
        connectionId (str): Unique connection identifier.
        connectedAt (int): Connection timestamp.
        domainName (str): API's domain name.
        eventType (str): Type of event (CONNECT/DISCONNECT/MESSAGE).
        routeKey (str): Route selection key.
        requestId (str): Unique request identifier.
        extendedRequestId (str): Extended request identifier.
        apiId (str): API Gateway API identifier.
        authorizer (Dict[str, Any]): Authorizer context.
        requestTime (str): Request timestamp string.
        requestTimeEpoch (int): Request timestamp in epoch.
        messageDirection (str): Message direction (IN/OUT).
        stage (str): API stage.
        identity (Identity): Client identity information.
        messageId (str, optional): Unique message ID (for MESSAGE events).
        error (Error, optional): Error information.
        status (int, optional): Response status code.
    """
    connectionId: str
    connectedAt: int
    domainName: str
    eventType: Literal["CONNECT", "DISCONNECT", "MESSAGE"]
    routeKey: str
    requestId: str
    extendedRequestId: str
    apiId: str
    authorizer: Dict[str, Any]
    requestTime: str
    requestTimeEpoch: int
    messageDirection: Literal["IN", "OUT"]
    stage: str
    identity: Identity
    messageId: str | None = None
    error: Error | None = None
    status: int | None = None


class WebSocketConnectEvent(BaseModel):
    """Event for WebSocket $connect and $disconnect routes.

    Args:
        requestContext (RequestContext): Connection context.
        isBase64Encoded (bool): Whether the payload is base64 encoded.
        headers (Dict[str, str]): Request headers.
        multiValueHeaders (Dict[str, List[str]]): Headers with multiple values.
        queryStringParameters (Dict[str, str]): Query string parameters.
        multiValueQueryStringParameters (Dict[str, List[str]]): Parameters with multiple values.

    Reference:
        https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-mapping-template-reference.html
    """
    requestContext: RequestContext
    isBase64Encoded: bool
    headers: Dict[str, str]
    multiValueHeaders: Dict[str, List[str]]
    queryStringParameters: Dict[str, str]
    multiValueQueryStringParameters: Dict[str, List[str]]


class WebSocketRouteEvent(BaseModel):
    """Event for WebSocket custom routes and $default route.

    Args:
        requestContext (RequestContext): Connection context.
        isBase64Encoded (bool): Whether the payload is base64 encoded.
        body (str): Message payload.

    Reference:
        https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-mapping-template-reference.html
    """
    requestContext: RequestContext
    isBase64Encoded: bool
    body: str
