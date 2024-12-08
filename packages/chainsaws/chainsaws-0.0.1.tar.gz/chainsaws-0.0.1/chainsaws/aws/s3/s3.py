import io
import json
import logging
import time
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from secrets import token_urlsafe
from typing import Any, BinaryIO
from urllib.parse import urljoin

from chainsaws.aws.s3._s3_internal import S3
from chainsaws.aws.s3.s3_models import (
    BucketConfig,
    BulkUploadItem,
    BulkUploadResult,
    ContentType,
    CopyObjectResult,
    FileUploadConfig,
    FileUploadResult,
    ObjectListConfig,
    PresignedUrlConfig,
    S3APIConfig,
    S3SelectCSVConfig,
    S3SelectFormat,
    S3SelectJSONType,
    SelectObjectConfig,
)
from chainsaws.aws.s3.s3_utils import validate_bucket_name
from chainsaws.aws.shared import session

logger = logging.getLogger(__name__)


class S3API:
    """High level API for S3 operations."""

    def __init__(self, bucket_name: str, config: S3APIConfig | None = None) -> None:
        validate_bucket_name(bucket_name=bucket_name)

        self.config = config or S3APIConfig()

        self.boto3_session = session.get_boto_session(
            credentials=self.config.credentials,
        )
        self.bucket_name: str = bucket_name
        self.s3 = S3(boto3_session=self.boto3_session,
                     bucket_name=bucket_name, config=config)

    def _get_base_url(self, bucket_name: str | None = None, use_accelerate: bool = False) -> str:
        """Generate base URL for S3 bucket.

        Args:
            bucket_name: Optional bucket name (defaults to self.bucket_name)
            use_accelerate: Whether to use S3 Transfer Acceleration

        Returns:
            str: Base URL for the S3 bucket

        """
        target_bucket = bucket_name or self.bucket_name

        if use_accelerate:
            return f"https://{target_bucket}.s3-accelerate.amazonaws.com/"

        return f"https://{target_bucket}.s3.{self.s3.region}.amazonaws.com/"

    def init_s3_bucket(self) -> None:
        """Initialize S3 bucket."""
        bucket_config = BucketConfig(
            bucket_name=self.bucket_name, acl=self.config.acl, use_accelerate=self.config.use_accelerate)
        return self.s3.init_bucket(config=bucket_config)

    def upload_binary(self, file_name: str, binary: bytes) -> None:
        return self.s3.upload_binary(self.bucket_name, file_name, binary)

    def upload_file_and_return_url(
        self,
        file_bytes: bytes,
        extension: str | None = None,
        object_key: str | None = None,
        content_type: ContentType | None = None,
    ) -> FileUploadResult:
        """Uploads a file to an S3 bucket and returns its public URL.

        This method uploads the provided file bytes to the specified S3 bucket
        and generates a public URL for accessing the uploaded file. The file
        can be uploaded with a specified content type and an optional unique
        file identifier.

        Args:
            file_bytes (bytes): The file data to be uploaded.
            extension (str): The file extension used to determine the content type.
            content_type (Optional[ContentType]): The MIME type of the file. If not provided,
                it will be inferred from the file extension.
            object_key (Optional[str]): An optional file identifier. If not provided,
                a unique identifier will be generated.

        Returns:
            FileUploadResult: An object containing the public URL and the object key of the uploaded file.

        Raises:
            Exception: If the upload fails due to network issues, invalid credentials, or other errors.

        Example:
            >>> result = s3_api.upload_file_and_return_url(
            ...     file_bytes=b"Hello, World!",
            ...     extension="txt"
            ... )
            >>> print(result.url)
            https://mybucket.s3.amazonaws.com/unique-file-id.txt

        """
        if not extension and object_key and "." in object_key:
            extension = object_key.split(".")[-1]

        extension = extension or ""

        file_id = object_key or f'{token_urlsafe(
            32)}{f".{extension}" if extension else ""}'

        content_type = content_type or (
            ContentType.from_extension(extension) if extension
            else ContentType.BINARY
        )

        upload_config = FileUploadConfig(
            bucket_name=self.bucket_name,
            file_name=file_id,
            content_type=content_type,
        )

        self.s3.upload_file(upload_config, file_bytes)

        base_url = self._get_base_url(
            use_accelerate=self.config.use_accelerate)

        return FileUploadResult(
            url=urljoin(base_url, file_id),
            object_key=file_id,
        )

    def upload_items_for_select(self, file_name: str, item_list: list[dict[str, Any]]) -> None:
        """Upload JSON items for S3 Select queries."""
        if not all(isinstance(item, dict) for item in enumerate(item_list)):
            msg = "All items must be dictionaries"
            raise ValueError(msg)

        json_string = "\n".join(json.dumps(item) for item in item_list)
        return self.upload_binary(file_name, json_string.encode("utf-8"))

    def upload_large_file(
        self,
        object_key: str,
        file_bytes: bytes | BinaryIO,
        content_type: ContentType | None = None,
        part_size: int = 5 * 1024 * 1024,  # 5MB
    ) -> FileUploadResult:
        """Upload a large file using multipart upload.

        Args:
            object_key: The key to store the object under
            file_bytes: File data as bytes or file-like object
            content_type: Optional content type
            part_size: Size of each part in bytes (minimum 5MB)

        Returns:
            FileUploadResult: An object containing the public URL and the object key of the uploaded file

        """
        if content_type is None:
            extension = object_key.split(".")[-1] if "." in object_key else ""
            content_type = ContentType.from_extension(extension)

        if isinstance(file_bytes, bytes):
            file_bytes = io.BytesIO(file_bytes)

        try:
            upload_id = self.s3.create_multipart_upload(
                self.bucket_name,
                object_key,
                content_type,
            )

            parts = []
            part_number = 1

            while True:
                data = file_bytes.read(part_size)
                if not data:
                    break

                if len(data) < part_size and part_number == 1:
                    # If it's the first part and smaller than part_size,
                    # we should do a regular upload instead
                    self.s3.abort_multipart_upload(
                        self.bucket_name,
                        object_key,
                        upload_id,
                    )

                    return self.upload_file_and_return_url(
                        file_bytes=data,
                        extension=object_key.split(".")[-1],
                        object_key=object_key,
                        content_type=content_type,
                    )

                part = self.s3.upload_part(
                    self.bucket_name,
                    object_key,
                    upload_id,
                    part_number,
                    data,
                )
                parts.append({
                    "PartNumber": part_number,
                    "ETag": part["ETag"],
                })
                part_number += 1

            self.s3.complete_multipart_upload(
                self.bucket_name,
                object_key,
                upload_id,
                parts,
            )

            base_url = self._get_base_url(
                use_accelerate=self.config.use_accelerate)

            return FileUploadResult(
                url=urljoin(base_url, object_key),
                object_key=object_key,
            )

        except Exception as ex:
            logger.exception(f"Failed to upload large file: {ex!s}")
            if "upload_id" in locals():
                self.s3.abort_multipart_upload(
                    self.bucket_name,
                    object_key,
                    upload_id,
                )
            raise

    def bulk_upload(
        self,
        items: list[BulkUploadItem],
        max_workers: int | None = None,
        part_size: int = 5 * 1024 * 1024,  # 5MB
    ) -> BulkUploadResult:
        """Upload multiple files in parallel.

        Args:
            items: List of BulkUploadItem configurations
            max_workers: Maximum number of concurrent uploads (defaults to min(32, os.cpu_count() * 4))
            part_size: Size of each part for multipart uploads

        Returns:
            BulkUploadResult containing successful and failed uploads

        """
        result = BulkUploadResult()

        def upload_item(item: BulkUploadItem) -> tuple[str, str | Exception]:
            try:
                # Handle different input types
                if isinstance(item.data, str):
                    # It's a file path
                    path = Path(item.data)
                    if not path.exists():
                        msg = f"File not found: {item.data!s}"
                        raise FileNotFoundError(
                            msg)

                    file_size = path.stat().st_size
                    if file_size > part_size:
                        # Use multipart upload for large files
                        with open(path, "rb") as f:
                            self.upload_large_file(
                                object_key=item.object_key,
                                file_data=f,
                                content_type=item.content_type,
                                part_size=part_size,
                                acl=item.acl,
                            )
                    else:
                        with open(path, "rb") as f:
                            data = f.read()
                            self.upload_file_and_return_url(
                                file_bytes=data,
                                extension=path.suffix[1:],  # Remove the dot
                                content_type=item.content_type,
                                forced_file_id=item.object_key,
                                acl=item.acl,
                            )
                # It's bytes or file-like object
                elif isinstance(item.data, bytes):
                    if len(item.data) > part_size:
                        self.upload_large_file(
                            object_key=item.object_key,
                            file_data=item.data,
                            content_type=item.content_type,
                            part_size=part_size,
                            acl=item.acl,
                        )
                    else:
                        self.upload_file_and_return_url(
                            file_bytes=item.data,
                            extension=item.object_key.split(".")[-1],
                            content_type=item.content_type,
                            forced_file_id=item.object_key,
                            acl=item.acl,
                        )
                else:
                    # File-like object
                    self.upload_large_file(
                        object_key=item.object_key,
                        file_data=item.data,
                        content_type=item.content_type,
                        part_size=part_size,
                        acl=item.acl,
                    )

                url = self.get_url_by_object_key(item.object_key)
                return item.object_key, url

            except Exception as ex:
                logger.exception(f"Failed to upload {item.object_key}: {ex!s}")
                return item.object_key, str(ex)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(upload_item, item) for item in items]

            for future in futures:
                try:
                    object_key, result_or_error = future.result()
                    if isinstance(result_or_error, Exception):
                        result.failed[object_key] = str(result_or_error)
                    else:
                        result.successful[object_key] = result_or_error
                except Exception as ex:
                    logger.exception(f"Unexpected error in bulk upload: {ex!s}")

        return result

    def generate_object_keys(
        self,
        prefix: str,
        start_after: str | None = None,
        limit: int = 1000,
    ) -> Generator[dict[str, Any], None, None]:
        """Generate object keys with pagination."""
        continuation_token = None

        while True:
            list_config = ObjectListConfig(
                prefix=prefix,
                continuation_token=continuation_token,
                start_after=start_after,
                limit=limit,
            )

            response = self.s3.list_objects_v2(list_config)

            yield from response.get("Contents", [])

            continuation_token = response.get("NextContinuationToken")
            if not continuation_token:
                break

    def select(self, object_key: str, query: str) -> dict[str, Any]:
        """Execute S3 Select query."""
        select_config = SelectObjectConfig(
            bucket_name=self.bucket_name,
            object_key=object_key,
            query=query,
            input_serialization={"JSON": {"Type": "DOCUMENT"}},
            output_serialization={"JSON": {}},
        )

        return self.s3.select_object_content(select_config)

    def create_presigned_url_put_object(
        self,
        object_key: str,
        content_type: str,
        acl: str = "private",
        expiration: int = 3600,
    ) -> str:
        """Generate presigned URL for PUT operation."""
        config = PresignedUrlConfig(
            bucket_name=self.bucket_name,
            object_name=object_key,
            client_method="put_object",
            content_type=content_type,
            acl=acl,
            expiration=expiration,
        )
        return self.s3.create_presigned_url(config)

    def create_presigned_url_get_object(
        self,
        object_key: str,
        expiration: int = 3600,
    ) -> str:
        """Generate presigned URL for GET operation."""
        config = PresignedUrlConfig(
            bucket_name=self.bucket_name,
            object_name=object_key,
            client_method="get_object",
            expiration=expiration,
        )
        return self.s3.create_presigned_url(config)

    def get_url_by_object_key(self, object_key: str, use_accelerate: bool = False) -> str | None:
        """Get public URL for object key."""
        if not object_key:
            return None
        return urljoin(self._get_base_url(use_accelerate=use_accelerate), object_key)

    def delete_object(self, object_key: str) -> bool:
        """Delete an object from S3 bucket.

        Args:
            object_key: The key of the object to delete

        Returns:
            bool: True if deletion was successful, False otherwise

        """
        return self.s3.delete_object(self.bucket_name, object_key)

    def delete_multiple_objects(self, object_keys: list[str]) -> dict:
        """Delete multiple objects from the bucket."""
        return self.s3.delete_objects(self.bucket_name, object_keys)

    def check_key_exists(self, object_key: str) -> bool:
        """Check if object key exists in bucket."""
        return bool(self.s3.head_object(self.bucket_name, object_key))

    def copy_object(
        self,
        source_key: str,
        dest_key: str,
        dest_bucket: str | None = None,
        acl: str = "private",
    ) -> CopyObjectResult:
        """Copy an object within the same bucket or to another bucket.

        Args:
            source_key: Source object key
            dest_key: Destination object key
            dest_bucket: Optional destination bucket (defaults to same bucket)
            acl: Access control list for the new object

        Returns:
            CopyObjectResult containing success status and destination URL

        """
        target_bucket = dest_bucket or self.bucket_name

        try:
            self.s3.copy_object(
                self.bucket_name,
                source_key,
                target_bucket,
                dest_key,
                acl,
            )

            dest_url = urljoin(
                self._get_base_url(bucket_name=target_bucket),
                dest_key,
            )

            return CopyObjectResult(
                success=True,
                url=dest_url,
                object_key=dest_key,
            )

        except Exception as ex:
            logger.exception(f"Failed to copy object from {
                         source_key} to {dest_key}: {ex!s}")
            return CopyObjectResult(
                success=False,
                url=None,
                object_key=dest_key,
                error_message=str(ex),
            )

    def get_object_tags(self, object_key: str) -> dict:
        """Get tags for an object."""
        return self.s3.get_object_tags(self.bucket_name, object_key)

    def put_object_tags(self, object_key: str, tags: dict[str, str]) -> dict:
        """Set tags for an object."""
        return self.s3.put_object_tags(self.bucket_name, object_key, tags)

    def get_object_metadata(
        self,
        object_key: str,
        version_id: str | None = None,
    ) -> dict:
        """Get detailed metadata for an object."""
        return self.s3.get_object_metadata(
            self.bucket_name,
            object_key,
            version_id,
        )

    def put_bucket_policy(self, policy: dict[str, Any]) -> None:
        """Put/Update bucket policy.

        Args:
            policy: Dictionary containing the bucket policy

        Example:
            ```python
            s3.put_bucket_policy({
                "Version": "2012-10-17",
                "Statement": [{
                    "Sid": "AllowCloudFrontServicePrincipal",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "cloudfront.amazonaws.com"
                    },
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                    "Condition": {
                        "StringEquals": {
                            "AWS:SourceArn": "arn:aws:cloudfront::ACCOUNT_ID:distribution/*"
                        }
                    }
                }]
            })
            ```

        Raises:
            Exception: If policy update fails

        """
        try:
            return self.s3.put_bucket_policy(self.bucket_name, json.dumps(policy))
        except Exception as e:
            logger.exception(f"Failed to put bucket policy: {e!s}")
            raise

    def get_bucket_policy(self) -> dict[str, Any]:
        """Get current bucket policy.

        Returns:
            Dict containing the bucket policy. Empty dict if no policy exists.

        Raises:
            Exception: If policy retrieval fails

        """
        try:
            policy = self.s3.get_bucket_policy(self.bucket_name)
            return json.loads(policy.get("Policy", "{}"))
        except Exception as e:
            logger.exception(f"Failed to get bucket policy: {e!s}")
            raise

    def add_lambda_notification(
        self,
        lambda_function_arn: str,
        events: list[str] | None = None,
        prefix: str | None = None,
        suffix: str | None = None,
        id: str | None = None,
    ) -> dict[str, Any]:
        """Add Lambda function notification configuration to S3 bucket.

        Args:
            lambda_function_arn: Lambda function ARN
            events: List of S3 events to trigger Lambda. Defaults to ['s3:ObjectCreated:*']
            prefix: Optional key prefix filter
            suffix: Optional key suffix filter
            id: Optional configuration ID

        Example:
            ```python
            # Trigger Lambda when PNG files are uploaded to 'images/' prefix
            s3.add_lambda_notification(
                lambda_function_arn="arn:aws:lambda:region:account:function:image-processor",
                events=['s3:ObjectCreated:Put'],
                prefix='images/',
                suffix='.png'
            )
            ```

        """
        from chainsaws.aws.lambda_client.lambda_client import LambdaAPI

        if not events:
            events = ["s3:ObjectCreated:*"]

        if not id:
            import uuid
            id = f"LambdaTrigger-{str(uuid.uuid4())[:8]}"

        try:
            lambda_api = LambdaAPI(self.config)
            try:
                lambda_api.add_permission(
                    function_name=lambda_function_arn,
                    statement_id=f"S3Trigger-{id}",
                    action="lambda:InvokeFunction",
                    principal="s3.amazonaws.com",
                    source_arn=f"arn:aws:s3:::{self.bucket_name}",
                )
            except Exception as e:
                if "ResourceConflictException" not in str(e):
                    raise

            config = {
                "LambdaFunctionArn": lambda_function_arn,
                "Events": events,
            }

            if prefix or suffix:
                filter_rules = []
                if prefix:
                    filter_rules.append({"Name": "prefix", "Value": prefix})
                if suffix:
                    filter_rules.append({"Name": "suffix", "Value": suffix})
                config["Filter"] = {"Key": {"FilterRules": filter_rules}}

            return self.s3.put_bucket_notification_configuration(
                self.bucket_name,
                {id: config},
            )

        except Exception as e:
            logger.exception(f"Failed to add Lambda notification: {e!s}")
            raise

    def remove_lambda_notification(
        self,
        id: str,
        lambda_function_arn: str | None = None,
        remove_permission: bool = True,
    ) -> None:
        """Remove Lambda function notification configuration.

        Args:
            id: Configuration ID to remove
            lambda_function_arn: Optional Lambda ARN (needed for permission removal)
            remove_permission: Whether to remove Lambda permission

        Example:
            ```python
            s3.remove_lambda_notification(
                id="LambdaTrigger-12345678",
                lambda_function_arn="arn:aws:lambda:region:account:function:image-processor"
            )
            ```

        """
        try:
            # Get current configuration
            current_config = self.s3.get_bucket_notification_configuration(
                self.bucket_name)

            # Remove specified configuration
            if id in current_config:
                del current_config[id]
                self.s3.put_bucket_notification_configuration(
                    self.bucket_name,
                    current_config,
                )

            # Remove Lambda permission if requested
            if remove_permission and lambda_function_arn:
                from chainsaws.aws.lambda_client.lambda_client import LambdaAPI
                lambda_api = LambdaAPI(self.config)
                try:
                    lambda_api.remove_permission(
                        function_name=lambda_function_arn,
                        statement_id=f"S3Trigger-{id}",
                    )
                except Exception as e:
                    if "ResourceNotFoundException" not in str(e):
                        logger.warning(
                            f"Failed to remove Lambda permission: {e!s}")

        except Exception as e:
            logger.exception(f"Failed to remove Lambda notification: {e!s}")
            raise

    def select_query(
        self,
        object_key: str,
        query: str,
        input_format: S3SelectFormat = S3SelectFormat.JSON,
        output_format: S3SelectFormat = S3SelectFormat.JSON,
        json_type: S3SelectJSONType = S3SelectJSONType.LINES,
        compression_type: str | None = None,
        csv_input_config: S3SelectCSVConfig | None = None,
        csv_output_config: S3SelectCSVConfig | None = None,
        max_rows: int | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Execute S3 Select query with advanced options.

        Args:
            object_key: S3 object key
            query: SQL query to execute
            input_format: Input format (JSON, CSV, PARQUET)
            output_format: Output format (JSON, CSV)
            json_type: JSON type for input (DOCUMENT or LINES)
            compression_type: Input compression type
            csv_input_config: CSV input configuration
            csv_output_config: CSV output configuration
            max_rows: Maximum number of rows to return

        Yields:
            Query results as dictionaries

        Example:
            ```python
            # Query JSON Lines
            results = s3.select_query(
                object_key="data/logs.jsonl",
                query="SELECT * FROM s3object s WHERE s.level = 'ERROR'",
                input_format=S3SelectFormat.JSON,
                json_type=S3SelectJSONType.LINES
            )

            # Query CSV with custom configuration
            results = s3.select_query(
                object_key="data/users.csv",
                query="SELECT name, email FROM s3object WHERE age > 25",
                input_format=S3SelectFormat.CSV,
                csv_input_config=S3SelectCSVConfig(
                    file_header_info="USE",
                    delimiter=","
                )
            )
            ```

        """
        input_serialization = {}
        output_serialization = {}

        # Configure input serialization
        if input_format == S3SelectFormat.JSON:
            input_serialization["JSON"] = {"Type": json_type}
        elif input_format == S3SelectFormat.CSV:
            csv_config = csv_input_config or S3SelectCSVConfig()
            input_serialization["CSV"] = csv_config.model_dump(
                exclude_none=True)
        elif input_format == S3SelectFormat.PARQUET:
            input_serialization["Parquet"] = {}

        # Configure output serialization
        if output_format == S3SelectFormat.JSON:
            output_serialization["JSON"] = {}
        elif output_format == S3SelectFormat.CSV:
            csv_config = csv_output_config or S3SelectCSVConfig()
            output_serialization["CSV"] = csv_config.model_dump(
                exclude_none=True)

        if compression_type:
            input_serialization["CompressionType"] = compression_type

        select_config = SelectObjectConfig(
            bucket_name=self.bucket_name,
            object_key=object_key,
            query=query,
            input_serialization=input_serialization,
            output_serialization=output_serialization,
        )

        row_count = 0
        for record in self.s3.select_object_content(select_config):
            if max_rows and row_count >= max_rows:
                break
            yield record
            row_count += 1

    def upload_jsonlines(
        self,
        object_key: str,
        items: list[dict[str, Any]],
        compression: str | None = None,
    ) -> str:
        """Upload items as JSON Lines format for efficient S3 Select queries.

        Args:
            object_key: Target object key
            items: List of dictionaries to upload
            compression: Optional compression (gzip, bzip2)

        Returns:
            URL of uploaded object

        Example:
            ```python
            url = s3.upload_jsonlines(
                "data/logs.jsonl",
                [
                    {"timestamp": "2023-01-01", "level": "INFO", "message": "Started"},
                    {"timestamp": "2023-01-01", "level": "ERROR", "message": "Failed"}
                ],
                compression="gzip"
            )
            ```

        """
        if not all(isinstance(item, dict) for item in items):
            msg = "All items must be dictionaries"
            raise ValueError(msg)

        # Convert to JSON Lines format
        json_lines = "\n".join(json.dumps(item) for item in items)
        data = json_lines.encode("utf-8")

        # Apply compression if requested
        if compression:
            if compression.lower() == "gzip":
                import gzip
                data = gzip.compress(data)
            elif compression.lower() == "bzip2":
                import bz2
                data = bz2.compress(data)
            else:
                msg = "Unsupported compression format"
                raise ValueError(msg)

        # Upload with appropriate content type
        content_type = "application/x-jsonlines"
        if compression:
            content_type += f"+{compression}"

        return self.upload_binary(object_key, data, content_type=content_type)

    def make_bucket_public(self) -> None:
        """Make the S3 bucket publicly accessible.
        This method:
        1. Disables bucket's public access block settings
        2. Updates the bucket policy to allow public access.

        Example:
            ```python
            s3 = S3API(bucket_name="my-bucket")
            s3.make_bucket_public()
            ```

        Raises:
            Exception: If any step of making the bucket public fails

        """
        try:
            logger.info(f"Disabling public access block for bucket '{
                        self.bucket_name}'")
            self.s3.put_public_access_block(
                self.bucket_name,
                {
                    "BlockPublicAcls": False,
                    "IgnorePublicAcls": False,
                    "BlockPublicPolicy": False,
                    "RestrictPublicBuckets": False,
                },
            )

            time.sleep(2)

            # Update bucket policy to allow public read access
            logger.info("Updating bucket policy to allow public access")
            public_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{self.bucket_name}/*",
                    },
                ],
            }
            self.s3.update_bucket_policy(public_policy)

            logger.info(f"Successfully made bucket '{
                        self.bucket_name}' public")
        except Exception as e:
            logger.exception(f"Failed to make bucket public: {e!s}")
            raise

    def make_bucket_private(self) -> None:
        """Make the S3 bucket private.
        This method:
        1. Removes any bucket policy
        2. Enables bucket's public access block settings.

        Example:
            ```python
            s3 = S3API(bucket_name="my-bucket")
            s3.make_bucket_private()
            ```

        Raises:
            Exception: If any step of making the bucket private fails

        """
        try:
            logger.info(f"Removing bucket policy from '{self.bucket_name}'")
            self.s3.delete_bucket_policy(self.bucket_name)

            logger.info(f"Enabling public access block for bucket '{
                        self.bucket_name}'")
            self.s3.put_public_access_block(
                self.bucket_name,
                {
                    "BlockPublicAcls": True,
                    "IgnorePublicAcls": True,
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True,
                },
            )

            logger.info(f"Successfully made bucket '{
                        self.bucket_name}' private")
        except Exception as e:
            logger.exception(f"Failed to make bucket private: {e!s}")
            raise
