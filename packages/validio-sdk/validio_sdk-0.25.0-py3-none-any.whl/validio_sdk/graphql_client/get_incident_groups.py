from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic import Field

from validio_sdk.scalars import JsonPointer, SourceId, ValidatorId

from .base_model import BaseModel
from .enums import IncidentGroupPriority, IncidentStatus


class GetIncidentGroups(BaseModel):
    incident_groups: "GetIncidentGroupsIncidentGroups" = Field(alias="incidentGroups")


class GetIncidentGroupsIncidentGroups(BaseModel):
    elements: List["GetIncidentGroupsIncidentGroupsElements"]
    index: "GetIncidentGroupsIncidentGroupsIndex"
    page_info: "GetIncidentGroupsIncidentGroupsPageInfo" = Field(alias="pageInfo")


class GetIncidentGroupsIncidentGroupsElements(BaseModel):
    id: Any
    status: IncidentStatus
    priority: IncidentGroupPriority
    mute_until: Optional[datetime] = Field(alias="muteUntil")
    owner: Optional["GetIncidentGroupsIncidentGroupsElementsOwner"]
    source: "GetIncidentGroupsIncidentGroupsElementsSource"
    validator: "GetIncidentGroupsIncidentGroupsElementsValidator"
    segment: "GetIncidentGroupsIncidentGroupsElementsSegment"
    severity_stats: "GetIncidentGroupsIncidentGroupsElementsSeverityStats" = Field(
        alias="severityStats"
    )
    first_seen_at: datetime = Field(alias="firstSeenAt")
    last_seen_at: datetime = Field(alias="lastSeenAt")


class GetIncidentGroupsIncidentGroupsElementsOwner(BaseModel):
    id: Any
    display_name: str = Field(alias="displayName")
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class GetIncidentGroupsIncidentGroupsElementsSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
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
    namespace: "GetIncidentGroupsIncidentGroupsElementsSourceNamespace"


class GetIncidentGroupsIncidentGroupsElementsSourceNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class GetIncidentGroupsIncidentGroupsElementsValidator(BaseModel):
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


class GetIncidentGroupsIncidentGroupsElementsSegment(BaseModel):
    fields: List["GetIncidentGroupsIncidentGroupsElementsSegmentFields"]


class GetIncidentGroupsIncidentGroupsElementsSegmentFields(BaseModel):
    field: JsonPointer
    value: str


class GetIncidentGroupsIncidentGroupsElementsSeverityStats(BaseModel):
    high_count: int = Field(alias="highCount")
    medium_count: int = Field(alias="mediumCount")
    low_count: int = Field(alias="lowCount")
    total_count: int = Field(alias="totalCount")


class GetIncidentGroupsIncidentGroupsIndex(BaseModel):
    source: List["GetIncidentGroupsIncidentGroupsIndexSource"]
    owner: List["GetIncidentGroupsIncidentGroupsIndexOwner"]
    status: List["GetIncidentGroupsIncidentGroupsIndexStatus"]
    priority: List["GetIncidentGroupsIncidentGroupsIndexPriority"]
    validator: List["GetIncidentGroupsIncidentGroupsIndexValidator"]
    tag_label: List["GetIncidentGroupsIncidentGroupsIndexTagLabel"] = Field(
        alias="tagLabel"
    )
    namespace: List["GetIncidentGroupsIncidentGroupsIndexNamespace"]


class GetIncidentGroupsIncidentGroupsIndexSource(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetIncidentGroupsIncidentGroupsIndexOwner(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetIncidentGroupsIncidentGroupsIndexStatus(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetIncidentGroupsIncidentGroupsIndexPriority(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetIncidentGroupsIncidentGroupsIndexValidator(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetIncidentGroupsIncidentGroupsIndexTagLabel(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetIncidentGroupsIncidentGroupsIndexNamespace(BaseModel):
    value: str
    count: int


class GetIncidentGroupsIncidentGroupsPageInfo(BaseModel):
    start_cursor: Optional[str] = Field(alias="startCursor")
    end_cursor: Optional[str] = Field(alias="endCursor")
    has_next_page: Optional[bool] = Field(alias="hasNextPage")
    has_previous_page: Optional[bool] = Field(alias="hasPreviousPage")
    filtered_count: int = Field(alias="filteredCount")
    total_count: int = Field(alias="totalCount")


GetIncidentGroups.model_rebuild()
GetIncidentGroupsIncidentGroups.model_rebuild()
GetIncidentGroupsIncidentGroupsElements.model_rebuild()
GetIncidentGroupsIncidentGroupsElementsSource.model_rebuild()
GetIncidentGroupsIncidentGroupsElementsSegment.model_rebuild()
GetIncidentGroupsIncidentGroupsIndex.model_rebuild()
