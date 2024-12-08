# AWS S3 High-Level API

A comprehensive Python interface for AWS S3 (Simple Storage Service) that provides an easy-to-use, type-safe API with advanced features including bulk operations, S3 Select support, and presigned URLs.

## Features

- 🚀 High-level abstraction over boto3
- 📦 Bulk upload/download with parallel processing
- 🔍 S3 Select query support with multiple formats
- 🔐 Presigned URL generation
- 📋 Object tagging and metadata management
- 🔄 Object copying and moving
- ✨ Type safety with Pydantic models
- 📝 Comprehensive content type support

## Installation

```bash
pip install chainsaws
```

## Quick Start

```python
from chainsaws.aws.s3 import S3API, ContentType

# Initialize API
s3 = S3API(bucket_name="my-bucket")

# Upload file
result = s3.upload_file_and_return_url(
    file_bytes=b"Hello, World!",
    extension="txt",
    content_type=ContentType.TEXT
)
print(f"File uploaded: {result.url}")
```

## Core Features

### File Upload

```python
# Simple upload
s3.upload_binary("path/to/file.txt", b"Hello, World!")

# Upload with metadata
result = s3.upload_file_and_return_url(
    file_bytes=image_data,
    extension="png",
    content_type=ContentType.PNG
)
```

### Bulk Operations

```python
from chainsaws.aws.s3 import BulkUploadItem, ContentType

# Prepare items for bulk upload
items = [
    BulkUploadItem(
        object_key="images/photo1.jpg",
        data=photo1_bytes,
        content_type=ContentType.JPEG
    ),
    BulkUploadItem(
        object_key="documents/doc1.pdf",
        data=pdf_bytes,
        content_type=ContentType.PDF
    )
]

# Perform bulk upload with parallel processing
result = s3.bulk_upload(items, max_workers=4)

# Check results
for key, url in result.successful.items():
    print(f"Successfully uploaded {key} to {url}")
for key, error in result.failed.items():
    print(f"Failed to upload {key}: {error}")
```

### S3 Select Operations

```python
# Upload data for S3 Select
s3.upload_items_for_select(
    "data/users.json",
    [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25}
    ]
)

# Execute S3 Select query
results = s3.select(
    object_key="data/users.json",
    query="SELECT s.name, s.age FROM s3object s WHERE s.age > 25"
)

# With pagination
from chainsaws.aws.s3.s3_utils import make_query
query = make_query(
    base_query="SELECT * FROM s3object s",
    idx_offset=100,
    limit=50
)
```

### Presigned URLs

```python
# Generate upload URL
upload_url = s3.create_presigned_url_put_object(
    object_key="uploads/file.pdf",
    content_type=ContentType.PDF,
    expiration=3600
)

# Generate download URL
download_url = s3.create_presigned_url_get_object(
    object_key="documents/report.pdf",
    expiration=3600
)
```

### Object Management

```python
# Copy objects
result = s3.copy_object(
    source_key="original/file.txt",
    dest_key="backup/file.txt"
)

# Delete objects
s3.delete_object("path/to/file.txt")
s3.delete_multiple_objects(["file1.txt", "file2.txt"])

# Check existence
exists = s3.check_key_exists("path/to/file.txt")

# Get/Set tags
tags = s3.get_object_tags("path/to/file.txt")
s3.put_object_tags("path/to/file.txt", {"env": "prod"})

# Get metadata
metadata = s3.get_object_metadata("path/to/file.txt")
```

## Advanced Configuration

```python
from chainsaws.aws.s3 import S3API, S3APIConfig

s3 = S3API(
    bucket_name="my-bucket",
    config=S3APIConfig(
        region="ap-northeast-2",
        credentials={
            "aws_access_key_id": "YOUR_KEY",
            "aws_secret_access_key": "YOUR_SECRET"
        },
        acl="private"
    )
)
```

## Content Types

The API includes comprehensive MIME type support through the `ContentType` enum:

- Application: JSON, PDF, ZIP, EXCEL, WORD, etc.
- Text: PLAIN, HTML, CSS, CSV, XML
- Image: JPEG, PNG, GIF, SVG, WEBP
- Audio: MP3, WAV, OGG
- Video: MP4, MPEG, WEBM

```python
from chainsaws.aws.s3 import ContentType

# Automatic content type detection
content_type = ContentType.from_extension("jpg")  # Returns ContentType.JPEG
```

## Best Practices

1. Use bulk operations for multiple files
2. Implement proper error handling
3. Set appropriate content types
4. Use presigned URLs for secure temporary access
5. Implement pagination for large object lists
6. Use S3 Select for efficient data querying

## Error Handling

```python
try:
    result = s3.upload_file_and_return_url(
        file_bytes=data,
        extension="pdf"
    )
except Exception as e:
    logger.error(f"Upload failed: {str(e)}")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
