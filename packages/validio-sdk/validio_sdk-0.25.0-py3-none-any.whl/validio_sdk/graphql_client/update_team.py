from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails, TeamDetails


class UpdateTeam(BaseModel):
    team_update: "UpdateTeamTeamUpdate" = Field(alias="teamUpdate")


class UpdateTeamTeamUpdate(BaseModel):
    errors: List["UpdateTeamTeamUpdateErrors"]
    team: Optional["UpdateTeamTeamUpdateTeam"]


class UpdateTeamTeamUpdateErrors(ErrorDetails):
    pass


class UpdateTeamTeamUpdateTeam(TeamDetails):
    pass


UpdateTeam.model_rebuild()
UpdateTeamTeamUpdate.model_rebuild()
