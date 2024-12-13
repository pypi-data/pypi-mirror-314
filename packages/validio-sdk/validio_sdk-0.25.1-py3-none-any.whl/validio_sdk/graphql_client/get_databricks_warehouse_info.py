from pydantic import Field

from .base_model import BaseModel


class GetDatabricksWarehouseInfo(BaseModel):
    databricks_warehouse_info: "GetDatabricksWarehouseInfoDatabricksWarehouseInfo" = (
        Field(alias="databricksWarehouseInfo")
    )


class GetDatabricksWarehouseInfoDatabricksWarehouseInfo(BaseModel):
    name: str
    state: str
    auto_stop_minutes: int = Field(alias="autoStopMinutes")


GetDatabricksWarehouseInfo.model_rebuild()
