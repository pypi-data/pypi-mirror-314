from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails, TeamDetails


class CreateTeam(BaseModel):
    team_create: "CreateTeamTeamCreate" = Field(alias="teamCreate")


class CreateTeamTeamCreate(BaseModel):
    errors: List["CreateTeamTeamCreateErrors"]
    team: Optional["CreateTeamTeamCreateTeam"]


class CreateTeamTeamCreateErrors(ErrorDetails):
    pass


class CreateTeamTeamCreateTeam(TeamDetails):
    pass


CreateTeam.model_rebuild()
CreateTeamTeamCreate.model_rebuild()
