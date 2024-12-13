from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteTags(BaseModel):
    tags_delete: "DeleteTagsTagsDelete" = Field(alias="tagsDelete")


class DeleteTagsTagsDelete(BaseModel):
    errors: List["DeleteTagsTagsDeleteErrors"]


class DeleteTagsTagsDeleteErrors(ErrorDetails):
    pass


DeleteTags.model_rebuild()
DeleteTagsTagsDelete.model_rebuild()
