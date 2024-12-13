from typing import Optional

from .base_model import BaseModel
from .fragments import TeamDetails


class GetTeam(BaseModel):
    team: Optional["GetTeamTeam"]


class GetTeamTeam(TeamDetails):
    pass


GetTeam.model_rebuild()
