from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails, TeamDetails


class AddTeamMembers(BaseModel):
    team_members_add: "AddTeamMembersTeamMembersAdd" = Field(alias="teamMembersAdd")


class AddTeamMembersTeamMembersAdd(BaseModel):
    errors: List["AddTeamMembersTeamMembersAddErrors"]
    team: Optional["AddTeamMembersTeamMembersAddTeam"]


class AddTeamMembersTeamMembersAddErrors(ErrorDetails):
    pass


class AddTeamMembersTeamMembersAddTeam(TeamDetails):
    pass


AddTeamMembers.model_rebuild()
AddTeamMembersTeamMembersAdd.model_rebuild()
