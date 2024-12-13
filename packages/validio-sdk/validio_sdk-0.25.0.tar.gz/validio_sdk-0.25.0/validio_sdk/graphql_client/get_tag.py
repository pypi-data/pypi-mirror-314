from typing import Optional

from .base_model import BaseModel
from .fragments import TagDetails


class GetTag(BaseModel):
    tag: Optional["GetTagTag"]


class GetTagTag(TagDetails):
    pass


GetTag.model_rebuild()
