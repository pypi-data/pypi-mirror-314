"""
Lambda Event Types for S3 triggers
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class S3UserIdentity(BaseModel):
    principalId: str


class S3RequestParameters(BaseModel):
    sourceIPAddress: str


class S3ResponseElements(BaseModel):
    x_amz_request_id: Optional[str] = Field(None, alias="x-amz-request-id")
    x_amz_id_2: Optional[str] = Field(None, alias="x-amz-id-2")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class S3OwnerIdentity(BaseModel):
    principalId: str


class S3Bucket(BaseModel):
    name: str
    ownerIdentity: S3OwnerIdentity
    arn: str


class S3Object(BaseModel):
    key: str
    size: int
    eTag: str
    versionId: Optional[str] = None
    sequencer: str


class S3Details(BaseModel):
    s3SchemaVersion: str
    configurationId: str
    bucket: S3Bucket
    object: S3Object


class S3GlacierRestoreEventData(BaseModel):
    lifecycleRestorationExpiryTime: str
    lifecycleRestoreStorageClass: str


class S3GlacierEventData(BaseModel):
    restoreEventData: S3GlacierRestoreEventData


class S3Message(BaseModel):
    """S3 event message structure"""
    eventVersion: str
    eventSource: str
    awsRegion: str
    eventTime: str
    eventName: str
    userIdentity: S3UserIdentity
    requestParameters: S3RequestParameters
    responseElements: Optional[S3ResponseElements] = None
    s3: S3Details
    glacierEventData: Optional[S3GlacierEventData] = None


class S3Event(BaseModel):
    Records: List[S3Message]
