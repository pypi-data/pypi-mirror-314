from typing import Any, ClassVar, Literal

from pydantic import BaseModel, Field

from chainsaws.aws.shared.config import APIConfig


class Route53APIConfig(APIConfig):
    """Configuration for Route53 client."""



class DNSRecordSet(BaseModel):
    """DNS record set configuration."""

    name: str = Field(...,
                      description="DNS record name (e.g., 'example.com.')")
    type: Literal["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SOA", "SRV", "PTR"] = Field(
        ...,
        description="DNS record type",
    )
    ttl: int = Field(300, description="Time to live in seconds")
    records: list[str] = Field(..., description="Record values")

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "name": "api.example.com.",
                "type": "A",
                "ttl": 300,
                "records": ["192.0.2.1"],
            },
        }


class DNSRecordChange(BaseModel):
    """DNS record change request."""

    action: Literal["CREATE", "DELETE",
                    "UPSERT"] = Field(..., description="Change action")
    record_set: DNSRecordSet = Field(..., description="Record set to change")


class HealthCheckConfig(BaseModel):
    """Health check configuration."""

    ip_address: str | None = Field(None, description="IP address to check")
    port: int | None = Field(
        None, description="Port to check", gt=1, le=65535)
    type: Literal["HTTP", "HTTPS",
                  "TCP"] = Field(..., description="Health check type")
    resource_path: str | None = Field(
        None, description="Resource path for HTTP(S) checks")
    fqdn: str | None = Field(
        None, description="Fully qualified domain name to check")
    search_string: str | None = Field(
        None, description="String to search for in response")
    request_interval: int = Field(
        30, description="Check interval in seconds", gt=10, le=30)
    failure_threshold: int = Field(
        3, description="Number of consecutive failures needed", gt=1, le=10)

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "ip_address": "192.0.2.1",
                "port": 443,
                "type": "HTTPS",
                "resource_path": "/health",
                "request_interval": 30,
                "failure_threshold": 3,
            },
        }


class HealthCheckResponse(BaseModel):
    """Health check creation response."""

    id: str = Field(..., description="Health check ID")
    status: str = Field(..., description="Current health check status")


class FailoverConfig(BaseModel):
    """DNS failover configuration."""

    is_primary: bool = Field(...,
                             description="Whether this is the primary record")
    health_check_id: str | None = Field(
        None, description="Associated health check ID")


class WeightedConfig(BaseModel):
    """Weighted routing configuration."""

    weight = Field(
        ...,
        description="Routing weight (0-255)",
        gt=0,
        le=255,
    )
    set_identifier: str = Field(
        ...,
        description="Unique identifier for this weighted record set",
    )


class LatencyConfig(BaseModel):
    """Latency-based routing configuration."""

    region: str = Field(
        ...,
        description="AWS region for this endpoint",
    )
    set_identifier: str = Field(
        ...,
        description="Unique identifier for this latency record set",
    )


class RoutingConfig(BaseModel):
    """DNS routing configuration."""

    policy: Literal["WEIGHTED", "LATENCY"] = Field(
        ...,
        description="Routing policy type",
    )
    weighted: WeightedConfig | None = Field(
        None,
        description="Weighted routing configuration",
    )
    latency: LatencyConfig | None = Field(
        None,
        description="Latency-based routing configuration",
    )
    health_check_id: str | None = Field(
        None,
        description="Optional health check ID",
    )

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "examples": [
                {
                    "policy": "WEIGHTED",
                    "weighted": {
                        "weight": 100,
                        "set_identifier": "primary",
                    },
                },
                {
                    "policy": "LATENCY",
                    "latency": {
                        "region": "ap-northeast-2",
                        "set_identifier": "seoul",
                    },
                },
            ],
        }


class AliasTarget(BaseModel):
    """AWS service alias target configuration."""

    hosted_zone_id: str = Field(
        ...,
        description="Hosted zone ID of the AWS service",
    )
    dns_name: str = Field(
        ...,
        description="DNS name of the AWS service",
    )
    evaluate_target_health: bool = Field(
        True,
        description="Whether to evaluate target health",
    )

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "examples": [
                {
                    # CloudFront example
                    "hosted_zone_id": "Z2FDTNDATAQYW2",
                    "dns_name": "d123456789.cloudfront.net",
                    "evaluate_target_health": True,
                },
                {
                    # ALB example
                    "hosted_zone_id": "Z1H1FL5HABSF5",
                    "dns_name": "my-alb-123456789.region.elb.amazonaws.com",
                    "evaluate_target_health": True,
                },
            ],
        }


class DNSRecordSet(BaseModel):
    """DNS record set configuration."""

    name: str = Field(...,
                      description="DNS record name (e.g., 'example.com.')")
    type: Literal["A", "AAAA", "CNAME"] = Field(
        ...,
        description="DNS record type (only A, AAAA, CNAME supported for alias)",
    )
    ttl: int | None = Field(
        None,
        description="Time to live in seconds (not used for alias records)",
    )
    records: list[str] | None = Field(
        None,
        description="Record values (not used for alias records)",
    )
    alias_target: AliasTarget | None = Field(
        None,
        description="Alias target configuration",
    )
    failover: FailoverConfig | None = None
    routing: RoutingConfig | None = None

    class Config:
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "examples": [
                {
                    # Standard record
                    "name": "api.example.com.",
                    "type": "A",
                    "ttl": 300,
                    "records": ["192.0.2.1"],
                },
                {
                    # Alias record
                    "name": "www.example.com.",
                    "type": "A",
                    "alias_target": {
                        "hosted_zone_id": "Z2FDTNDATAQYW2",
                        "dns_name": "d123456789.cloudfront.net",
                        "evaluate_target_health": True,
                    },
                },
            ],
        }
