import json
import logging
import tempfile
from typing import Any, BinaryIO

import boto3
from botocore.exceptions import ClientError
from botocore.response import StreamingBody

from chainsaws.aws.s3.s3_models import (
    BucketACL,
    BucketConfig,
    FileUploadConfig,
    ObjectListConfig,
    PresignedUrlConfig,
    S3APIConfig,
    SelectObjectConfig,
)

logger = logging.getLogger(__name__)


class S3:
    def __init__(
        self,
        boto3_session: boto3.Session,
        bucket_name: str,
        config: S3APIConfig | None = None,
    ) -> None:
        self.bucket_name = bucket_name
        self.config = config or S3APIConfig()
        self.region: str = self.config.region
        self.client: boto3.client = boto3_session.client(
            service_name="s3", region_name=self.config.region)
        self.resource: boto3.resource = boto3_session.resource(
            service_name="s3", region_name=self.config.region)

    def init_bucket(self, config: BucketConfig) -> None:
        """Initialize a bucket, creating it if it doesn't exist.

        Args:
            config: Bucket configuration parameters

        Note:
            If bucket already exists, a warning will be logged

        """
        try:
            try:
                self.client.head_bucket(Bucket=self.bucket_name)
                logger.warning(
                    f"[S3.init_bucket] Bucket '{
                        self.bucket_name}' already exists",
                )
                return
            except ClientError as e:
                error_code = int(e.response["Error"]["Code"])
                if error_code == 404:  # If bucket does not exist
                    self.create_bucket(config)
                    logger.info(
                        f"[S3.init_bucket] Successfully created bucket '{
                            self.bucket_name}'",
                    )

                    if config.use_accelerate:
                        self.client.put_bucket_accelerate_configuration(
                            Bucket=self.bucket_name,
                            AccelerateConfiguration={"Status": "Enabled"},
                        )
                        logger.info(
                            f"[S3.init_bucket] S3 Transfer Acceleration enabled for bucket '{
                                self.bucket_name}'",
                        )
                else:
                    raise

        except Exception as ex:
            logger.exception(f"[S3.init_bucket] Failed to initialize bucket '{
                         self.bucket_name}': {ex!s}")
            raise

    def create_bucket(self, config: BucketConfig) -> dict:
        """Create a new S3 bucket."""
        return self.client.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration={"LocationConstraint": self.region},
            ACL=self.config.acl,
        )

    def update_bucket_acl(self, acl: BucketACL) -> None:
        """Update the ACL for the S3 bucket.

        Args:
            acl: The ACL to apply to the bucket (e.g., 'private', 'public-read').

        """
        try:
            self.client.put_bucket_acl(
                Bucket=self.bucket_name,
                ACL=acl,
            )
            logger.info(f"[S3.update_bucket_acl] Updated ACL for bucket '{
                        self.bucket_name}' to '{acl}'")
        except Exception as ex:
            logger.exception(f"[S3.update_bucket_acl] Failed to update ACL for bucket '{
                         self.bucket_name}': {ex!s}")
            raise

    def update_bucket_policy(self, policy: str | dict) -> None:
        """Update the bucket policy.

        Args:
            policy: The JSON policy to apply to the bucket.

        """
        bucket_policy = policy
        if isinstance(policy, dict):
            bucket_policy = json.dumps(policy)

        try:
            self.client.put_bucket_policy(
                Bucket=self.bucket_name,
                Policy=bucket_policy,
            )
            logger.info(f"[S3.update_bucket_policy] Updated policy for bucket '{
                        self.bucket_name}'")
        except Exception as ex:
            logger.exception(f"[S3.update_bucket_policy] Failed to update policy for bucket '{
                         self.bucket_name}': {ex!s}")
            raise

    def delete_bucket_policy(self, bucket_name: str) -> None:
        """Delete bucket policy."""
        try:
            self.client.delete_bucket_policy(Bucket=bucket_name)
            logger.info(f"[S3.delete_bucket_policy] Deleted policy for bucket '{
                        bucket_name}'")
        except Exception as ex:
            logger.exception(
                f"[S3.delete_bucket_policy] Failed to delete bucket policy: {ex!s}")
            raise

    def upload_binary(self, bucket_name: str, file_name: str, binary: bytes) -> None:
        """Upload binary data to S3."""
        with tempfile.TemporaryFile() as tmp:
            tmp.write(binary)
            tmp.seek(0)
            self.client.upload_fileobj(tmp, bucket_name, file_name)

    def delete_binary(self, bucket_name: str, file_name: str) -> dict:
        """Delete an object from S3."""
        return self.resource.Object(bucket_name, file_name).delete()

    def download_binary(self, bucket_name: str, file_name: str) -> bytes:
        """Download binary data from S3."""
        with tempfile.NamedTemporaryFile() as data:
            self.client.download_fileobj(bucket_name, file_name, data)
            data.seek(0)
            return data.read()

    def upload_file(self, config: FileUploadConfig, file_bytes: bytes | BinaryIO) -> dict:
        """Upload a file to S3 with content type consideration."""
        return self.client.put_object(
            Bucket=self.bucket_name,
            Key=config.file_name,
            Body=file_bytes,
            ContentType=config.content_type,
        )

    def select_object_content(self, config: SelectObjectConfig) -> StreamingBody:
        """Execute S3 Select query."""
        return self.client.select_object_content(
            Bucket=self.bucket_name,
            Key=config.object_key,
            RequestProgress={"Enabled": True},
            Expression=config.query,
            ExpressionType="SQL",
            InputSerialization=config.input_serialization,
            OutputSerialization=config.output_serialization,
        )

    def list_objects_v2(self, config: ObjectListConfig) -> dict:
        """List objects in a bucket with pagination."""
        request_payload = {
            "Bucket": self.bucket_name,
            "Prefix": config.prefix,
            "MaxKeys": config.limit,
        }
        if config.continuation_token:
            request_payload["ContinuationToken"] = config.continuation_token
        if config.start_after:
            request_payload["StartAfter"] = config.start_after

        return self.client.list_objects_v2(**request_payload)

    def delete_object(self, bucket_name: str, object_key: str) -> bool:
        """Delete an object from S3 bucket.

        Args:
            bucket_name: Name of the S3 bucket
            object_key: The key of the object to delete

        Returns:
            bool: True if deletion was successful, False otherwise

        """
        try:
            self.client.delete_object(
                Bucket=bucket_name,
                Key=object_key,
            )
            return True
        except Exception as ex:
            logger.exception(
                f"[S3.delete_object] Failed to delete object: {ex!s}")
            return False

    def delete_objects(self, bucket_name: str, object_keys: list[str]) -> dict:
        """Delete multiple objects from S3 bucket in a single request.

        Args:
            bucket_name: Name of the S3 bucket
            object_keys: List of object keys to delete

        Returns:
            dict: Response containing successful and failed deletions

        """
        objects = [{"Key": key} for key in object_keys]
        try:
            return self.client.delete_objects(
                Bucket=bucket_name,
                Delete={
                    "Objects": objects,
                    "Quiet": False,
                },
            )
        except Exception as ex:
            logger.exception(
                f"[S3.delete_objects] Failed to delete objects: {ex!s}")
            raise

    def create_presigned_url(self, config: PresignedUrlConfig) -> str:
        """Generate a presigned URL for S3 operations."""
        params = {
            "Bucket": self.bucket_name,
            "Key": config.object_name,
        }
        if config.content_type:
            params["ContentType"] = config.content_type
        if config.acl:
            params["ACL"] = config.acl

        return self.client.generate_presigned_url(
            config.client_method,
            Params=params,
            ExpiresIn=config.expiration,
        )

    def head_object(self, bucket_name: str, key: str) -> dict | None:
        """Check if an object exists in S3."""
        try:
            return self.client.head_object(Bucket=bucket_name, Key=key)
        except Exception:
            return None

    def get_object_tags(self, bucket_name: str, object_key: str) -> dict:
        """Get tags for an S3 object.

        Args:
            bucket_name: Name of the S3 bucket
            object_key: The key of the object

        """
        try:
            return self.client.get_object_tagging(
                Bucket=bucket_name,
                Key=object_key,
            )
        except Exception as ex:
            logger.exception(
                f"[S3.get_object_tags] Failed to get object tags: {ex!s}")
            raise

    def put_object_tags(
        self,
        bucket_name: str,
        object_key: str,
        tags: dict[str, str],
    ) -> dict:
        """Set tags for an S3 object.

        Args:
            bucket_name: Name of the S3 bucket
            object_key: The key of the object
            tags: Dictionary of tag key-value pairs

        """
        tag_set = [{"Key": k, "Value": v} for k, v in tags.items()]
        try:
            return self.client.put_object_tagging(
                Bucket=bucket_name,
                Key=object_key,
                Tagging={"TagSet": tag_set},
            )
        except Exception as ex:
            logger.exception(
                f"[S3.put_object_tags] Failed to put object tags: {ex!s}")
            raise

    def copy_object(
        self,
        source_bucket: str,
        source_key: str,
        dest_bucket: str,
        dest_key: str,
        acl: str = "private",
    ) -> dict:
        """Copy an object from one bucket/location to another.

        Args:
            source_bucket: Source bucket name
            source_key: Source object key
            dest_bucket: Destination bucket name
            dest_key: Destination object key
            acl: Access control list for the new object

        """
        try:
            return self.client.copy_object(
                CopySource={"Bucket": source_bucket, "Key": source_key},
                Bucket=dest_bucket,
                Key=dest_key,
                ACL=acl,
            )
        except Exception as ex:
            logger.exception(f"[S3.copy_object] Failed to copy object: {ex!s}")
            raise

    def get_object_metadata(
        self,
        bucket_name: str,
        object_key: str,
        version_id: str | None = None,
    ) -> dict:
        """Get detailed metadata for an S3 object.

        Args:
            bucket_name: Name of the S3 bucket
            object_key: The key of the object
            version_id: Optional version ID for versioned objects

        """
        try:
            params = {
                "Bucket": bucket_name,
                "Key": object_key,
            }
            if version_id:
                params["VersionId"] = version_id

            response = self.client.head_object(**params)
            return {
                "content_length": response.get("ContentLength"),
                "content_type": response.get("ContentType"),
                "last_modified": response.get("LastModified"),
                "etag": response.get("ETag"),
                "version_id": response.get("VersionId"),
                "metadata": response.get("Metadata", {}),
                "storage_class": response.get("StorageClass"),
            }
        except Exception as ex:
            logger.exception(
                f"[S3.get_object_metadata] Failed to get object metadata: {ex!s}")
            raise

    def create_multipart_upload(
        self,
        bucket_name: str,
        object_key: str,
        content_type: str | None = None,
        acl: str = "private",
    ) -> str:
        """Initialize multipart upload.

        Args:
            bucket_name: Name of the S3 bucket
            object_key: The key of the object
            content_type: Optional content type of the file
            acl: Access control list for the object

        Returns:
            str: Upload ID for the multipart upload

        """
        params = {
            "Bucket": bucket_name,
            "Key": object_key,
            "ACL": acl,
        }
        if content_type:
            params["ContentType"] = content_type

        try:
            response = self.client.create_multipart_upload(**params)
            return response["UploadId"]
        except Exception as ex:
            logger.exception(
                f"[S3.create_multipart_upload] Failed to create multipart upload: {ex!s}")
            raise

    def upload_part(
        self,
        bucket_name: str,
        object_key: str,
        upload_id: str,
        part_number: int,
        body: bytes | BinaryIO,
    ) -> dict:
        """Upload a part in multipart upload.

        Args:
            bucket_name: Name of the S3 bucket
            object_key: The key of the object
            upload_id: Upload ID from create_multipart_upload
            part_number: Part number (1 to 10000)
            body: The data to upload

        """
        try:
            response = self.client.upload_part(
                Bucket=bucket_name,
                Key=object_key,
                UploadId=upload_id,
                PartNumber=part_number,
                Body=body,
            )
            return {
                "PartNumber": part_number,
                "ETag": response["ETag"],
            }
        except Exception as ex:
            logger.exception(f"[S3.upload_part] Failed to upload part {
                         part_number}: {ex!s}")
            raise

    def complete_multipart_upload(
        self,
        bucket_name: str,
        object_key: str,
        upload_id: str,
        parts: list[dict],
    ) -> dict:
        """Complete a multipart upload.

        Args:
            bucket_name: Name of the S3 bucket
            object_key: The key of the object
            upload_id: Upload ID from create_multipart_upload
            parts: List of {'PartNumber': int, 'ETag': str} dicts

        """
        try:
            sorted_parts = sorted(parts, key=lambda x: x["PartNumber"])
            formatted_parts = [
                {
                    "PartNumber": part["PartNumber"],
                    "ETag": part["ETag"].strip('"'),
                }
                for part in sorted_parts
            ]

            return self.client.complete_multipart_upload(
                Bucket=bucket_name,
                Key=object_key,
                UploadId=upload_id,
                MultipartUpload={
                    "Parts": formatted_parts,
                },
            )
        except Exception as ex:
            logger.exception(
                f"[S3.complete_multipart_upload] Failed to complete multipart upload: {ex!s}")
            raise

    def abort_multipart_upload(
        self,
        bucket_name: str,
        object_key: str,
        upload_id: str,
    ) -> None:
        """Abort a multipart upload.

        Args:
            bucket_name: Name of the S3 bucket
            object_key: The key of the object
            upload_id: Upload ID to abort

        """
        try:
            self.client.abort_multipart_upload(
                Bucket=bucket_name,
                Key=object_key,
                UploadId=upload_id,
            )
        except Exception as ex:
            logger.exception(
                f"[S3.abort_multipart_upload] Failed to abort multipart upload: {ex!s}")
            raise

    def put_bucket_policy(self, bucket_name: str, policy: str) -> None:
        """Put bucket policy."""
        try:
            return self.client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=policy,
            )
        except self.client.exceptions.NoSuchBucket as e:
            msg = f"Bucket {bucket_name} does not exist"
            raise ValueError(msg) from e
        except Exception:
            raise

    def get_bucket_policy(self, bucket_name: str) -> dict[str, Any]:
        """Get bucket policy."""
        try:
            return self.client.get_bucket_policy(Bucket=bucket_name)
        except self.client.exceptions.NoSuchBucketPolicy:
            return {"Policy": "{}"}
        except self.client.exceptions.NoSuchBucket as e:
            msg = f"Bucket {bucket_name} does not exist"
            raise ValueError(msg) from e
        except Exception as ex:
            logger.exception(str(ex))
            raise

    def put_bucket_notification_configuration(
        self,
        bucket_name: str,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        """Put bucket notification configuration."""
        try:
            return self.client.put_bucket_notification_configuration(
                Bucket=bucket_name,
                NotificationConfiguration={
                    "LambdaFunctionConfigurations": [config]},
            )
        except Exception as ex:
            logger.exception(
                f"[S3.put_bucket_notification_configuration] Failed to set notification: {ex!s}")
            raise

    def get_bucket_notification_configuration(
        self,
        bucket_name: str,
    ) -> dict[str, Any]:
        """Get bucket notification configuration."""
        try:
            response = self.client.get_bucket_notification_configuration(
                Bucket=bucket_name,
            )
            return {
                config.get("Id"): config
                for config in response.get("LambdaFunctionConfigurations", [])
            }
        except Exception as ex:
            logger.exception(
                f"[S3.get_bucket_notification_configuration] Failed to get notification: {ex!s}")
            raise

    def put_public_access_block(
        self,
        bucket_name: str,
        public_access_block_configuration: dict[str, bool],
    ) -> None:
        """Configure public access block settings for the bucket.

        Args:
            bucket_name: Name of the S3 bucket
            public_access_block_configuration: Dictionary containing the following boolean settings:
                - BlockPublicAcls: Block public access to buckets and objects granted through new ACLs
                - IgnorePublicAcls: Ignore public ACLs on buckets and objects
                - BlockPublicPolicy: Block public bucket policies
                - RestrictPublicBuckets: Block public and cross-account access to buckets with public policies

        Example:
            ```python
            s3.put_public_access_block(
                bucket_name="my-bucket",
                public_access_block_configuration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )
            ```

        """
        try:
            self.client.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration=public_access_block_configuration,
            )
            logger.info(
                f"[S3.put_public_access_block] Updated public access block configuration for bucket '{
                    bucket_name}'",
            )
        except Exception as ex:
            logger.exception(
                f"[S3.put_public_access_block] Failed to update public access block configuration: {
                    ex!s}",
            )
            raise
