from pydantic import Field

from .base_model import BaseModel


class StartDatabricksWarehouse(BaseModel):
    databricks_start_warehouse: bool = Field(alias="databricksStartWarehouse")
