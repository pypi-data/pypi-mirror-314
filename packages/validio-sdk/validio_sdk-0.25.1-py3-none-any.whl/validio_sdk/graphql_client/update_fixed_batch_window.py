from pydantic import Field

from .base_model import BaseModel
from .fragments import WindowUpdate


class UpdateFixedBatchWindow(BaseModel):
    fixed_batch_window_update: "UpdateFixedBatchWindowFixedBatchWindowUpdate" = Field(
        alias="fixedBatchWindowUpdate"
    )


class UpdateFixedBatchWindowFixedBatchWindowUpdate(WindowUpdate):
    pass


UpdateFixedBatchWindow.model_rebuild()
