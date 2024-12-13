from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceCreation


class CreateClickHouseSource(BaseModel):
    click_house_source_create: "CreateClickHouseSourceClickHouseSourceCreate" = Field(
        alias="clickHouseSourceCreate"
    )


class CreateClickHouseSourceClickHouseSourceCreate(SourceCreation):
    pass


CreateClickHouseSource.model_rebuild()
