from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic import Field

from validio_sdk.scalars import JsonPointer, SourceId, ValidatorId

from .base_model import BaseModel
from .enums import IncidentGroupPriority, IncidentStatus


class GetSourceIncidentGroups(BaseModel):
    source: Optional["GetSourceIncidentGroupsSource"]


class GetSourceIncidentGroupsSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    incident_groups: "GetSourceIncidentGroupsSourceIncidentGroups" = Field(
        alias="incidentGroups"
    )


class GetSourceIncidentGroupsSourceIncidentGroups(BaseModel):
    elements: List["GetSourceIncidentGroupsSourceIncidentGroupsElements"]
    index: "GetSourceIncidentGroupsSourceIncidentGroupsIndex"
    page_info: "GetSourceIncidentGroupsSourceIncidentGroupsPageInfo" = Field(
        alias="pageInfo"
    )


class GetSourceIncidentGroupsSourceIncidentGroupsElements(BaseModel):
    id: Any
    status: IncidentStatus
    priority: IncidentGroupPriority
    owner: Optional["GetSourceIncidentGroupsSourceIncidentGroupsElementsOwner"]
    source: "GetSourceIncidentGroupsSourceIncidentGroupsElementsSource"
    validator: "GetSourceIncidentGroupsSourceIncidentGroupsElementsValidator"
    segment: "GetSourceIncidentGroupsSourceIncidentGroupsElementsSegment"
    severity_stats: (
        "GetSourceIncidentGroupsSourceIncidentGroupsElementsSeverityStats"
    ) = Field(alias="severityStats")
    first_seen_at: datetime = Field(alias="firstSeenAt")
    last_seen_at: datetime = Field(alias="lastSeenAt")


class GetSourceIncidentGroupsSourceIncidentGroupsElementsOwner(BaseModel):
    id: Any
    display_name: str = Field(alias="displayName")


class GetSourceIncidentGroupsSourceIncidentGroupsElementsSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetSourceIncidentGroupsSourceIncidentGroupsElementsSourceNamespace"


class GetSourceIncidentGroupsSourceIncidentGroupsElementsSourceNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class GetSourceIncidentGroupsSourceIncidentGroupsElementsValidator(BaseModel):
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
    id: ValidatorId
    name: str


class GetSourceIncidentGroupsSourceIncidentGroupsElementsSegment(BaseModel):
    fields: List["GetSourceIncidentGroupsSourceIncidentGroupsElementsSegmentFields"]


class GetSourceIncidentGroupsSourceIncidentGroupsElementsSegmentFields(BaseModel):
    field: JsonPointer
    value: str


class GetSourceIncidentGroupsSourceIncidentGroupsElementsSeverityStats(BaseModel):
    high_count: int = Field(alias="highCount")
    medium_count: int = Field(alias="mediumCount")
    low_count: int = Field(alias="lowCount")
    total_count: int = Field(alias="totalCount")


class GetSourceIncidentGroupsSourceIncidentGroupsIndex(BaseModel):
    owner: List["GetSourceIncidentGroupsSourceIncidentGroupsIndexOwner"]
    status: List["GetSourceIncidentGroupsSourceIncidentGroupsIndexStatus"]
    priority: List["GetSourceIncidentGroupsSourceIncidentGroupsIndexPriority"]
    validator: List["GetSourceIncidentGroupsSourceIncidentGroupsIndexValidator"]


class GetSourceIncidentGroupsSourceIncidentGroupsIndexOwner(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetSourceIncidentGroupsSourceIncidentGroupsIndexStatus(BaseModel):
    value: str
    count: int


class GetSourceIncidentGroupsSourceIncidentGroupsIndexPriority(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetSourceIncidentGroupsSourceIncidentGroupsIndexValidator(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetSourceIncidentGroupsSourceIncidentGroupsPageInfo(BaseModel):
    start_cursor: Optional[str] = Field(alias="startCursor")
    end_cursor: Optional[str] = Field(alias="endCursor")
    has_next_page: Optional[bool] = Field(alias="hasNextPage")
    has_previous_page: Optional[bool] = Field(alias="hasPreviousPage")
    filtered_count: int = Field(alias="filteredCount")
    total_count: int = Field(alias="totalCount")


GetSourceIncidentGroups.model_rebuild()
GetSourceIncidentGroupsSource.model_rebuild()
GetSourceIncidentGroupsSourceIncidentGroups.model_rebuild()
GetSourceIncidentGroupsSourceIncidentGroupsElements.model_rebuild()
GetSourceIncidentGroupsSourceIncidentGroupsElementsSource.model_rebuild()
GetSourceIncidentGroupsSourceIncidentGroupsElementsSegment.model_rebuild()
GetSourceIncidentGroupsSourceIncidentGroupsIndex.model_rebuild()
