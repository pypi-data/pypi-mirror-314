from pydantic import Field

from .base_model import BaseModel
from .fragments import UserDeletion


class DeleteUser(BaseModel):
    user_delete: "DeleteUserUserDelete" = Field(alias="userDelete")


class DeleteUserUserDelete(UserDeletion):
    pass


DeleteUser.model_rebuild()
