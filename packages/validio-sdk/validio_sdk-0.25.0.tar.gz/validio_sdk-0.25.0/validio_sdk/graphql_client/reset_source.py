from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class ResetSource(BaseModel):
    source_reset: "ResetSourceSourceReset" = Field(alias="sourceReset")


class ResetSourceSourceReset(BaseModel):
    errors: List["ResetSourceSourceResetErrors"]


class ResetSourceSourceResetErrors(ErrorDetails):
    pass


ResetSource.model_rebuild()
ResetSourceSourceReset.model_rebuild()
