from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class PollSourceManually(BaseModel):
    source_manual_poll: "PollSourceManuallySourceManualPoll" = Field(
        alias="sourceManualPoll"
    )


class PollSourceManuallySourceManualPoll(BaseModel):
    id: Optional[Any]
    errors: List["PollSourceManuallySourceManualPollErrors"]


class PollSourceManuallySourceManualPollErrors(ErrorDetails):
    pass


PollSourceManually.model_rebuild()
PollSourceManuallySourceManualPoll.model_rebuild()
