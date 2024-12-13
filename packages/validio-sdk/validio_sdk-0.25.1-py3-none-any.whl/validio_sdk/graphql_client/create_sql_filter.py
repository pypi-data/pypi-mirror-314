from pydantic import Field

from .base_model import BaseModel
from .fragments import FilterCreation


class CreateSqlFilter(BaseModel):
    sql_filter_create: "CreateSqlFilterSqlFilterCreate" = Field(alias="sqlFilterCreate")


class CreateSqlFilterSqlFilterCreate(FilterCreation):
    pass


CreateSqlFilter.model_rebuild()
