from typing import List

from .base_model import BaseModel
from .fragments import TeamDetails


class GetTeams(BaseModel):
    teams: List["GetTeamsTeams"]


class GetTeamsTeams(TeamDetails):
    pass


GetTeams.model_rebuild()
