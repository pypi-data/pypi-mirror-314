from pydantic import Field

from .base_model import BaseModel
from .fragments import WindowUpdate


class UpdateGlobalWindow(BaseModel):
    global_window_update: "UpdateGlobalWindowGlobalWindowUpdate" = Field(
        alias="globalWindowUpdate"
    )


class UpdateGlobalWindowGlobalWindowUpdate(WindowUpdate):
    pass


UpdateGlobalWindow.model_rebuild()
