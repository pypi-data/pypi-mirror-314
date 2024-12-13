from pydantic import Field

from .base_model import BaseModel
from .fragments import WindowCreation


class CreateTumblingWindow(BaseModel):
    tumbling_window_create: "CreateTumblingWindowTumblingWindowCreate" = Field(
        alias="tumblingWindowCreate"
    )


class CreateTumblingWindowTumblingWindowCreate(WindowCreation):
    pass


CreateTumblingWindow.model_rebuild()
