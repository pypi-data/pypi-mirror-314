from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import JsonPointer, SourceId

from .base_model import BaseModel
from .enums import (
    BooleanOperator,
    ComparisonOperator,
    EnumOperator,
    NullOperator,
    StringOperator,
)


class GetFilter(BaseModel):
    filter: Optional[
        Annotated[
            Union[
                "GetFilterFilterFilter",
                "GetFilterFilterBooleanFilter",
                "GetFilterFilterEnumFilter",
                "GetFilterFilterNullFilter",
                "GetFilterFilterSqlFilter",
                "GetFilterFilterStringFilter",
                "GetFilterFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetFilterFilterFilter(BaseModel):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetFilterFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetFilterFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetFilterFilterFilterNamespace(BaseModel):
    id: Any


class GetFilterFilterFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetFilterFilterFilterSourceNamespace"
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


class GetFilterFilterFilterSourceNamespace(BaseModel):
    id: Any


class GetFilterFilterBooleanFilter(BaseModel):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetFilterFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetFilterFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetFilterFilterBooleanFilterConfig"


class GetFilterFilterBooleanFilterNamespace(BaseModel):
    id: Any


class GetFilterFilterBooleanFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetFilterFilterBooleanFilterSourceNamespace"
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


class GetFilterFilterBooleanFilterSourceNamespace(BaseModel):
    id: Any


class GetFilterFilterBooleanFilterConfig(BaseModel):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetFilterFilterEnumFilter(BaseModel):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetFilterFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetFilterFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetFilterFilterEnumFilterConfig"


class GetFilterFilterEnumFilterNamespace(BaseModel):
    id: Any


class GetFilterFilterEnumFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetFilterFilterEnumFilterSourceNamespace"
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


class GetFilterFilterEnumFilterSourceNamespace(BaseModel):
    id: Any


class GetFilterFilterEnumFilterConfig(BaseModel):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetFilterFilterNullFilter(BaseModel):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetFilterFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetFilterFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetFilterFilterNullFilterConfig"


class GetFilterFilterNullFilterNamespace(BaseModel):
    id: Any


class GetFilterFilterNullFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetFilterFilterNullFilterSourceNamespace"
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


class GetFilterFilterNullFilterSourceNamespace(BaseModel):
    id: Any


class GetFilterFilterNullFilterConfig(BaseModel):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetFilterFilterSqlFilter(BaseModel):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetFilterFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetFilterFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetFilterFilterSqlFilterConfig"


class GetFilterFilterSqlFilterNamespace(BaseModel):
    id: Any


class GetFilterFilterSqlFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetFilterFilterSqlFilterSourceNamespace"
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


class GetFilterFilterSqlFilterSourceNamespace(BaseModel):
    id: Any


class GetFilterFilterSqlFilterConfig(BaseModel):
    query: str


class GetFilterFilterStringFilter(BaseModel):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetFilterFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetFilterFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetFilterFilterStringFilterConfig"


class GetFilterFilterStringFilterNamespace(BaseModel):
    id: Any


class GetFilterFilterStringFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetFilterFilterStringFilterSourceNamespace"
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


class GetFilterFilterStringFilterSourceNamespace(BaseModel):
    id: Any


class GetFilterFilterStringFilterConfig(BaseModel):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetFilterFilterThresholdFilter(BaseModel):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetFilterFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetFilterFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetFilterFilterThresholdFilterConfig"


class GetFilterFilterThresholdFilterNamespace(BaseModel):
    id: Any


class GetFilterFilterThresholdFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetFilterFilterThresholdFilterSourceNamespace"
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


class GetFilterFilterThresholdFilterSourceNamespace(BaseModel):
    id: Any


class GetFilterFilterThresholdFilterConfig(BaseModel):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


GetFilter.model_rebuild()
GetFilterFilterFilter.model_rebuild()
GetFilterFilterFilterSource.model_rebuild()
GetFilterFilterBooleanFilter.model_rebuild()
GetFilterFilterBooleanFilterSource.model_rebuild()
GetFilterFilterEnumFilter.model_rebuild()
GetFilterFilterEnumFilterSource.model_rebuild()
GetFilterFilterNullFilter.model_rebuild()
GetFilterFilterNullFilterSource.model_rebuild()
GetFilterFilterSqlFilter.model_rebuild()
GetFilterFilterSqlFilterSource.model_rebuild()
GetFilterFilterStringFilter.model_rebuild()
GetFilterFilterStringFilterSource.model_rebuild()
GetFilterFilterThresholdFilter.model_rebuild()
GetFilterFilterThresholdFilterSource.model_rebuild()
