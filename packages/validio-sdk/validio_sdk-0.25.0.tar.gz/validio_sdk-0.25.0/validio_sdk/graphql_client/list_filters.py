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


class ListFilters(BaseModel):
    filters_list: List[
        Annotated[
            Union[
                "ListFiltersFiltersListFilter",
                "ListFiltersFiltersListBooleanFilter",
                "ListFiltersFiltersListEnumFilter",
                "ListFiltersFiltersListNullFilter",
                "ListFiltersFiltersListSqlFilter",
                "ListFiltersFiltersListStringFilter",
                "ListFiltersFiltersListThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="filtersList")


class ListFiltersFiltersListFilter(BaseModel):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListFiltersFiltersListFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListFiltersFiltersListFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListFiltersFiltersListFilterNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListFiltersFiltersListFilterSourceNamespace"
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


class ListFiltersFiltersListFilterSourceNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListBooleanFilter(BaseModel):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListFiltersFiltersListBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListFiltersFiltersListBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListFiltersFiltersListBooleanFilterConfig"


class ListFiltersFiltersListBooleanFilterNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListBooleanFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListFiltersFiltersListBooleanFilterSourceNamespace"
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


class ListFiltersFiltersListBooleanFilterSourceNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListBooleanFilterConfig(BaseModel):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListFiltersFiltersListEnumFilter(BaseModel):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListFiltersFiltersListEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListFiltersFiltersListEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListFiltersFiltersListEnumFilterConfig"


class ListFiltersFiltersListEnumFilterNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListEnumFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListFiltersFiltersListEnumFilterSourceNamespace"
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


class ListFiltersFiltersListEnumFilterSourceNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListEnumFilterConfig(BaseModel):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListFiltersFiltersListNullFilter(BaseModel):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListFiltersFiltersListNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListFiltersFiltersListNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListFiltersFiltersListNullFilterConfig"


class ListFiltersFiltersListNullFilterNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListNullFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListFiltersFiltersListNullFilterSourceNamespace"
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


class ListFiltersFiltersListNullFilterSourceNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListNullFilterConfig(BaseModel):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListFiltersFiltersListSqlFilter(BaseModel):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListFiltersFiltersListSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListFiltersFiltersListSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListFiltersFiltersListSqlFilterConfig"


class ListFiltersFiltersListSqlFilterNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListSqlFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListFiltersFiltersListSqlFilterSourceNamespace"
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


class ListFiltersFiltersListSqlFilterSourceNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListSqlFilterConfig(BaseModel):
    query: str


class ListFiltersFiltersListStringFilter(BaseModel):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListFiltersFiltersListStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListFiltersFiltersListStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListFiltersFiltersListStringFilterConfig"


class ListFiltersFiltersListStringFilterNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListStringFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListFiltersFiltersListStringFilterSourceNamespace"
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


class ListFiltersFiltersListStringFilterSourceNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListStringFilterConfig(BaseModel):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListFiltersFiltersListThresholdFilter(BaseModel):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListFiltersFiltersListThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListFiltersFiltersListThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListFiltersFiltersListThresholdFilterConfig"


class ListFiltersFiltersListThresholdFilterNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListThresholdFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListFiltersFiltersListThresholdFilterSourceNamespace"
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


class ListFiltersFiltersListThresholdFilterSourceNamespace(BaseModel):
    id: Any


class ListFiltersFiltersListThresholdFilterConfig(BaseModel):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


ListFilters.model_rebuild()
ListFiltersFiltersListFilter.model_rebuild()
ListFiltersFiltersListFilterSource.model_rebuild()
ListFiltersFiltersListBooleanFilter.model_rebuild()
ListFiltersFiltersListBooleanFilterSource.model_rebuild()
ListFiltersFiltersListEnumFilter.model_rebuild()
ListFiltersFiltersListEnumFilterSource.model_rebuild()
ListFiltersFiltersListNullFilter.model_rebuild()
ListFiltersFiltersListNullFilterSource.model_rebuild()
ListFiltersFiltersListSqlFilter.model_rebuild()
ListFiltersFiltersListSqlFilterSource.model_rebuild()
ListFiltersFiltersListStringFilter.model_rebuild()
ListFiltersFiltersListStringFilterSource.model_rebuild()
ListFiltersFiltersListThresholdFilter.model_rebuild()
ListFiltersFiltersListThresholdFilterSource.model_rebuild()
