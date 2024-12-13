from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class UnmuteSource(BaseModel):
    source_unmute: "UnmuteSourceSourceUnmute" = Field(alias="sourceUnmute")


class UnmuteSourceSourceUnmute(BaseModel):
    errors: List["UnmuteSourceSourceUnmuteErrors"]


class UnmuteSourceSourceUnmuteErrors(ErrorDetails):
    pass


UnmuteSource.model_rebuild()
UnmuteSourceSourceUnmute.model_rebuild()
