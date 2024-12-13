from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class MuteIncidents(BaseModel):
    incidents_mute: "MuteIncidentsIncidentsMute" = Field(alias="incidentsMute")


class MuteIncidentsIncidentsMute(BaseModel):
    errors: List["MuteIncidentsIncidentsMuteErrors"]


class MuteIncidentsIncidentsMuteErrors(ErrorDetails):
    pass


MuteIncidents.model_rebuild()
MuteIncidentsIncidentsMute.model_rebuild()
