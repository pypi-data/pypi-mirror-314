from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateDatabricksSource(BaseModel):
    databricks_source_update: "UpdateDatabricksSourceDatabricksSourceUpdate" = Field(
        alias="databricksSourceUpdate"
    )


class UpdateDatabricksSourceDatabricksSourceUpdate(SourceUpdate):
    pass


UpdateDatabricksSource.model_rebuild()
