from datetime import datetime
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import JsonPointer, SourceId, WindowId

from .base_model import BaseModel
from .enums import WindowTimeUnit


class GetWindow(BaseModel):
    window: Optional[
        Annotated[
            Union[
                "GetWindowWindowWindow",
                "GetWindowWindowFileWindow",
                "GetWindowWindowFixedBatchWindow",
                "GetWindowWindowTumblingWindow",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetWindowWindowWindow(BaseModel):
    typename__: Literal["GlobalWindow", "Window"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowWindowWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowWindowWindowNamespace"


class GetWindowWindowWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowWindowWindowSourceNamespace"
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


class GetWindowWindowWindowSourceNamespace(BaseModel):
    id: Any


class GetWindowWindowWindowNamespace(BaseModel):
    id: Any


class GetWindowWindowFileWindow(BaseModel):
    typename__: Literal["FileWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowWindowFileWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowWindowFileWindowNamespace"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class GetWindowWindowFileWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowWindowFileWindowSourceNamespace"
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


class GetWindowWindowFileWindowSourceNamespace(BaseModel):
    id: Any


class GetWindowWindowFileWindowNamespace(BaseModel):
    id: Any


class GetWindowWindowFixedBatchWindow(BaseModel):
    typename__: Literal["FixedBatchWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowWindowFixedBatchWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowWindowFixedBatchWindowNamespace"
    config: "GetWindowWindowFixedBatchWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class GetWindowWindowFixedBatchWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowWindowFixedBatchWindowSourceNamespace"
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


class GetWindowWindowFixedBatchWindowSourceNamespace(BaseModel):
    id: Any


class GetWindowWindowFixedBatchWindowNamespace(BaseModel):
    id: Any


class GetWindowWindowFixedBatchWindowConfig(BaseModel):
    batch_size: int = Field(alias="batchSize")
    segmented_batching: bool = Field(alias="segmentedBatching")
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs")


class GetWindowWindowTumblingWindow(BaseModel):
    typename__: Literal["TumblingWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "GetWindowWindowTumblingWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowWindowTumblingWindowNamespace"
    config: "GetWindowWindowTumblingWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class GetWindowWindowTumblingWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetWindowWindowTumblingWindowSourceNamespace"
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


class GetWindowWindowTumblingWindowSourceNamespace(BaseModel):
    id: Any


class GetWindowWindowTumblingWindowNamespace(BaseModel):
    id: Any


class GetWindowWindowTumblingWindowConfig(BaseModel):
    window_size: int = Field(alias="windowSize")
    time_unit: WindowTimeUnit = Field(alias="timeUnit")
    window_timeout_disabled: bool = Field(alias="windowTimeoutDisabled")


GetWindow.model_rebuild()
GetWindowWindowWindow.model_rebuild()
GetWindowWindowWindowSource.model_rebuild()
GetWindowWindowFileWindow.model_rebuild()
GetWindowWindowFileWindowSource.model_rebuild()
GetWindowWindowFixedBatchWindow.model_rebuild()
GetWindowWindowFixedBatchWindowSource.model_rebuild()
GetWindowWindowTumblingWindow.model_rebuild()
GetWindowWindowTumblingWindowSource.model_rebuild()
