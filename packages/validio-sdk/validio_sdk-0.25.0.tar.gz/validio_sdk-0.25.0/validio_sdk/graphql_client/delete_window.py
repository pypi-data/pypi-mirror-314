from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteWindow(BaseModel):
    windows_delete: "DeleteWindowWindowsDelete" = Field(alias="windowsDelete")


class DeleteWindowWindowsDelete(BaseModel):
    errors: List["DeleteWindowWindowsDeleteErrors"]


class DeleteWindowWindowsDeleteErrors(ErrorDetails):
    pass


DeleteWindow.model_rebuild()
DeleteWindowWindowsDelete.model_rebuild()
