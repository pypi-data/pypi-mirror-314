from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class MuteSource(BaseModel):
    source_mute: "MuteSourceSourceMute" = Field(alias="sourceMute")


class MuteSourceSourceMute(BaseModel):
    errors: List["MuteSourceSourceMuteErrors"]


class MuteSourceSourceMuteErrors(ErrorDetails):
    pass


MuteSource.model_rebuild()
MuteSourceSourceMute.model_rebuild()
