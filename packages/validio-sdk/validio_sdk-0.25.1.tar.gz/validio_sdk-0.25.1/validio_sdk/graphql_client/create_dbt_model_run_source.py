from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceCreation


class CreateDbtModelRunSource(BaseModel):
    dbt_model_run_source_create: "CreateDbtModelRunSourceDbtModelRunSourceCreate" = (
        Field(alias="dbtModelRunSourceCreate")
    )


class CreateDbtModelRunSourceDbtModelRunSourceCreate(SourceCreation):
    pass


CreateDbtModelRunSource.model_rebuild()
