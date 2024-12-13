from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteTeam(BaseModel):
    team_delete: "DeleteTeamTeamDelete" = Field(alias="teamDelete")


class DeleteTeamTeamDelete(BaseModel):
    errors: List["DeleteTeamTeamDeleteErrors"]


class DeleteTeamTeamDeleteErrors(ErrorDetails):
    pass


DeleteTeam.model_rebuild()
DeleteTeamTeamDelete.model_rebuild()
