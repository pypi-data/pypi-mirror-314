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
    IncidentGroupPriority,
    IncidentStatus,
    NullOperator,
    NumericAnomalyMetric,
    NumericDistributionMetric,
    NumericMetric,
    RelativeTimeMetric,
    RelativeVolumeMetric,
    StringOperator,
    VolumeMetric,
)
from .fragments import SegmentDetails


class GetIncidentGroup(BaseModel):
    incident_group: Optional["GetIncidentGroupIncidentGroup"] = Field(
        alias="incidentGroup"
    )


class GetIncidentGroupIncidentGroup(BaseModel):
    id: Any
    status: IncidentStatus
    priority: IncidentGroupPriority
    owner: Optional["GetIncidentGroupIncidentGroupOwner"]
    source: "GetIncidentGroupIncidentGroupSource"
    validator: Union[
        "GetIncidentGroupIncidentGroupValidatorValidator",
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidator",
        "GetIncidentGroupIncidentGroupValidatorFreshnessValidator",
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidator",
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidator",
        "GetIncidentGroupIncidentGroupValidatorNumericValidator",
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidator",
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidator",
        "GetIncidentGroupIncidentGroupValidatorSqlValidator",
        "GetIncidentGroupIncidentGroupValidatorVolumeValidator",
    ] = Field(discriminator="typename__")
    segment: "GetIncidentGroupIncidentGroupSegment"
    severity_stats: "GetIncidentGroupIncidentGroupSeverityStats" = Field(
        alias="severityStats"
    )
    first_seen_at: datetime = Field(alias="firstSeenAt")
    last_seen_at: datetime = Field(alias="lastSeenAt")


class GetIncidentGroupIncidentGroupOwner(BaseModel):
    id: Any
    display_name: str = Field(alias="displayName")


class GetIncidentGroupIncidentGroupSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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


class GetIncidentGroupIncidentGroupValidatorValidator(BaseModel):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorValidatorTags"]


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfig(BaseModel):
    source: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigWindow"
    segmentation: (
        "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
        "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceNamespace"
    )


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigWindowNamespace"
    )


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidator(BaseModel):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorNamespace"
    tags: List[
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorTags"
    ]
    config: (
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfig"
    )
    reference_source_config: (
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorTags(
    BaseModel
):
    key: str
    value: Optional[str]


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidator(BaseModel):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorFreshnessValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfig"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfig(BaseModel):
    source: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfig(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidator(BaseModel):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfig"
    reference_source_config: (
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidator(BaseModel):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorNamespace"
    )
    tags: List["GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfig"
    reference_source_config: (
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorNumericValidator(BaseModel):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorNumericValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorNumericValidatorConfig"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfig(BaseModel):
    source: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigWindow"
    segmentation: (
        "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetIncidentGroupIncidentGroupValidatorNumericValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidator(BaseModel):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfig(
    BaseModel
):
    source: (
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSource"
    )
    window: (
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigWindow"
    )
    segmentation: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfig(BaseModel):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidator(BaseModel):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfig"
    reference_source_config: (
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorSqlValidator(BaseModel):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorSqlValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorSqlValidatorConfig"


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfig(BaseModel):
    source: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigWindow"
    segmentation: (
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceNamespace"
    )


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigWindowNamespace"
    )


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetIncidentGroupIncidentGroupValidatorSqlValidatorConfig(BaseModel):
    query: str
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorVolumeValidator(BaseModel):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    description: Optional[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    has_custom_name: bool = Field(alias="hasCustomName")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorVolumeValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfig"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfig(BaseModel):
    source: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigWindow"
    segmentation: (
        "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]
    source_filter: Optional[
        Annotated[
            Union[
                "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterFilter",
                "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter",
                "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter",
                "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilter",
                "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter",
                "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilter",
                "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="sourceFilter")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSource(
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
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterFilter(
    BaseModel
):
    typename__: Literal["Filter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter(
    BaseModel
):
    typename__: Literal["BooleanFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: BooleanOperator = Field(alias="booleanOperator")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter(
    BaseModel
):
    typename__: Literal["EnumFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterConfig"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterConfig(
    BaseModel
):
    field: JsonPointer
    values: List[str]
    operator: EnumOperator = Field(alias="enumOperator")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilter(
    BaseModel
):
    typename__: Literal["NullFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilterConfig"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilterConfig(
    BaseModel
):
    field: JsonPointer
    operator: NullOperator = Field(alias="nullOperator")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter(
    BaseModel
):
    typename__: Literal["SqlFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterConfig"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterConfig(
    BaseModel
):
    query: str


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilter(
    BaseModel
):
    typename__: Literal["StringFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilterConfig"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: Optional[str] = Field(alias="stringValue")
    operator: StringOperator = Field(alias="stringOperator")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter(
    BaseModel
):
    typename__: Literal["ThresholdFilter"] = Field(alias="__typename")
    id: Any
    name: str
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace"
    resource_name: str = Field(alias="resourceName")
    source: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource(
    BaseModel
):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace"
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterConfig(
    BaseModel
):
    field: JsonPointer
    value: float = Field(alias="thresholdValue")
    operator: ComparisonOperator = Field(alias="thresholdOperator")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorTags(BaseModel):
    key: str
    value: Optional[str]


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupSegment(SegmentDetails):
    pass


class GetIncidentGroupIncidentGroupSeverityStats(BaseModel):
    high_count: int = Field(alias="highCount")
    medium_count: int = Field(alias="mediumCount")
    low_count: int = Field(alias="lowCount")
    total_count: int = Field(alias="totalCount")


GetIncidentGroup.model_rebuild()
GetIncidentGroupIncidentGroup.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterBooleanFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterEnumFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterNullFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterSqlFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterStringFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilter.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceFilterThresholdFilterSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfig.model_rebuild()
