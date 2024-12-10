from enum import Enum
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, Field, HttpUrl

from chainsaws.aws.shared.config import APIConfig

BucketACL = Literal["private", "public-read",
                    "public-read-write", "authenticated-read"]


class ContentType(str, Enum):
    """Common MIME content types."""

    # Application types
    JSON = "application/json"
    PDF = "application/pdf"
    ZIP = "application/zip"
    GZIP = "application/gzip"
    EXCEL = "application/vnd.ms-excel"
    EXCEL_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    WORD = "application/msword"
    WORD_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    BINARY = "application/octet-stream"

    # Text types
    TEXT = "text/plain"
    HTML = "text/html"
    CSS = "text/css"
    CSV = "text/csv"
    XML = "text/xml"

    # Image types
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    SVG = "image/svg+xml"
    WEBP = "image/webp"
    ICO = "image/x-icon"

    # Audio types
    MP3 = "audio/mpeg"
    WAV = "audio/wav"
    OGG = "audio/ogg"

    # Video types
    MP4 = "video/mp4"
    MPEG = "video/mpeg"
    WEBM = "video/webm"

    @classmethod
    def from_extension(cls, extension: str) -> "ContentType":
        """Get content type from file extension."""
        extension = extension.lower().lstrip(".")
        mapping = {
            # Application
            "json": cls.JSON,
            "pdf": cls.PDF,
            "zip": cls.ZIP,
            "gz": cls.GZIP,
            "xls": cls.EXCEL,
            "xlsx": cls.EXCEL_XLSX,
            "doc": cls.WORD,
            "docx": cls.WORD_DOCX,

            # Text
            "txt": cls.TEXT,
            "html": cls.HTML,
            "htm": cls.HTML,
            "css": cls.CSS,
            "csv": cls.CSV,
            "xml": cls.XML,

            # Image
            "jpg": cls.JPEG,
            "jpeg": cls.JPEG,
            "png": cls.PNG,
            "gif": cls.GIF,
            "svg": cls.SVG,
            "webp": cls.WEBP,
            "ico": cls.ICO,

            # Audio
            "mp3": cls.MP3,
            "wav": cls.WAV,
            "ogg": cls.OGG,

            # Video
            "mp4": cls.MP4,
            "mpeg": cls.MPEG,
            "webm": cls.WEBM,
        }

        return mapping.get(extension, cls.BINARY)


class S3APIConfig(APIConfig):
    """Configuration for S3API."""

    acl: BucketACL = Field(
        default="private",
        description="Bucket ACL",
    )
    use_accelerate: bool = Field(
        default=True, description="Config for bucket-level data acceleration in objects that enabled faster data transfer")


class BucketConfig(BaseModel):
    """Bucket creation/management configuration."""

    bucket_name: str = Field(..., description="Name of the S3 bucket")
    acl: BucketACL = Field(
        default="private",
        description="Bucket ACL",
    )
    use_accelerate: bool = Field(
        default=True, description="Config for bucket-level data acceleration in objects that enabled faster data transfer")


class FileUploadConfig(BaseModel):
    """File upload configuration."""

    bucket_name: str = Field(..., description="Target bucket name")
    file_name: str = Field(..., description="Target file name (key)")
    content_type: ContentType | None = Field(
        default=None,
        description="Content type of the file",
    )


class ObjectListConfig(BaseModel):
    """Configuration for listing objects."""

    prefix: str = Field(default="", description="Prefix for filtering objects")
    continuation_token: str | None = Field(
        default=None, description="Continuation token for pagination")
    start_after: str | None = Field(
        default=None, description="Start listing after this key")
    limit: int = Field(default=1000, le=1000,
                       description="Maximum number of objects to return")


class FileUploadResult(BaseModel):
    """Result of file upload operation."""

    url: HttpUrl = Field(..., description="Public URL of uploaded file")
    object_key: str = Field(..., description="S3 object key")


