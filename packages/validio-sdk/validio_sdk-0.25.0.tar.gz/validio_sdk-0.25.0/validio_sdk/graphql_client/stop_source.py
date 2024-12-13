from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import SourceState
from .fragments import ErrorDetails


class StopSource(BaseModel):
    source_stop: "StopSourceSourceStop" = Field(alias="sourceStop")


class StopSourceSourceStop(BaseModel):
    errors: List["StopSourceSourceStopErrors"]
    state: Optional[SourceState]


class StopSourceSourceStopErrors(ErrorDetails):
    pass


StopSource.model_rebuild()
StopSourceSourceStop.model_rebuild()
