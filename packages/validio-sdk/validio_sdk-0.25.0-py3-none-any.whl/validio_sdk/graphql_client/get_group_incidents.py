from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import IncidentSeverity, IncidentStatus, MetricValueFormat


class GetGroupIncidents(BaseModel):
    incident_group: Optional["GetGroupIncidentsIncidentGroup"] = Field(
        alias="incidentGroup"
    )


class GetGroupIncidentsIncidentGroup(BaseModel):
    validator: "GetGroupIncidentsIncidentGroupValidator"
    incidents: "GetGroupIncidentsIncidentGroupIncidents"


class GetGroupIncidentsIncidentGroupValidator(BaseModel):
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
    metric_value_format: MetricValueFormat = Field(alias="metricValueFormat")


class GetGroupIncidentsIncidentGroupIncidents(BaseModel):
    elements: List["GetGroupIncidentsIncidentGroupIncidentsElements"]
    index: "GetGroupIncidentsIncidentGroupIncidentsIndex"
    page_info: "GetGroupIncidentsIncidentGroupIncidentsPageInfo" = Field(
        alias="pageInfo"
    )


class GetGroupIncidentsIncidentGroupIncidentsElements(BaseModel):
    id: Any
    value: float
    deviation: float
    lower_bound: Optional[float] = Field(alias="lowerBound")
    upper_bound: Optional[float] = Field(alias="upperBound")
    status: IncidentStatus
    severity: IncidentSeverity
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    backfill_mode: bool = Field(alias="backfillMode")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetGroupIncidentsIncidentGroupIncidentsIndex(BaseModel):
    severity: List["GetGroupIncidentsIncidentGroupIncidentsIndexSeverity"]
    status: List["GetGroupIncidentsIncidentGroupIncidentsIndexStatus"]


class GetGroupIncidentsIncidentGroupIncidentsIndexSeverity(BaseModel):
    value: str
    count: int


class GetGroupIncidentsIncidentGroupIncidentsIndexStatus(BaseModel):
    value: str
    count: int


class GetGroupIncidentsIncidentGroupIncidentsPageInfo(BaseModel):
    start_cursor: Optional[str] = Field(alias="startCursor")
    end_cursor: Optional[str] = Field(alias="endCursor")
    has_next_page: Optional[bool] = Field(alias="hasNextPage")
    has_previous_page: Optional[bool] = Field(alias="hasPreviousPage")
    filtered_count: int = Field(alias="filteredCount")
    total_count: int = Field(alias="totalCount")


GetGroupIncidents.model_rebuild()
GetGroupIncidentsIncidentGroup.model_rebuild()
GetGroupIncidentsIncidentGroupIncidents.model_rebuild()
GetGroupIncidentsIncidentGroupIncidentsIndex.model_rebuild()
