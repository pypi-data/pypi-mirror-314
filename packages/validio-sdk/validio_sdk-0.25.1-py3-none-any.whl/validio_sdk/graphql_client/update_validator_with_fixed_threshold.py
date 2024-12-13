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


class UpdateValidatorWithFixedThreshold(BaseModel):
    validator_with_fixed_threshold_update: (
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdate"
    ) = Field(alias="validatorWithFixedThresholdUpdate")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdate(BaseModel):
    errors: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateErrors"
    ]
    validator: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidator",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidator",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidator",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidator",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidator",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidator",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidator",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidator",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidator",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateErrors(
    ErrorDetails
):
    pass


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidator(
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
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorNamespace"
    tags: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorTags"
    ]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidator(
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
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorNamespace"
    tags: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorTags"
    ]
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidator(
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
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorNamespace"
    tags: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorTags"
    ]
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorConfig(
    BaseModel
):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidator(
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
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorNamespace"
    tags: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorTags"
    ]
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidator(
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
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorNamespace"
    tags: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorTags"
    ]
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidator(
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
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorNamespace"
    tags: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorTags"
    ]
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidator(
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
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorTags"
    ]
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorConfig(
    BaseModel
):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidator(
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
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorTags"
    ]
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorConfig(
    BaseModel
):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidator(
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
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorNamespace"
    tags: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorTags"
    ]
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorConfig(
    BaseModel
):
    query: str
    threshold: Union[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidator(
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
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorTags"
    ]
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSource"
    window: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilter",
                "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorConfig(
    BaseModel
):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


UpdateValidatorWithFixedThreshold.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdate.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidator.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidator.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidator.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorFreshnessValidatorConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidator.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidator.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidator.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorNumericValidatorConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidator.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeTimeValidatorConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidator.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidator.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorSqlValidatorConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidator.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
UpdateValidatorWithFixedThresholdValidatorWithFixedThresholdUpdateValidatorVolumeValidatorConfig.model_rebuild()
