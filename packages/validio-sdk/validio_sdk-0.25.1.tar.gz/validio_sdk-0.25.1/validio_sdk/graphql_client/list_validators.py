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


class ListValidators(BaseModel):
    validators_list: List[
        Annotated[
            Union[
                "ListValidatorsValidatorsListValidator",
                "ListValidatorsValidatorsListCategoricalDistributionValidator",
                "ListValidatorsValidatorsListFreshnessValidator",
                "ListValidatorsValidatorsListNumericAnomalyValidator",
                "ListValidatorsValidatorsListNumericDistributionValidator",
                "ListValidatorsValidatorsListNumericValidator",
                "ListValidatorsValidatorsListRelativeTimeValidator",
                "ListValidatorsValidatorsListRelativeVolumeValidator",
                "ListValidatorsValidatorsListSqlValidator",
                "ListValidatorsValidatorsListVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="validatorsList")


class ListValidatorsValidatorsListValidator(BaseModel):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "ListValidatorsValidatorsListValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListValidatorNamespace"
    tags: List["ListValidatorsValidatorsListValidatorTags"]


class ListValidatorsValidatorsListValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListValidatorSourceConfigWindow"
    segmentation: "ListValidatorsValidatorsListValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterFilter(BaseModel):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: (
        "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterFilterNamespace"
    )
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilterConfig"
    )


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilterConfig"
    )


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilter(BaseModel):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: (
        "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilterConfig"
    )


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class ListValidatorsValidatorsListCategoricalDistributionValidator(BaseModel):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorNamespace"
    tags: List["ListValidatorsValidatorsListCategoricalDistributionValidatorTags"]
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: (
        "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSource"
    )
    window: (
        "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigWindow"
    )
    segmentation: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListCategoricalDistributionValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class ListValidatorsValidatorsListCategoricalDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListFreshnessValidator(BaseModel):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "ListValidatorsValidatorsListFreshnessValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorNamespace"
    tags: List["ListValidatorsValidatorsListFreshnessValidatorTags"]
    config: "ListValidatorsValidatorsListFreshnessValidatorConfig"


class ListValidatorsValidatorsListFreshnessValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigWindow"
    segmentation: (
        "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
        "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceNamespace"
    )


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListFreshnessValidatorSourceConfigWindowNamespace"
    )


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListFreshnessValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class ListValidatorsValidatorsListFreshnessValidatorConfig(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "ListValidatorsValidatorsListFreshnessValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListFreshnessValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListNumericAnomalyValidator(BaseModel):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorNamespace"
    tags: List["ListValidatorsValidatorsListNumericAnomalyValidatorTags"]
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorConfig"
    reference_source_config: (
        "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigWindow"
    segmentation: (
        "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
        "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceNamespace"
    )


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigWindowNamespace"
    )


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListNumericAnomalyValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class ListValidatorsValidatorsListNumericAnomalyValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: (
        "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSource"
    )
    window: (
        "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigWindow"
    )
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListNumericDistributionValidator(BaseModel):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorNamespace"
    tags: List["ListValidatorsValidatorsListNumericDistributionValidatorTags"]
    config: "ListValidatorsValidatorsListNumericDistributionValidatorConfig"
    reference_source_config: (
        "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigWindow"
    segmentation: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListNumericDistributionValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class ListValidatorsValidatorsListNumericDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSource"
    window: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListNumericValidator(BaseModel):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "ListValidatorsValidatorsListNumericValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericValidatorNamespace"
    tags: List["ListValidatorsValidatorsListNumericValidatorTags"]
    config: "ListValidatorsValidatorsListNumericValidatorConfig"


class ListValidatorsValidatorsListNumericValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListNumericValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListNumericValidatorSourceConfigWindow"
    segmentation: "ListValidatorsValidatorsListNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListNumericValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListNumericValidatorSourceConfigSegmentationNamespace"
    )


class ListValidatorsValidatorsListNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListNumericValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListNumericValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class ListValidatorsValidatorsListNumericValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListNumericValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListNumericValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListRelativeTimeValidator(BaseModel):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorNamespace"
    tags: List["ListValidatorsValidatorsListRelativeTimeValidatorTags"]
    config: "ListValidatorsValidatorsListRelativeTimeValidatorConfig"


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigWindow"
    segmentation: (
        "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
        "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceNamespace"
    )


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigWindowNamespace"
    )


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListRelativeTimeValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class ListValidatorsValidatorsListRelativeTimeValidatorConfig(BaseModel):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListRelativeVolumeValidator(BaseModel):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorNamespace"
    tags: List["ListValidatorsValidatorsListRelativeVolumeValidatorTags"]
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorConfig"
    reference_source_config: (
        "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigWindow"
    segmentation: (
        "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
        "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceNamespace"
    )


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigWindowNamespace"
    )


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListRelativeVolumeValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class ListValidatorsValidatorsListRelativeVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: (
        "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSource"
    )
    window: (
        "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigWindow"
    )
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListSqlValidator(BaseModel):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "ListValidatorsValidatorsListSqlValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListSqlValidatorNamespace"
    tags: List["ListValidatorsValidatorsListSqlValidatorTags"]
    config: "ListValidatorsValidatorsListSqlValidatorConfig"


class ListValidatorsValidatorsListSqlValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListSqlValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListSqlValidatorSourceConfigWindow"
    segmentation: "ListValidatorsValidatorsListSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListSqlValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListSqlValidatorSourceConfigSegmentationNamespace"
    )


class ListValidatorsValidatorsListSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterFilter(BaseModel):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: (
        "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterFilterSource"
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListSqlValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListSqlValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class ListValidatorsValidatorsListSqlValidatorConfig(BaseModel):
    query: str
    threshold: Union[
        "ListValidatorsValidatorsListSqlValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListSqlValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class ListValidatorsValidatorsListSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListSqlValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListSqlValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListVolumeValidator(BaseModel):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "ListValidatorsValidatorsListVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListVolumeValidatorNamespace"
    tags: List["ListValidatorsValidatorsListVolumeValidatorTags"]
    config: "ListValidatorsValidatorsListVolumeValidatorConfig"


class ListValidatorsValidatorsListVolumeValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListVolumeValidatorSourceConfigWindow"
    segmentation: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterFilter",
                "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilter",
                "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilter",
                "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListVolumeValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListVolumeValidatorSourceConfigSegmentationNamespace"
    )


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class ListValidatorsValidatorsListVolumeValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class ListValidatorsValidatorsListVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListVolumeValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListVolumeValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


ListValidators.model_rebuild()
ListValidatorsValidatorsListValidator.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidator.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorConfig.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListFreshnessValidator.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorConfig.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidator.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorConfig.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidator.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorConfig.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericValidator.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListNumericValidatorConfig.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidator.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorConfig.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidator.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorConfig.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListSqlValidator.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListSqlValidatorConfig.model_rebuild()
ListValidatorsValidatorsListVolumeValidator.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorConfig.model_rebuild()
