from typing import List

from pydantic import Field

from .base_model import BaseModel
from .enums import ApiErrorCode


class UpdateIncidentStatus(BaseModel):
    incident_status_update: "UpdateIncidentStatusIncidentStatusUpdate" = Field(
        alias="incidentStatusUpdate"
    )


class UpdateIncidentStatusIncidentStatusUpdate(BaseModel):
    errors: List["UpdateIncidentStatusIncidentStatusUpdateErrors"]


class UpdateIncidentStatusIncidentStatusUpdateErrors(BaseModel):
    code: ApiErrorCode
    message: str


UpdateIncidentStatus.model_rebuild()
UpdateIncidentStatusIncidentStatusUpdate.model_rebuild()
