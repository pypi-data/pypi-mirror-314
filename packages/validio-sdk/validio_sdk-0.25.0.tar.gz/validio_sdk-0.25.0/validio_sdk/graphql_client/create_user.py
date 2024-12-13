from pydantic import Field

from .base_model import BaseModel
from .fragments import UserCreation


class CreateUser(BaseModel):
    user_create: "CreateUserUserCreate" = Field(alias="userCreate")


class CreateUserUserCreate(UserCreation):
    pass


CreateUser.model_rebuild()
