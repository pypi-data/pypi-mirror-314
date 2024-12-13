from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateClickHouseSource(BaseModel):
    click_house_source_update: "UpdateClickHouseSourceClickHouseSourceUpdate" = Field(
        alias="clickHouseSourceUpdate"
    )


class UpdateClickHouseSourceClickHouseSourceUpdate(SourceUpdate):
    pass


UpdateClickHouseSource.model_rebuild()
