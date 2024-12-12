"""API Gateway Lambda Proxy event types for AWS Lambda.

This module contains both V1 and V2 payload format versions for HTTP API integration.
"""


from typing import Dict, List, Literal, Optional
from pydantic import BaseModel


class RequestContextIdentity(BaseModel):
    """Identity information in the request context.

    Args:
        accountId (str, optional): AWS account ID.
        accessKey (str, optional): AWS access key ID.
        apiKey (str, optional): API key used for the request.
        apiKeyId (str, optional): API key ID.
        caller (str, optional): Caller identity.
        cognitoAuthenticationProvider (str, optional): Cognito authentication provider.
        cognitoAuthenticationType (str, optional): Cognito authentication type.
        cognitoIdentityId (str, optional): Cognito identity ID.
        cognitoIdentityPoolId (str, optional): Cognito identity pool ID.
        principalOrgId (str, optional): AWS Organizations principal ID.
        sourceIp (str): Source IP address of the request.
        clientCert (dict, optional): Client certificate details.
        user (str, optional): User identity.
        userAgent (str, optional): User agent string.
        userArn (str, optional): User ARN.

    Reference:
        https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
    """
    accountId: Optional[str] = None
    accessKey: Optional[str] = None
    apiKey: Optional[str] = None
    apiKeyId: Optional[str] = None
    caller: Optional[str] = None
    cognitoAuthenticationProvider: Optional[str] = None
    cognitoAuthenticationType: Optional[str] = None
    cognitoIdentityId: Optional[str] = None
    cognitoIdentityPoolId: Optional[str] = None
    principalOrgId: Optional[str] = None
    sourceIp: str
    clientCert: Optional[Dict] = None
    user: Optional[str] = None
    userAgent: Optional[str] = None
    userArn: Optional[str] = None


class RequestContextV1(BaseModel):
    """Request context for API Gateway v1 payload format.

    Args:
        accountId (str): AWS account ID.
        apiId (str): API Gateway API identifier.
        authorizer (dict): Authorizer data.
        domainName (str, optional): Custom domain name.
        domainPrefix (str, optional): Custom domain prefix.
        extendedRequestId (str, optional): Extended request identifier.
        httpMethod (str): HTTP method used.
        identity (RequestContextIdentity): Identity information.
        operationName (str, optional): API operation name.
        path (str): Request path.
        protocol (str): Protocol used.
        requestId (str): Request identifier.
        requestTime (str, optional): Request timestamp.
        requestTimeEpoch (int): Request timestamp in epoch.
        resourceId (str): API Gateway resource identifier.
        resourcePath (str): Resource path.
        stage (str): API stage.
    """
    accountId: str
    apiId: str
    authorizer: Dict
    domainName: Optional[str] = None
    domainPrefix: Optional[str] = None
    extendedRequestId: Optional[str] = None
    httpMethod: str
    identity: RequestContextIdentity
    operationName: Optional[str] = None
    path: str
    protocol: str
    requestId: str
    requestTime: Optional[str] = None
    requestTimeEpoch: int
    resourceId: str
    resourcePath: str
    stage: str


class APIGatewayProxyV1Event(BaseModel):
    """API Gateway proxy event using v1 payload format.

    Args:
        resource (str): API Gateway resource.
        path (str): Request path.
        httpMethod (str): HTTP method.
        requestContext (RequestContextV1): Request context information.
        headers (Dict[str, str]): Request headers.
        multiValueHeaders (Dict[str, List[str]]): Multi-value request headers.
        queryStringParameters (Dict[str, str], optional): Query string parameters.
        multiValueQueryStringParameters (Dict[str, List[str]], optional): Multi-value query parameters.
        pathParameters (Dict[str, str], optional): Path parameters.
        stageVariables (Dict[str, str], optional): Stage variables.
        body (str, optional): Request body.
        isBase64Encoded (bool): Whether the body is base64 encoded.

    Reference:
        https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html
    """
    version: Literal["1.0"]
    resource: str
    path: str
    httpMethod: Literal["GET", "POST", "PUT",
                        "DELETE", "HEAD", "OPTIONS", "PATCH"]
    requestContext: RequestContextV1
    headers: Dict[str, str]
    multiValueHeaders: Dict[str, List[str]]
    queryStringParameters: Optional[Dict[str, str]] = None
    multiValueQueryStringParameters: Optional[Dict[str, List[str]]] = None
    pathParameters: Optional[Dict[str, str]] = None
    stageVariables: Optional[Dict[str, str]] = None
    body: Optional[str] = None
    isBase64Encoded: bool


