from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateDemoSource(BaseModel):
    demo_source_update: "UpdateDemoSourceDemoSourceUpdate" = Field(
        alias="demoSourceUpdate"
    )


class UpdateDemoSourceDemoSourceUpdate(SourceUpdate):
    pass


UpdateDemoSource.model_rebuild()
