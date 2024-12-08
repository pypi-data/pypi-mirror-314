"""DynamoDB API wrapper for simplified table operations with partition management."""

from chainsaws.aws.dynamodb.dynamodb import DynamoDBAPI
from chainsaws.aws.dynamodb.dynamodb_exception import (
    BatchOperationError,
    DynamoDBError,
    DynamoDBPartitionError,
    PartitionNotFoundError,
)
from chainsaws.aws.dynamodb.dynamodb_models import (
    DynamoDBAPIConfig,
    DynamoIndex,
    DynamoModel,
    PartitionIndex,
    PartitionMap,
    PartitionMapConfig,
)

__all__ = [
    "BatchOperationError",
    "DynamoDBAPI",
    "DynamoDBAPIConfig",
    "DynamoDBError",
    "DynamoDBPartitionError",
    "DynamoIndex",
    "DynamoModel",
    "PartitionIndex",
    "PartitionMap",
    "PartitionMapConfig",
    "PartitionNotFoundError",
]
