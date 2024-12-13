from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceCreation


class CreateDemoSource(BaseModel):
    demo_source_create: "CreateDemoSourceDemoSourceCreate" = Field(
        alias="demoSourceCreate"
    )


class CreateDemoSourceDemoSourceCreate(SourceCreation):
    pass


CreateDemoSource.model_rebuild()
