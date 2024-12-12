from enum import Enum

from pydantic import BaseModel, Field, field_validator

from chainsaws.aws.shared.config import APIConfig


class LambdaAPIConfig(APIConfig):
    """Configuration for LambdaAPI."""



class InvocationType(str, Enum):
    """Lambda function invocation types."""

    REQUEST_RESPONSE = "RequestResponse"
    EVENT = "Event"
    DRY_RUN = "DryRun"


class PythonRuntime(str, Enum):
    """Supported Python runtimes for Lambda functions."""

    PYTHON_313 = "python3.13"
    PYTHON_312 = "python3.12"
    PYTHON_311 = "python3.11"
    PYTHON_310 = "python3.10"
    PYTHON_39 = "python3.9"


class LambdaHandler(BaseModel):
    """Lambda function handler configuration.

    Defaults to "index", "handler" # index.handler

    Example:
        handler = LambdaHandler(module_path="app", function_name="handler")  # app.handler
        handler = LambdaHandler(module_path="src.functions.app", function_name="process_event")  # src.functions.app.process_event

    """

    module_path: str = Field(
        "index", description="Module path (e.g., 'app' or 'src.functions.app')")
    function_name: str = Field(
        "handler", description="Function name (e.g., 'handler' or 'process_event')")

    @field_validator("module_path", "function_name")
    @classmethod
    def validate_python_identifier(cls, v: str) -> str:
        """Validate that the path components are valid Python identifiers."""
        for part in v.split("."):
            if not part.isidentifier():
                msg = f"'{part}' is not a valid Python identifier"
                raise ValueError(msg)
        return v

    def __str__(self) -> str:
        return f"{self.module_path}.{self.function_name}"


class FunctionConfiguration(BaseModel):
    """Lambda function configuration."""

    FunctionName: str
    FunctionArn: str
    Runtime: str
    Role: str
    Handler: str
    CodeSize: int
    Description: str | None = None
    Timeout: int
    MemorySize: int
    LastModified: str
    CodeSha256: str
    Version: str
    Environment: dict[str, dict[str, str]] | None = None
    TracingConfig: dict[str, str] | None = None
    RevisionId: str | None = None
    State: str | None = None
    LastUpdateStatus: str | None = None
    PackageType: str | None = None
    Architectures: list[str] | None = None


class FunctionCode(BaseModel):
    """Lambda function code configuration."""

    ZipFile: bytes | None = None
    S3Bucket: str | None = None
    S3Key: str | None = None
    S3ObjectVersion: str | None = None
    ImageUri: str | None = None


class CreateFunctionRequest(BaseModel):
    """Request model for creating Lambda function."""

    FunctionName: str
    Runtime: PythonRuntime
    Role: str
    Handler: str
    Code: FunctionCode
    Description: str | None = None
    Timeout: int = Field(default=3, ge=1, le=900)
    MemorySize: int = Field(default=128, ge=128, le=10240)
    Publish: bool = False
    Environment: dict[str, dict[str, str]] | None = None
    Tags: dict[str, str] | None = None
    Architectures: list[str] | None = Field(default=["x86_64"])


class TriggerType(Enum):
    """Supported Lambda trigger types."""

    API_GATEWAY = "apigateway"
    S3 = "s3"
    EVENTBRIDGE = "eventbridge"
    SNS = "sns"
    SQS = "sqs"
    DYNAMODB = "dynamodb"
