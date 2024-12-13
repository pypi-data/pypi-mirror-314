from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterUpdate


class UpdateSqlFilter(BaseModel):
    sql_filter_update: "UpdateSqlFilterSqlFilterUpdate" = Field(alias="sqlFilterUpdate")


class UpdateSqlFilterSqlFilterUpdate(FilterUpdate):
    pass


UpdateSqlFilter.model_rebuild()
