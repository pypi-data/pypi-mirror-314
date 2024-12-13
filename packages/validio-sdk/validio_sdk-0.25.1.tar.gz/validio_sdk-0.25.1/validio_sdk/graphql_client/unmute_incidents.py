from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class UnmuteIncidents(BaseModel):
    incidents_unmute: "UnmuteIncidentsIncidentsUnmute" = Field(alias="incidentsUnmute")


class UnmuteIncidentsIncidentsUnmute(BaseModel):
    errors: List["UnmuteIncidentsIncidentsUnmuteErrors"]


class UnmuteIncidentsIncidentsUnmuteErrors(ErrorDetails):
    pass


UnmuteIncidents.model_rebuild()
UnmuteIncidentsIncidentsUnmute.model_rebuild()
