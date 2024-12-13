from pydantic import Field

from .base_model import BaseModel
from .fragments import UserUpdate


class UpdateUser(BaseModel):
    user_update: "UpdateUserUserUpdate" = Field(alias="userUpdate")


class UpdateUserUserUpdate(UserUpdate):
    pass


UpdateUser.model_rebuild()
