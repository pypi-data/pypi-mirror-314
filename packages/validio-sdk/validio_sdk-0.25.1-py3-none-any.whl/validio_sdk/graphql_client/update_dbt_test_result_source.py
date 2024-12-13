from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateDbtTestResultSource(BaseModel):
    dbt_test_result_source_update: (
        "UpdateDbtTestResultSourceDbtTestResultSourceUpdate"
    ) = Field(alias="dbtTestResultSourceUpdate")


class UpdateDbtTestResultSourceDbtTestResultSourceUpdate(SourceUpdate):
    pass


UpdateDbtTestResultSource.model_rebuild()
