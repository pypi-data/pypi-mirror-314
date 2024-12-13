from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceCreation


class CreateDatabricksSource(BaseModel):
    databricks_source_create: "CreateDatabricksSourceDatabricksSourceCreate" = Field(
        alias="databricksSourceCreate"
    )


class CreateDatabricksSourceDatabricksSourceCreate(SourceCreation):
    pass


CreateDatabricksSource.model_rebuild()
