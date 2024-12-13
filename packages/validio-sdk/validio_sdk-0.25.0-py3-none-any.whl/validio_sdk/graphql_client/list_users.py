from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import UserDetails


class ListUsers(BaseModel):
    users_list: List["ListUsersUsersList"] = Field(alias="usersList")


class ListUsersUsersList(UserDetails):
    pass


ListUsers.model_rebuild()
