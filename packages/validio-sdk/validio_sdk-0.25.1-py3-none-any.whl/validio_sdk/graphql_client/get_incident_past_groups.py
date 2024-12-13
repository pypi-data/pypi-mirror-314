from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic import Field

from validio_sdk.scalars import JsonPointer, ValidatorId

from .base_model import BaseModel
from .enums import IncidentGroupPriority, IncidentStatus


class GetIncidentPastGroups(BaseModel):
    incident_group: Optional["GetIncidentPastGroupsIncidentGroup"] = Field(
        alias="incidentGroup"
    )


class GetIncidentPastGroupsIncidentGroup(BaseModel):
    past_groups: "GetIncidentPastGroupsIncidentGroupPastGroups" = Field(
        alias="pastGroups"
    )


class GetIncidentPastGroupsIncidentGroupPastGroups(BaseModel):
    elements: List["GetIncidentPastGroupsIncidentGroupPastGroupsElements"]
    index: "GetIncidentPastGroupsIncidentGroupPastGroupsIndex"
    page_info: "GetIncidentPastGroupsIncidentGroupPastGroupsPageInfo" = Field(
        alias="pageInfo"
    )


class GetIncidentPastGroupsIncidentGroupPastGroupsElements(BaseModel):
    id: Any
    status: IncidentStatus
    priority: IncidentGroupPriority
    owner: Optional["GetIncidentPastGroupsIncidentGroupPastGroupsElementsOwner"]
    validator: "GetIncidentPastGroupsIncidentGroupPastGroupsElementsValidator"
    segment: "GetIncidentPastGroupsIncidentGroupPastGroupsElementsSegment"
    severity_stats: (
        "GetIncidentPastGroupsIncidentGroupPastGroupsElementsSeverityStats"
    ) = Field(alias="severityStats")
    first_seen_at: datetime = Field(alias="firstSeenAt")
    last_seen_at: datetime = Field(alias="lastSeenAt")


class GetIncidentPastGroupsIncidentGroupPastGroupsElementsOwner(BaseModel):
    id: Any
    display_name: str = Field(alias="displayName")


class GetIncidentPastGroupsIncidentGroupPastGroupsElementsValidator(BaseModel):
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


class GetIncidentPastGroupsIncidentGroupPastGroupsElementsSegment(BaseModel):
    fields: List["GetIncidentPastGroupsIncidentGroupPastGroupsElementsSegmentFields"]


class GetIncidentPastGroupsIncidentGroupPastGroupsElementsSegmentFields(BaseModel):
    field: JsonPointer
    value: str


class GetIncidentPastGroupsIncidentGroupPastGroupsElementsSeverityStats(BaseModel):
    high_count: int = Field(alias="highCount")
    medium_count: int = Field(alias="mediumCount")
    low_count: int = Field(alias="lowCount")
    total_count: int = Field(alias="totalCount")


class GetIncidentPastGroupsIncidentGroupPastGroupsIndex(BaseModel):
    owner: List["GetIncidentPastGroupsIncidentGroupPastGroupsIndexOwner"]
    status: List["GetIncidentPastGroupsIncidentGroupPastGroupsIndexStatus"]
    priority: List["GetIncidentPastGroupsIncidentGroupPastGroupsIndexPriority"]


class GetIncidentPastGroupsIncidentGroupPastGroupsIndexOwner(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetIncidentPastGroupsIncidentGroupPastGroupsIndexStatus(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetIncidentPastGroupsIncidentGroupPastGroupsIndexPriority(BaseModel):
    label: Optional[str]
    value: str
    count: int


class GetIncidentPastGroupsIncidentGroupPastGroupsPageInfo(BaseModel):
    start_cursor: Optional[str] = Field(alias="startCursor")
    end_cursor: Optional[str] = Field(alias="endCursor")
    has_next_page: Optional[bool] = Field(alias="hasNextPage")
    has_previous_page: Optional[bool] = Field(alias="hasPreviousPage")
    filtered_count: int = Field(alias="filteredCount")
    total_count: int = Field(alias="totalCount")


GetIncidentPastGroups.model_rebuild()
GetIncidentPastGroupsIncidentGroup.model_rebuild()
GetIncidentPastGroupsIncidentGroupPastGroups.model_rebuild()
GetIncidentPastGroupsIncidentGroupPastGroupsElements.model_rebuild()
GetIncidentPastGroupsIncidentGroupPastGroupsElementsSegment.model_rebuild()
GetIncidentPastGroupsIncidentGroupPastGroupsIndex.model_rebuild()
