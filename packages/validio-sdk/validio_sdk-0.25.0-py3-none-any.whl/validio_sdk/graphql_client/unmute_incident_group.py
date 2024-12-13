from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class UnmuteIncidentGroup(BaseModel):
    incident_group_unmute: "UnmuteIncidentGroupIncidentGroupUnmute" = Field(
        alias="incidentGroupUnmute"
    )


class UnmuteIncidentGroupIncidentGroupUnmute(BaseModel):
    errors: List["UnmuteIncidentGroupIncidentGroupUnmuteErrors"]


class UnmuteIncidentGroupIncidentGroupUnmuteErrors(ErrorDetails):
    pass


UnmuteIncidentGroup.model_rebuild()
UnmuteIncidentGroupIncidentGroupUnmute.model_rebuild()
