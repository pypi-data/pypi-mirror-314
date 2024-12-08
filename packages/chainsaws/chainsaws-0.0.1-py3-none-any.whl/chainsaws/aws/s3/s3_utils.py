import re

from pydantic import BaseModel, Field

from chainsaws.aws.s3.s3_exception import InvalidBucketNameError


class S3QueryParams(BaseModel):
    """Parameters for S3 Select query modification."""

    base_query: str = Field(..., description="Base SQL query to be modified")
    idx_offset: int = Field(
        default=0, ge=0, description="Starting index for pagination")
    limit: int = Field(default=100, gt=0, le=1000,
                       description="Maximum number of records to return")


def validate_bucket_name(bucket_name: str) -> None:
    """Validate an S3 bucket name according to AWS naming rules.

    Args:
        bucket_name: The name of the S3 bucket to validate.

    Raises:
        InvalidBucketNameError: If the bucket name is invalid.

    """
    if not (3 <= len(bucket_name) <= 63):
        msg = "Bucket name must be between 3 and 63 characters long."
        raise InvalidBucketNameError(
            msg)

    if not re.match(r"^[a-z0-9][a-z0-9.-]*[a-z0-9]$", bucket_name):
        msg = "Bucket name can only contain lowercase letters, numbers, dots (.), and hyphens (-), and must start and end with a letter or number."
        raise InvalidBucketNameError(
            msg)

    if ".." in bucket_name:
        msg = "Bucket name must not contain two adjacent periods."
        raise InvalidBucketNameError(
            msg)

    if re.match(r"^\d+\.\d+\.\d+\.\d+$", bucket_name):
        msg = "Bucket name must not be formatted as an IP address."
        raise InvalidBucketNameError(
            msg)

    if bucket_name.startswith(("xn--", "sthree-", "sthree-configurator", "amzn-s3-demo-")):
        msg = "Bucket name must not start with reserved prefixes."
        raise InvalidBucketNameError(
            msg)

    if bucket_name.endswith(("-s3alias", "--ol-s3", ".mrap", "--x-s3")):
        msg = "Bucket name must not end with reserved suffixes."
        raise InvalidBucketNameError(
            msg)

    if "." in bucket_name:
        msg = "Buckets used with Amazon S3 Transfer Acceleration can't have dots (.) in their names."
        raise InvalidBucketNameError(
            msg)


def make_query(base_query: str, idx_offset: int = 0, limit: int = 100) -> str:
    """Modifies an S3 Select query to include pagination using _idx field.

    Args:
        base_query: Base SQL query to modify
        idx_offset: Starting index for pagination
        limit: Maximum number of records to return

    Returns:
        str: Modified query with pagination

    Raises:
        ValueError: If the query doesn't contain a FROM clause

    """
    # Convert query to uppercase for consistent comparison
    query_upper = base_query.upper()

    has_where = "WHERE" in query_upper

    if "FROM" not in query_upper:
        msg = "Invalid SQL query. 'FROM' clause not found."
        raise ValueError(msg)

    if has_where:
        modified_query = f"{base_query} AND s._idx >= {
            idx_offset} LIMIT {limit}"
    else:
        from_idx = query_upper.index("FROM")
        before_from = base_query[:from_idx]
        after_from = base_query[from_idx + 4:].strip()
        modified_query = f"{before_from} FROM {
            after_from} WHERE s._idx >= {idx_offset} LIMIT {limit}"

    return modified_query
