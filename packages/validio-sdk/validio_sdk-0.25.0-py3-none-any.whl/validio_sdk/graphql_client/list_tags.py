from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import TagDetails


class ListTags(BaseModel):
    tags_list: List["ListTagsTagsList"] = Field(alias="tagsList")


class ListTagsTagsList(TagDetails):
    pass


ListTags.model_rebuild()
