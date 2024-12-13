from typing import List, Literal, Optional

from pydantic import Field

from validio_sdk.scalars import ValidatorId

from .base_model import BaseModel
from .enums import SourceState


class GetSourceRecommendedValidators(BaseModel):
    source: Optional["GetSourceRecommendedValidatorsSource"]


class GetSourceRecommendedValidatorsSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    state: SourceState
    recommended_validators: List[
        "GetSourceRecommendedValidatorsSourceRecommendedValidators"
    ] = Field(alias="recommendedValidators")


class GetSourceRecommendedValidatorsSourceRecommendedValidators(BaseModel):
    id: ValidatorId
    typename__: Literal[
        "CategoricalDistributionValidator",
        "FreshnessValidator",
        "NumericAnomalyValidator",
        "NumericDistributionValidator",
        "NumericValidator",
        "RelativeTimeValidator",
        "RelativeVolumeValidator",
        "SqlValidator",
        "Validator",
        "VolumeValidator",
    ] = Field(alias="__typename")
    name: str
    source_config: (
        "GetSourceRecommendedValidatorsSourceRecommendedValidatorsSourceConfig"
    ) = Field(alias="sourceConfig")


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsSourceConfig(BaseModel):
    segmentation: "GetSourceRecommendedValidatorsSourceRecommendedValidatorsSourceConfigSegmentation"


class GetSourceRecommendedValidatorsSourceRecommendedValidatorsSourceConfigSegmentation(
    BaseModel
):
    name: str


GetSourceRecommendedValidators.model_rebuild()
GetSourceRecommendedValidatorsSource.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidators.model_rebuild()
GetSourceRecommendedValidatorsSourceRecommendedValidatorsSourceConfig.model_rebuild()
