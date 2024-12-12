from typing import (
    Any,
    ClassVar,
    Literal,
    Self,
    TypedDict,
    TypeGuard,
    Union,
    Optional,
)

from pydantic import BaseModel, Field

from chainsaws.aws.shared.config import APIConfig


class KeySchemaElement(BaseModel):
    """DynamoDB key schema element."""

    AttributeName: str = Field(..., description="Name of the key attribute")
    KeyType: Literal["HASH",
                     "RANGE"] = Field(..., description="Type of the key")


class AttributeDefinitionElement(BaseModel):
    """DynamoDB attribute definition element."""

    AttributeName: str = Field(..., description="Name of the attribute")
    AttributeType: Literal["S", "N",
                           "B"] = Field(..., description="Type of the attribute")


class StreamSpecificationElement(BaseModel):
    """DynamoDB stream specification."""

    StreamEnabled: bool = Field(
        True, description="Enable/disable DynamoDB Streams")
    StreamViewType: Literal["NEW_IMAGE", "OLD_IMAGE", "NEW_AND_OLD_IMAGES", "KEYS_ONLY"] = Field(
        "NEW_AND_OLD_IMAGES",
        description="Type of information captured in the stream",
    )


class CreateTableRequest(BaseModel):
    """Request model for creating a DynamoDB table."""

    TableName: str = Field(..., description="Name of the table to create")
    AttributeDefinitions: list[AttributeDefinitionElement] = Field(
        ...,
        description="List of attributes that describe the key schema",
    )
    KeySchema: list[KeySchemaElement] = Field(
        ...,
        description="List of key schema elements",
    )
    BillingMode: Literal["PROVISIONED", "PAY_PER_REQUEST"] = Field(
        "PAY_PER_REQUEST",
        description="Billing mode for the table",
    )
    StreamSpecification: StreamSpecificationElement | None = Field(
        None,
        description="DynamoDB Streams configuration",
    )

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "TableName": "users_table",
                "AttributeDefinitions": [
                    {"AttributeName": "user_id", "AttributeType": "S"},
                    {"AttributeName": "email", "AttributeType": "S"},
                ],
                "KeySchema": [
                    {"AttributeName": "user_id", "KeyType": "HASH"},
                    {"AttributeName": "email", "KeyType": "RANGE"},
                ],
                "BillingMode": "PAY_PER_REQUEST",
                "StreamSpecification": {
                    "StreamEnabled": True,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
            },
        }


class PartitionIndex(BaseModel):
    """Configuration for a partition index."""

    pk: str = Field(..., description="Primary key field for the index")
    sk: str = Field(..., description="Sort key field for the index")

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "pk": "user_id",
                "sk": "email",
            },
        }


class PartitionMapConfig(BaseModel):
    """Configuration for a single partition in the partition map."""

    pk: str = Field(..., description="Primary key field")
    sk: str = Field(..., description="Sort key field")
    uks: list[str] | None = Field(
        default_factory=list,
        description="List of unique key fields",
    )
    indexes: list[PartitionIndex] | None = Field(
        default_factory=list,
        description="List of secondary indexes",
    )

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "pk": "user_id",
                "sk": "email",
                "uks": ["email", "phone"],
                "indexes": [
                    {"pk": "email", "sk": "user_id"},
                    {"pk": "phone", "sk": "user_id"},
                ],
            },
        }


class PartitionMap(BaseModel):
    """Complete partition map configuration."""

    partitions: dict[str, PartitionMapConfig] = Field(
        ...,
        description="Mapping of partition names to their configurations",
    )

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "partitions": {
                    "users": {
                        "pk": "user_id",
                        "sk": "email",
                        "uks": ["email"],
                        "indexes": [
                            {"pk": "email", "sk": "user_id"},
                        ],
                    },
                    "orders": {
                        "pk": "order_id",
                        "sk": "user_id",
                        "indexes": [
                            {"pk": "user_id", "sk": "order_date"},
                        ],
                    },
                },
            },
        }


class DynamoDBConfig(BaseModel):
    """DynamoDB configuration settings."""

    region: str = Field(
        "ap-northeast-2", description="AWS region for the DynamoDB table")
    max_pool_connections: int = Field(
        100,
        description="Maximum number of connections in the connection pool",
        ge=1,
        le=1000,
    )

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "table_name": "users_table",
                "region": "ap-northeast-2",
                "max_pool_connections": 100,
            },
        }


