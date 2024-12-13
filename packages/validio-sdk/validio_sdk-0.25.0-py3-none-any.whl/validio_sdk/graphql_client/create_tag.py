from pydantic import Field

from .base_model import BaseModel
from .fragments import TagCreation


class CreateTag(BaseModel):
    tag_create: "CreateTagTagCreate" = Field(alias="tagCreate")


class CreateTagTagCreate(TagCreation):
    pass


CreateTag.model_rebuild()
