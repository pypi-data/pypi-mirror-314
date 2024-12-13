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


class GetValidatorByResourceName(BaseModel):
    validator_by_resource_name: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameValidator",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidator",
                "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidator",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidator",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidator",
                "GetValidatorByResourceNameValidatorByResourceNameNumericValidator",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidator",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidator",
                "GetValidatorByResourceNameValidatorByResourceNameSqlValidator",
                "GetValidatorByResourceNameValidatorByResourceNameVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="validatorByResourceName")


class GetValidatorByResourceNameValidatorByResourceNameValidator(BaseModel):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorNamespace"
    tags: List["GetValidatorByResourceNameValidatorByResourceNameValidatorTags"]


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfig(BaseModel):
    source: (
        "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSource"
    )
    window: (
        "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigWindow"
    )
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameValidatorNamespace(BaseModel):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidator(
    BaseModel
):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorNamespace"
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorTags"
    ]
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidator(BaseModel):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorNamespace"
    )
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorTags"
    ]
    config: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfig"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfig(
    BaseModel
):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidator(
    BaseModel
):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorNamespace"
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorTags"
    ]
    config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfig"
    )
    reference_source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidator(
    BaseModel
):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorNamespace"
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorTags"
    ]
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfig"
    reference_source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericValidator(BaseModel):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorNamespace"
    )
    tags: List["GetValidatorByResourceNameValidatorByResourceNameNumericValidatorTags"]
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidator(BaseModel):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorNamespace"
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorTags"
    ]
    config: (
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfig"
    )


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfig(
    BaseModel
):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidator(
    BaseModel
):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorNamespace"
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorTags"
    ]
    config: (
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfig"
    )
    reference_source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfig(
    BaseModel
):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameSqlValidator(BaseModel):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorNamespace"
    tags: List["GetValidatorByResourceNameValidatorByResourceNameSqlValidatorTags"]
    config: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfig"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorNamespace(BaseModel):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfig(BaseModel):
    query: str
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidator(BaseModel):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorNamespace"
    )
    tags: List["GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorTags"]
    config: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfig"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterFilter",
                "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilter",
                "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilter",
                "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


GetValidatorByResourceName.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfig.model_rebuild()
