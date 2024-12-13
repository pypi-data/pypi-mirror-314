from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateDbtModelRunSource(BaseModel):
    dbt_model_run_source_update: "UpdateDbtModelRunSourceDbtModelRunSourceUpdate" = (
        Field(alias="dbtModelRunSourceUpdate")
    )


class UpdateDbtModelRunSourceDbtModelRunSourceUpdate(SourceUpdate):
    pass


UpdateDbtModelRunSource.model_rebuild()
