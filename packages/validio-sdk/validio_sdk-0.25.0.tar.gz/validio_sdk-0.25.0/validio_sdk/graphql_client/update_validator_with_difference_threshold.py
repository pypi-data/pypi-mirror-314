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


class UpdateValidatorWithDifferenceThreshold(BaseModel):
    validator_with_difference_threshold_update: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdate"
    ) = Field(alias="validatorWithDifferenceThresholdUpdate")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdate(
    BaseModel
):
    errors: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateErrors"
    ]
    validator: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateErrors(
    ErrorDetails
):
    pass


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidator(
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
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorTags"
    ]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidator(
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
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidator(
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
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfig(
    BaseModel
):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidator(
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
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidator(
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
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidator(
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
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidator(
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
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfig(
    BaseModel
):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidator(
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
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfig(
    BaseModel
):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidator(
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
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfig(
    BaseModel
):
    query: str
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidator(
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
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfig(
    BaseModel
):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


UpdateValidatorWithDifferenceThreshold.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdate.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfig.model_rebuild()
