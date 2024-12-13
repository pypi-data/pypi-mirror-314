from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import SourcePollProgressStatus
from .fragments import ErrorDetails


class GetSourceManualPollProgress(BaseModel):
    source_manual_poll_progress: (
        "GetSourceManualPollProgressSourceManualPollProgress"
    ) = Field(alias="sourceManualPollProgress")


class GetSourceManualPollProgressSourceManualPollProgress(BaseModel):
    errors: List["GetSourceManualPollProgressSourceManualPollProgressErrors"]
    status: Optional[SourcePollProgressStatus]
    description: Optional[str]


class GetSourceManualPollProgressSourceManualPollProgressErrors(ErrorDetails):
    pass


GetSourceManualPollProgress.model_rebuild()
GetSourceManualPollProgressSourceManualPollProgress.model_rebuild()
