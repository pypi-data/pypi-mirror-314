from pydantic import Field

from .base_model import BaseModel
from .fragments import TagUpdate


class UpdateTag(BaseModel):
    tag_update: "UpdateTagTagUpdate" = Field(alias="tagUpdate")


class UpdateTagTagUpdate(TagUpdate):
    pass


UpdateTag.model_rebuild()
