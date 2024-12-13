from typing import List

from pydantic import Field

from .base_model import BaseModel
from .enums import ApiErrorCode


class UpdateIncidentGroupOwner(BaseModel):
    incident_group_owner_update: "UpdateIncidentGroupOwnerIncidentGroupOwnerUpdate" = (
        Field(alias="incidentGroupOwnerUpdate")
    )


class UpdateIncidentGroupOwnerIncidentGroupOwnerUpdate(BaseModel):
    errors: List["UpdateIncidentGroupOwnerIncidentGroupOwnerUpdateErrors"]


class UpdateIncidentGroupOwnerIncidentGroupOwnerUpdateErrors(BaseModel):
    code: ApiErrorCode
    message: str


UpdateIncidentGroupOwner.model_rebuild()
UpdateIncidentGroupOwnerIncidentGroupOwnerUpdate.model_rebuild()
