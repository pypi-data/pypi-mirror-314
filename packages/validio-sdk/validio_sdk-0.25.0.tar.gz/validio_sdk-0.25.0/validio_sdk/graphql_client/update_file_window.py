from pydantic import Field

from .base_model import BaseModel
from .fragments import WindowUpdate


class UpdateFileWindow(BaseModel):
    file_window_update: "UpdateFileWindowFileWindowUpdate" = Field(
        alias="fileWindowUpdate"
    )


class UpdateFileWindowFileWindowUpdate(WindowUpdate):
    pass


UpdateFileWindow.model_rebuild()
