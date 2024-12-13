from typing import List

from pydantic import Field

from .base_model import BaseModel
from .enums import ApiErrorCode


class UpdateIncidentGroupStatus(BaseModel):
    incident_group_status_update: (
        "UpdateIncidentGroupStatusIncidentGroupStatusUpdate"
    ) = Field(alias="incidentGroupStatusUpdate")


class UpdateIncidentGroupStatusIncidentGroupStatusUpdate(BaseModel):
    errors: List["UpdateIncidentGroupStatusIncidentGroupStatusUpdateErrors"]


class UpdateIncidentGroupStatusIncidentGroupStatusUpdateErrors(BaseModel):
    code: ApiErrorCode
    message: str


UpdateIncidentGroupStatus.model_rebuild()
UpdateIncidentGroupStatusIncidentGroupStatusUpdate.model_rebuild()
