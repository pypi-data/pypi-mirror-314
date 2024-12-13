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
from .fragments import ErrorDetails


class UpdateValidatorWithDynamicThreshold(BaseModel):
    validator_with_dynamic_threshold_update: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdate"
    ) = Field(alias="validatorWithDynamicThresholdUpdate")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdate(BaseModel):
    errors: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateErrors"
    ]
    validator: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidator",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidator",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidator",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidator",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidator",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidator",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidator",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidator",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidator",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateErrors(
    ErrorDetails
):
    pass


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidator(
    BaseModel
):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorTags"
    ]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidator(
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
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorTags"
    ]
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidator(
    BaseModel
):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorTags"
    ]
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorConfig(
    BaseModel
):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidator(
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
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorTags"
    ]
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidator(
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
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorTags"
    ]
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidator(
    BaseModel
):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorTags"
    ]
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidator(
    BaseModel
):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorTags"
    ]
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorConfig(
    BaseModel
):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidator(
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
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorTags"
    ]
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorConfig(
    BaseModel
):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidator(
    BaseModel
):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorTags"
    ]
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorConfig(
    BaseModel
):
    query: str
    threshold: Union[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidator(
    BaseModel
):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorTags"
    ]
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSource"
    window: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
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


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorConfig(
    BaseModel
):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


UpdateValidatorWithDynamicThreshold.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdate.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidator.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidator.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidator.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorFreshnessValidatorConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidator.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidator.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidator.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorNumericValidatorConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidator.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeTimeValidatorConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidator.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidator.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorSqlValidatorConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidator.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDynamicThresholdValidatorWithDynamicThresholdUpdateValidatorVolumeValidatorConfig.model_rebuild()