class DynamoDBAPIConfig(APIConfig):
    """DynamoDB API configuration."""

    max_pool_connections: int = Field(
        100,
        description="Maximum number of connections in the connection pool",
        ge=1,
        le=1000,
    )

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "credentials": {
                    "aws_access_key_id": "AKIAXXXXXXXXXXXXXXXX",
                    "aws_secret_access_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "region_name": "ap-northeast-2",
                    "profile_name": "default",
                },
                "region": "ap-northeast-2",
                "max_pool_connections": 100,
            },
        }


# Filter condition types
FilterCondition = Literal[
    "eq", "neq", "lte", "lt", "gte", "gt", "btw",
    "stw", "is_in", "contains", "exist", "not_exist",
]


class FilterDict(TypedDict):
    """Single filter condition."""

    field: str
    value: Any
    condition: FilterCondition


class RecursiveFilterBase(TypedDict):
    """Base for recursive filter operations."""

    field: str
    value: Any
    condition: FilterCondition


class RecursiveFilterNode(TypedDict):
    """Node in recursive filter tree."""

    left: Union["RecursiveFilterNode", RecursiveFilterBase]
    operation: Literal["and", "or"]
    right: Union["RecursiveFilterNode", RecursiveFilterBase]


class DynamoIndex:
    """Index configuration for DynamoDB models."""

    def __init__(self, pk: str, sk: str) -> None:
        self.pk = pk
        self.sk = sk


class DynamoDBPartitionConfig:
    """Partition configuration for DynamoDB models."""

    def __init__(
        self,
        partition: str,
        pk_field: str,
        sk_field: str,
        indexes: list[DynamoIndex] | None = None,
    ) -> None:
        self.partition = partition
        self.pk_field = pk_field
        self.sk_field = sk_field
        self.indexes = indexes or []


class DynamoModel(BaseModel):
    """Base model for DynamoDB models with partition configuration."""

    # System fields with aliases
    id: Optional[str] = Field(default=None, exclude=True, alias="_id")
    crt: Optional[int] = Field(default=None, exclude=True, alias="_crt")
    ptn: Optional[str] = Field(default=None, exclude=True, alias="_ptn")

    # Class variables for configuration
    _partition: ClassVar[str]
    _pk: ClassVar[str]
    _sk: ClassVar[str]
    _indexes: ClassVar[list[DynamoIndex]] = []

    # TTL field
    _ttl: ClassVar[Optional[float]] = None

    class Config:
        populate_by_name = True
        alias_generator = None

    @classmethod
    def get_partition_config(cls) -> DynamoDBPartitionConfig:
        """Get partition configuration for this model."""
        return DynamoDBPartitionConfig(
            partition=cls._partition,
            pk_field=cls._pk,
            sk_field=cls._sk,
            indexes=cls._indexes,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary, excluding system fields."""
        return self.model_dump()

    def to_json(self) -> str:
        """Convert model to JSON string."""
        return self.model_dump_json(indent=4)

    def to_yaml(self) -> str:
        """Convert model to YAML string."""
        return self.model_dump_yaml(indent=4)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Create model instance from dictionary, preserving system fields."""
        # Extract system fields with their DynamoDB names
        system_fields = {
            "_id": data.get("_id"),
            "_crt": data.get("_crt"),
            "_ptn": data.get("_ptn"),
        }

        # Create instance with regular fields
        instance = cls.model_validate(data, from_attributes=True)

        # Set system fields using their model names
        if system_fields["_id"] is not None:
            instance.id = system_fields["_id"]
        if system_fields["_crt"] is not None:
            instance.crt = system_fields["_crt"]
        if system_fields["_ptn"] is not None:
            instance.ptn = system_fields["_ptn"]

        return instance

    @property
    def _id(self) -> str | None:
        """Compatibility property for _id."""
        return self.id

    @property
    def _crt(self) -> int | None:
        """Compatibility property for _crt."""
        return self.crt

    @property
    def _ptn(self) -> str | None:
        """Compatibility property for _ptn."""
        return self.ptn

    @staticmethod
    def is_dynamo_model(model: type[Any]) -> TypeGuard[type["DynamoModel"]]:
        """Check if a class is a valid DynamoModel subclass.

        Args:
            model: Class to check

        Returns:
            bool: True if the class is a valid DynamoModel subclass

        """
        return (isinstance(model, type) and
                issubclass(model, DynamoModel) and
                all(hasattr(model, attr) for attr in ["_partition", "_pk", "_sk"]))
