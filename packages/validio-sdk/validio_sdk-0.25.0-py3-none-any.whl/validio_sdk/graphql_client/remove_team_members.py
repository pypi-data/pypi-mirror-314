from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails, TeamDetails


class RemoveTeamMembers(BaseModel):
    team_members_remove: "RemoveTeamMembersTeamMembersRemove" = Field(
        alias="teamMembersRemove"
    )


class RemoveTeamMembersTeamMembersRemove(BaseModel):
    errors: List["RemoveTeamMembersTeamMembersRemoveErrors"]
    team: Optional["RemoveTeamMembersTeamMembersRemoveTeam"]


class RemoveTeamMembersTeamMembersRemoveErrors(ErrorDetails):
    pass


class RemoveTeamMembersTeamMembersRemoveTeam(TeamDetails):
    pass


RemoveTeamMembers.model_rebuild()
RemoveTeamMembersTeamMembersRemove.model_rebuild()