class ClientCert(BaseModel):
    """Client certificate information.

    Args:
        clientCertPem (str): Client certificate in PEM format.
        subjectDN (str): Subject Distinguished Name.
        issuerDN (str): Issuer Distinguished Name.
        serialNumber (str): Certificate serial number.
        validity (Dict): Certificate validity information.
    """
    clientCertPem: str
    subjectDN: str
    issuerDN: str
    serialNumber: str
    validity: Dict


class Authentication(BaseModel):
    """Authentication information.

    Args:
        clientCert (ClientCert): Client certificate details.
    """
    clientCert: ClientCert


class JWTAuthorizer(BaseModel):
    """JWT token information.

    Args:
        claims (Dict[str, str]): JWT claims.
        scopes (List[str]): Authorization scopes.
    """
    claims: Dict[str, str]
    scopes: List[str]


class Authorizer(BaseModel):
    """Authorizer information.

    Args:
        jwt (JWTAuthorizer): JWT token details.
    """
    jwt: JWTAuthorizer


class HTTP(BaseModel):
    """HTTP request information.

    Args:
        method (str): HTTP method.
        path (str): Request path.
        protocol (str): Protocol version.
        sourceIp (str): Source IP address.
        userAgent (str): User agent string.
    """
    method: Literal["GET", "POST", "PUT",
                    "DELETE", "HEAD", "OPTIONS", "PATCH"]
    path: str
    protocol: str
    sourceIp: str
    userAgent: str


class RequestContextV2(BaseModel):
    """Request context for API Gateway v2 payload format.

    Args:
        accountId (str): AWS account ID.
        apiId (str): API Gateway API identifier.
        authentication (Authentication, optional): Authentication information.
        authorizer (Authorizer, optional): Authorizer information.
        domainName (str, optional): Custom domain name.
        domainPrefix (str, optional): Custom domain prefix.
        http (HTTP): HTTP request details.
        requestId (str): Request identifier.
        routeKey (str): API route key.
        stage (str): API stage.
        time (str): Request timestamp.
        timeEpoch (int): Request timestamp in epoch.

    Reference:
        https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    """
    accountId: str
    apiId: str
    authentication: Optional[Authentication] = None
    authorizer: Optional[Authorizer] = None
    domainName: Optional[str] = None
    domainPrefix: Optional[str] = None
    http: HTTP
    requestId: str
    routeKey: str
    stage: str
    time: str
    timeEpoch: int


class APIGatewayProxyV2Event(BaseModel):
    """API Gateway proxy event using v2 payload format.

    Args:
        version (str): API version.
        routeKey (str): API route key.
        rawPath (str): Raw request path.
        rawQueryString (str): Raw query string.
        cookies (List[str], optional): Request cookies.
        headers (Dict[str, str]): Request headers.
        queryStringParameters (Dict[str, str]): Query string parameters.
        requestContext (RequestContextV2): Request context information.
        body (str): Request body.
        pathParameters (Dict[str, str]): Path parameters.
        isBase64Encoded (bool): Whether the body is base64 encoded.
        stageVariables (Dict[str, str]): Stage variables.

    Reference:
        https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html
    """
    version: Literal["2.0"]
    routeKey: str
    rawPath: str
    rawQueryString: str
    cookies: Optional[List[str]] = None
    headers: Dict[str, str]
    queryStringParameters: Dict[str, str]
    requestContext: RequestContextV2
    body: str
    pathParameters: Dict[str, str]
    isBase64Encoded: bool
    stageVariables: Dict[str, str]
