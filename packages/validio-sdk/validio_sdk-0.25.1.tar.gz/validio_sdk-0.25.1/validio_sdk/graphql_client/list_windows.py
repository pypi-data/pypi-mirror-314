from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import JsonPointer, SourceId, WindowId

from .base_model import BaseModel
from .enums import WindowTimeUnit


class ListWindows(BaseModel):
    windows_list: List[
        Annotated[
            Union[
                "ListWindowsWindowsListWindow",
                "ListWindowsWindowsListFileWindow",
                "ListWindowsWindowsListFixedBatchWindow",
                "ListWindowsWindowsListTumblingWindow",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="windowsList")


class ListWindowsWindowsListWindow(BaseModel):
    typename__: Literal["GlobalWindow", "Window"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "ListWindowsWindowsListWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListWindowsWindowsListWindowNamespace"


class ListWindowsWindowsListWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListWindowsWindowsListWindowSourceNamespace"
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


class ListWindowsWindowsListWindowSourceNamespace(BaseModel):
    id: Any


class ListWindowsWindowsListWindowNamespace(BaseModel):
    id: Any


class ListWindowsWindowsListFileWindow(BaseModel):
    typename__: Literal["FileWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "ListWindowsWindowsListFileWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListWindowsWindowsListFileWindowNamespace"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class ListWindowsWindowsListFileWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListWindowsWindowsListFileWindowSourceNamespace"
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


class ListWindowsWindowsListFileWindowSourceNamespace(BaseModel):
    id: Any


class ListWindowsWindowsListFileWindowNamespace(BaseModel):
    id: Any


class ListWindowsWindowsListFixedBatchWindow(BaseModel):
    typename__: Literal["FixedBatchWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "ListWindowsWindowsListFixedBatchWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListWindowsWindowsListFixedBatchWindowNamespace"
    config: "ListWindowsWindowsListFixedBatchWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class ListWindowsWindowsListFixedBatchWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListWindowsWindowsListFixedBatchWindowSourceNamespace"
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


class ListWindowsWindowsListFixedBatchWindowSourceNamespace(BaseModel):
    id: Any


class ListWindowsWindowsListFixedBatchWindowNamespace(BaseModel):
    id: Any


class ListWindowsWindowsListFixedBatchWindowConfig(BaseModel):
    batch_size: int = Field(alias="batchSize")
    segmented_batching: bool = Field(alias="segmentedBatching")
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs")


class ListWindowsWindowsListTumblingWindow(BaseModel):
    typename__: Literal["TumblingWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "ListWindowsWindowsListTumblingWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListWindowsWindowsListTumblingWindowNamespace"
    config: "ListWindowsWindowsListTumblingWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class ListWindowsWindowsListTumblingWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListWindowsWindowsListTumblingWindowSourceNamespace"
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


class ListWindowsWindowsListTumblingWindowSourceNamespace(BaseModel):
    id: Any


class ListWindowsWindowsListTumblingWindowNamespace(BaseModel):
    id: Any


class ListWindowsWindowsListTumblingWindowConfig(BaseModel):
    window_size: int = Field(alias="windowSize")
    time_unit: WindowTimeUnit = Field(alias="timeUnit")
    window_timeout_disabled: bool = Field(alias="windowTimeoutDisabled")


ListWindows.model_rebuild()
ListWindowsWindowsListWindow.model_rebuild()
ListWindowsWindowsListWindowSource.model_rebuild()
ListWindowsWindowsListFileWindow.model_rebuild()
ListWindowsWindowsListFileWindowSource.model_rebuild()
ListWindowsWindowsListFixedBatchWindow.model_rebuild()
ListWindowsWindowsListFixedBatchWindowSource.model_rebuild()
ListWindowsWindowsListTumblingWindow.model_rebuild()
ListWindowsWindowsListTumblingWindowSource.model_rebuild()