class PresignedUrlConfig(BaseModel):
    """Configuration for presigned URL generation."""

    bucket_name: str = Field(..., description="Bucket name")
    object_name: str = Field(..., description="Object key")
    client_method: Literal["get_object",
                           "put_object"] = Field(..., description="S3 client method")
    content_type: str | None = Field(
        default=None, description="Content type of the object")
    acl: BucketACL = Field(
        default="private",
        description="Object ACL",
    )
    expiration: int = Field(default=3600, ge=1, le=604800,
                            description="URL expiration in seconds")


class SelectObjectConfig(BaseModel):
    """Configuration for S3 Select operations."""

    bucket_name: str = Field(..., description="Bucket name")
    object_key: str = Field(..., description="Object key")
    query: str = Field(..., description="SQL query to execute")
    input_serialization: dict[str, Any] = Field(
        default_factory=lambda: {"JSON": {"Type": "DOCUMENT"}},
        description="Input serialization configuration",
    )
    output_serialization: dict[str, Any] = Field(
        default_factory=lambda: {"JSON": {}},
        description="Output format configuration",
    )


class CopyObjectResult(BaseModel):
    """Result of copy object operation."""

    success: bool = Field(
        description="Whether the copy operation was successful",
    )
    url: str | None = Field(
        description="URL of the copied object if successful",
    )
    object_key: str = Field(
        description="Key of the copied object",
    )
    error_message: str | None = Field(
        default=None,
        description="Error message if copy failed",
    )


class BulkUploadItem(BaseModel):
    """Configuration for a single file in bulk upload."""

    object_key: str = Field(
        ...,
        description="The key (path) where the object will be stored in S3",
    )
    data: bytes | str = Field(
        ...,
        description="File data: can be bytes, file object, or path to file",
    )
    content_type: ContentType | None = Field(
        default=None,
        description="MIME type of the file. If not provided, will be guessed from extension",
    )
    acl: str = Field(
        default="private",
        description="S3 access control list setting (e.g., 'private', 'public-read')",
        pattern="^(private|public-read|public-read-write|authenticated-read)$",
    )


class BulkUploadResult(BaseModel):
    """Result of a bulk upload operation."""

    successful: dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary of successful uploads mapping object_key to S3 URL",
    )
    failed: dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary of failed uploads mapping object_key to error message",
    )

    class Config:
        """Pydantic model configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "successful": {
                    "folder/file1.pdf": "https://bucket.s3.region.amazonaws.com/folder/file1.pdf",
                    "folder/file2.jpg": "https://bucket.s3.region.amazonaws.com/folder/file2.jpg",
                },
                "failed": {
                    "folder/file3.txt": "File not found: /path/to/file3.txt",
                },
            },
        }


class S3SelectFormat(str, Enum):
    """S3 Select input/output format."""

    JSON = "JSON"
    CSV = "CSV"
    PARQUET = "PARQUET"


class S3SelectJSONType(str, Enum):
    """S3 Select JSON type."""

    DOCUMENT = "DOCUMENT"
    LINES = "LINES"


class S3SelectCSVConfig(BaseModel):
    """Configuration for CSV format in S3 Select."""

    file_header_info: str | None = Field(
        None, description="FileHeaderInfo (NONE, USE, IGNORE)")
    delimiter: str = Field(",", description="Field delimiter")
    quote_character: str = Field('"', description="Quote character")
    quote_escape_character: str = Field(
        '"', description="Quote escape character")
    comments: str | None = Field(None, description="Comment character")
    record_delimiter: str = Field("\n", description="Record delimiter")


class S3SelectConfig(BaseModel):
    """Configuration for S3 Select operations."""

    query: str = Field(..., description="SQL query to execute")
    input_format: S3SelectFormat = Field(..., description="Input format")
    output_format: S3SelectFormat = Field(
        S3SelectFormat.JSON, description="Output format")
    compression_type: str | None = Field(
        None, description="Input compression (NONE, GZIP, BZIP2)")
    json_type: S3SelectJSONType | None = Field(
        None, description="JSON input type")
    csv_input_config: S3SelectCSVConfig | None = Field(
        None, description="CSV input configuration")
    csv_output_config: S3SelectCSVConfig | None = Field(
        None, description="CSV output configuration")
    max_rows: int | None = Field(
        None, description="Maximum number of rows to return")
