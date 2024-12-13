from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic import Field

from validio_sdk.scalars import ValidatorId

from .base_model import BaseModel
from .enums import IncidentSeverity, IncidentStatus, MetricValueFormat


class GetValidatorIncidents(BaseModel):
    validator: Optional["GetValidatorIncidentsValidator"]


class GetValidatorIncidentsValidator(BaseModel):
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
    metric_value_format: MetricValueFormat = Field(alias="metricValueFormat")
    incidents: List["GetValidatorIncidentsValidatorIncidents"]


class GetValidatorIncidentsValidatorIncidents(BaseModel):
    id: Any
    group: "GetValidatorIncidentsValidatorIncidentsGroup"
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


class GetValidatorIncidentsValidatorIncidentsGroup(BaseModel):
    id: Any


GetValidatorIncidents.model_rebuild()
GetValidatorIncidentsValidator.model_rebuild()
GetValidatorIncidentsValidatorIncidents.model_rebuild()
