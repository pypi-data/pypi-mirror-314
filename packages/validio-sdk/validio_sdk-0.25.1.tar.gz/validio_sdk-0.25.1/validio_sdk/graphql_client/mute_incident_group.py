from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class MuteIncidentGroup(BaseModel):
    incident_group_mute: "MuteIncidentGroupIncidentGroupMute" = Field(
        alias="incidentGroupMute"
    )


class MuteIncidentGroupIncidentGroupMute(BaseModel):
    errors: List["MuteIncidentGroupIncidentGroupMuteErrors"]


class MuteIncidentGroupIncidentGroupMuteErrors(ErrorDetails):
    pass


MuteIncidentGroup.model_rebuild()
MuteIncidentGroupIncidentGroupMute.model_rebuild()
