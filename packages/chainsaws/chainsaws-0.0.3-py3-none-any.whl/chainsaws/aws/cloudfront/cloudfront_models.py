from typing import Literal

from pydantic import BaseModel, Field

from chainsaws.aws.shared.config import APIConfig


class CloudFrontAPIConfig(APIConfig):
    """Configuration for CloudFront client."""



class OriginConfig(BaseModel):
    """Origin configuration for CloudFront distribution."""

    domain_name: str = Field(..., description="Origin domain name")
    origin_id: str = Field(..., description="Unique identifier for the origin")
    origin_path: str | None = Field(
        "", description="Path to request content from")
    custom_headers: dict[str, str] | None = Field(
        default={},
        description="Custom headers to send to origin",
    )
    s3_origin_access_identity: str | None = Field(
        None,
        description="OAI for S3 bucket origin",
    )


class BehaviorConfig(BaseModel):
    """Cache behavior configuration."""

    path_pattern: str | None = Field(
        "*",
        description="Path pattern this behavior applies to",
    )
    target_origin_id: str = Field(..., description="ID of target origin")
    viewer_protocol_policy: Literal["redirect-to-https", "https-only", "allow-all"] = Field(
        "redirect-to-https",
        description="Protocol policy for viewers",
    )
    allowed_methods: list[str] = Field(
        ["GET", "HEAD"],
        description="Allowed HTTP methods",
    )
    cached_methods: list[str] = Field(
        ["GET", "HEAD"],
        description="Methods to cache",
    )
    cache_policy_id: str | None = Field(
        None,
        description="Cache policy ID",
    )
    origin_request_policy_id: str | None = Field(
        None,
        description="Origin request policy ID",
    )
    response_headers_policy_id: str | None = Field(
        None,
        description="Response headers policy ID",
    )
    function_associations: list[dict[str, str]] | None = Field(
        default=[],
        description="CloudFront function associations",
    )


class DistributionConfig(BaseModel):
    """CloudFront distribution configuration."""

    comment: str | None = Field("", description="Distribution comment")
    enabled: bool = Field(True, description="Distribution enabled state")
    aliases: list[str] | None = Field(
        default=[],
        description="Alternate domain names (CNAMEs)",
    )
    default_root_object: str | None = Field(
        "index.html",
        description="Default root object",
    )
    origins: list[OriginConfig] = Field(...,
                                        description="Origin configurations")
    default_behavior: BehaviorConfig = Field(...,
                                             description="Default cache behavior")
    custom_behaviors: list[BehaviorConfig] | None = Field(
        default=[],
        description="Custom cache behaviors",
    )
    price_class: Literal["PriceClass_All", "PriceClass_200", "PriceClass_100"] = Field(
        "PriceClass_100",
        description="Distribution price class",
    )
    certificate_arn: str | None = Field(
        None,
        description="ACM certificate ARN for custom domain",
    )
    web_acl_id: str | None = Field(
        None,
        description="WAF web ACL ID",
    )


class DistributionSummary(BaseModel):
    """Summary of CloudFront distribution."""

    id: str = Field(..., description="Distribution ID")
    domain_name: str = Field(..., description="Distribution domain name")
    enabled: bool = Field(..., description="Distribution enabled state")
    status: str = Field(..., description="Deployment status")
    aliases: list[str] = Field(..., description="Alternate domain names")
