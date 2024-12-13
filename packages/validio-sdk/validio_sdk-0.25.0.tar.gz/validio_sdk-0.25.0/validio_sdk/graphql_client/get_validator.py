from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import (
    JsonFilterExpression,
    JsonPointer,
    SegmentationId,
    SourceId,
    ValidatorId,
    WindowId,
)

from .base_model import BaseModel
from .enums import (
    BooleanOperator,
    CategoricalDistributionMetric,
    ComparisonOperator,
    DecisionBoundsType,
    DifferenceOperator,
    DifferenceType,
    EnumOperator,
    NullOperator,
    NumericAnomalyMetric,
    NumericDistributionMetric,
    NumericMetric,
    RelativeTimeMetric,
    RelativeVolumeMetric,
    StringOperator,
    VolumeMetric,
)


class GetValidator(BaseModel):
    validator: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorValidator",
                "GetValidatorValidatorCategoricalDistributionValidator",
                "GetValidatorValidatorFreshnessValidator",
                "GetValidatorValidatorNumericAnomalyValidator",
                "GetValidatorValidatorNumericDistributionValidator",
                "GetValidatorValidatorNumericValidator",
                "GetValidatorValidatorRelativeTimeValidator",
                "GetValidatorValidatorRelativeVolumeValidator",
                "GetValidatorValidatorSqlValidator",
                "GetValidatorValidatorVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetValidatorValidatorValidator(BaseModel):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetValidatorValidatorValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorValidatorNamespace"
    tags: List["GetValidatorValidatorValidatorTags"]


class GetValidatorValidatorValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorValidatorSourceConfigSource"
    window: "GetValidatorValidatorValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorValidatorSourceConfigSourceFilterFilter",
                "GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorValidatorSourceConfigSource(BaseModel):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterFilter(BaseModel):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorValidatorSourceConfigSourceFilterFilterNamespace(BaseModel):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: (
        "GetValidatorValidatorValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilter(BaseModel):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilter(BaseModel):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilterConfig(BaseModel):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilter(BaseModel):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilterConfig(BaseModel):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilter(BaseModel):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: (
        "GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilterConfig(BaseModel):
    query: str


class GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilter(BaseModel):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilter(BaseModel):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilterConfig"
    )


class GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorValidatorCategoricalDistributionValidator(BaseModel):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorValidatorCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorNamespace"
    tags: List["GetValidatorValidatorCategoricalDistributionValidatorTags"]
    config: "GetValidatorValidatorCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSource"
    window: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: (
        "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSource(
    BaseModel
):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorCategoricalDistributionValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorValidatorCategoricalDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
    BaseModel
):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorFreshnessValidator(BaseModel):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetValidatorValidatorFreshnessValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorFreshnessValidatorNamespace"
    tags: List["GetValidatorValidatorFreshnessValidatorTags"]
    config: "GetValidatorValidatorFreshnessValidatorConfig"


class GetValidatorValidatorFreshnessValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorFreshnessValidatorSourceConfigSource"
    window: "GetValidatorValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterFilter",
                "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorFreshnessValidatorSourceConfigSource(BaseModel):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorFreshnessValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorFreshnessValidatorSourceConfigSegmentationNamespace"
    )


class GetValidatorValidatorFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterFilter(BaseModel):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig"
    )


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorFreshnessValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorFreshnessValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorValidatorFreshnessValidatorConfig(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "GetValidatorValidatorFreshnessValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorFreshnessValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorFreshnessValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorNumericAnomalyValidator(BaseModel):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetValidatorValidatorNumericAnomalyValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorNamespace"
    tags: List["GetValidatorValidatorNumericAnomalyValidatorTags"]
    config: "GetValidatorValidatorNumericAnomalyValidatorConfig"
    reference_source_config: (
        "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorValidatorNumericAnomalyValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter",
                "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSource(BaseModel):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace"
    )


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorNumericAnomalyValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorValidatorNumericAnomalyValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    sensitivity: float
    minimum_reference_datapoints: Optional[float] = Field(
        alias="minimumReferenceDatapoints"
    )
    minimum_absolute_difference: float = Field(alias="minimumAbsoluteDifference")
    minimum_relative_difference_percent: float = Field(
        alias="minimumRelativeDifferencePercent"
    )


class GetValidatorValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfig(BaseModel):
    source: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter",
                "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
    BaseModel
):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorNumericDistributionValidator(BaseModel):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetValidatorValidatorNumericDistributionValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericDistributionValidatorNamespace"
    tags: List["GetValidatorValidatorNumericDistributionValidatorTags"]
    config: "GetValidatorValidatorNumericDistributionValidatorConfig"
    reference_source_config: (
        "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorValidatorNumericDistributionValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSource"
    window: "GetValidatorValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: (
        "GetValidatorValidatorNumericDistributionValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter",
                "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSource(BaseModel):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceNamespace"
    )


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorNumericDistributionValidatorSourceConfigWindowNamespace"
    )


class GetValidatorValidatorNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorNumericDistributionValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorValidatorNumericDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfig(BaseModel):
    source: (
        "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    )
    window: (
        "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    )
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSource(
    BaseModel
):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorNumericValidator(BaseModel):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetValidatorValidatorNumericValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericValidatorNamespace"
    tags: List["GetValidatorValidatorNumericValidatorTags"]
    config: "GetValidatorValidatorNumericValidatorConfig"


class GetValidatorValidatorNumericValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorNumericValidatorSourceConfigSource"
    window: "GetValidatorValidatorNumericValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterFilter",
                "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorNumericValidatorSourceConfigSource(BaseModel):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorNumericValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorNumericValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorNumericValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterFilter(BaseModel):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilterConfig"
    )


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilterConfig"
    )


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilter(BaseModel):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilterConfig"
    )


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorNumericValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorValidatorNumericValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorNumericValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorNumericValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorNumericValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorRelativeTimeValidator(BaseModel):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetValidatorValidatorRelativeTimeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeTimeValidatorNamespace"
    tags: List["GetValidatorValidatorRelativeTimeValidatorTags"]
    config: "GetValidatorValidatorRelativeTimeValidatorConfig"


class GetValidatorValidatorRelativeTimeValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSource"
    window: "GetValidatorValidatorRelativeTimeValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter",
                "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSource(BaseModel):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorRelativeTimeValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace"
    )


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorRelativeTimeValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorValidatorRelativeTimeValidatorConfig(BaseModel):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorRelativeVolumeValidator(BaseModel):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetValidatorValidatorRelativeVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorNamespace"
    tags: List["GetValidatorValidatorRelativeVolumeValidatorTags"]
    config: "GetValidatorValidatorRelativeVolumeValidatorConfig"
    reference_source_config: (
        "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorValidatorRelativeVolumeValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter",
                "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSource(BaseModel):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace"
    )


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorRelativeVolumeValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorValidatorRelativeVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfig(BaseModel):
    source: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter",
                "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
    BaseModel
):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorSqlValidator(BaseModel):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetValidatorValidatorSqlValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorSqlValidatorNamespace"
    tags: List["GetValidatorValidatorSqlValidatorTags"]
    config: "GetValidatorValidatorSqlValidatorConfig"


class GetValidatorValidatorSqlValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorSqlValidatorSourceConfigSource"
    window: "GetValidatorValidatorSqlValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterFilter",
                "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorSqlValidatorSourceConfigSource(BaseModel):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorSqlValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorSqlValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorSqlValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterFilter(BaseModel):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterFilterSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter(BaseModel):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterConfig"
    )


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilter(BaseModel):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilter(BaseModel):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilter(BaseModel):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilter(BaseModel):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilterConfig"
    )


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterConfig"
    )


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorSqlValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorSqlValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorValidatorSqlValidatorConfig(BaseModel):
    query: str
    threshold: Union[
        "GetValidatorValidatorSqlValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorSqlValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class GetValidatorValidatorSqlValidatorConfigThresholdDifferenceThreshold(BaseModel):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorSqlValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorSqlValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorVolumeValidator(BaseModel):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetValidatorValidatorVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorVolumeValidatorNamespace"
    tags: List["GetValidatorValidatorVolumeValidatorTags"]
    config: "GetValidatorValidatorVolumeValidatorConfig"


class GetValidatorValidatorVolumeValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorVolumeValidatorSourceConfigSource"
    window: "GetValidatorValidatorVolumeValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterFilter",
                "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorValidatorVolumeValidatorSourceConfigSource(BaseModel):
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
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorVolumeValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorVolumeValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorVolumeValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterFilter(BaseModel):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter(BaseModel):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"
    )


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilter(BaseModel):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilterConfig"
    )


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter(BaseModel):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"
    )


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilterConfig"
    )


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorValidatorVolumeValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorVolumeValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorValidatorVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorVolumeValidatorConfigThresholdDifferenceThreshold(BaseModel):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorVolumeValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorVolumeValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


GetValidator.model_rebuild()
GetValidatorValidatorValidator.model_rebuild()
GetValidatorValidatorValidatorSourceConfig.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidator.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfig.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorConfig.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorFreshnessValidator.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfig.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorFreshnessValidatorConfig.model_rebuild()
GetValidatorValidatorNumericAnomalyValidator.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfig.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorConfig.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidator.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfig.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorConfig.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorNumericValidator.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfig.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorNumericValidatorConfig.model_rebuild()
GetValidatorValidatorRelativeTimeValidator.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfig.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorConfig.model_rebuild()
GetValidatorValidatorRelativeVolumeValidator.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfig.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorConfig.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorSqlValidator.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfig.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorSqlValidatorConfig.model_rebuild()
GetValidatorValidatorVolumeValidator.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfig.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorValidatorVolumeValidatorConfig.model_rebuild()
