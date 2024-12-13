from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdatePostgreSqlSource(BaseModel):
    postgre_sql_source_update: "UpdatePostgreSqlSourcePostgreSqlSourceUpdate" = Field(
        alias="postgreSqlSourceUpdate"
    )


class UpdatePostgreSqlSourcePostgreSqlSourceUpdate(SourceUpdate):
    pass


UpdatePostgreSqlSource.model_rebuild()
