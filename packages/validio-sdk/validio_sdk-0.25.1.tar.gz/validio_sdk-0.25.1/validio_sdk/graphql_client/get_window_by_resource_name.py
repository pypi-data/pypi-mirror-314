from datetime import datetime
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import JsonPointer, SourceId, WindowId

from .base_model import BaseModel
from .enums import WindowTimeUnit


class GetWindowByResourceName(BaseModel):
    window_by_resource_name: Optional[
        Annotated[
            Union[
                "GetWindowByResourceNameWindowByResourceNameWindow",
                "GetWindowByResourceNameWindowByResourceNameFileWindow",
                "GetWindowByResourceNameWindowByResourceNameFixedBatchWindow",
                "GetWindowByResourceNameWindowByResourceNameTumblingWindow",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="windowByResourceName")


class GetWindowByResourceNameWindowByResourceNameWindow(BaseModel):
    typename__: Literal["GlobalWindow", "Window"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowByResourceNameWindowByResourceNameWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowByResourceNameWindowByResourceNameWindowNamespace"


class GetWindowByResourceNameWindowByResourceNameWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowByResourceNameWindowByResourceNameWindowSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetWindowByResourceNameWindowByResourceNameWindowSourceNamespace(BaseModel):
    id: Any


class GetWindowByResourceNameWindowByResourceNameWindowNamespace(BaseModel):
    id: Any


class GetWindowByResourceNameWindowByResourceNameFileWindow(BaseModel):
    typename__: Literal["FileWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowByResourceNameWindowByResourceNameFileWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowByResourceNameWindowByResourceNameFileWindowNamespace"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class GetWindowByResourceNameWindowByResourceNameFileWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowByResourceNameWindowByResourceNameFileWindowSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetWindowByResourceNameWindowByResourceNameFileWindowSourceNamespace(BaseModel):
    id: Any


class GetWindowByResourceNameWindowByResourceNameFileWindowNamespace(BaseModel):
    id: Any


class GetWindowByResourceNameWindowByResourceNameFixedBatchWindow(BaseModel):
    typename__: Literal["FixedBatchWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowByResourceNameWindowByResourceNameFixedBatchWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowByResourceNameWindowByResourceNameFixedBatchWindowNamespace"
    config: "GetWindowByResourceNameWindowByResourceNameFixedBatchWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class GetWindowByResourceNameWindowByResourceNameFixedBatchWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetWindowByResourceNameWindowByResourceNameFixedBatchWindowSourceNamespace"
    )
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetWindowByResourceNameWindowByResourceNameFixedBatchWindowSourceNamespace(
    BaseModel
):
    id: Any


class GetWindowByResourceNameWindowByResourceNameFixedBatchWindowNamespace(BaseModel):
    id: Any


class GetWindowByResourceNameWindowByResourceNameFixedBatchWindowConfig(BaseModel):
    batch_size: int = Field(alias="batchSize")
    segmented_batching: bool = Field(alias="segmentedBatching")
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs")


class GetWindowByResourceNameWindowByResourceNameTumblingWindow(BaseModel):
    typename__: Literal["TumblingWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowByResourceNameWindowByResourceNameTumblingWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowByResourceNameWindowByResourceNameTumblingWindowNamespace"
    config: "GetWindowByResourceNameWindowByResourceNameTumblingWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class GetWindowByResourceNameWindowByResourceNameTumblingWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetWindowByResourceNameWindowByResourceNameTumblingWindowSourceNamespace"
    )
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetWindowByResourceNameWindowByResourceNameTumblingWindowSourceNamespace(
    BaseModel
):
    id: Any


class GetWindowByResourceNameWindowByResourceNameTumblingWindowNamespace(BaseModel):
    id: Any


class GetWindowByResourceNameWindowByResourceNameTumblingWindowConfig(BaseModel):
    window_size: int = Field(alias="windowSize")
    time_unit: WindowTimeUnit = Field(alias="timeUnit")
    window_timeout_disabled: bool = Field(alias="windowTimeoutDisabled")


GetWindowByResourceName.model_rebuild()
GetWindowByResourceNameWindowByResourceNameWindow.model_rebuild()
GetWindowByResourceNameWindowByResourceNameWindowSource.model_rebuild()
GetWindowByResourceNameWindowByResourceNameFileWindow.model_rebuild()
GetWindowByResourceNameWindowByResourceNameFileWindowSource.model_rebuild()
GetWindowByResourceNameWindowByResourceNameFixedBatchWindow.model_rebuild()
GetWindowByResourceNameWindowByResourceNameFixedBatchWindowSource.model_rebuild()
GetWindowByResourceNameWindowByResourceNameTumblingWindow.model_rebuild()
GetWindowByResourceNameWindowByResourceNameTumblingWindowSource.model_rebuild()
