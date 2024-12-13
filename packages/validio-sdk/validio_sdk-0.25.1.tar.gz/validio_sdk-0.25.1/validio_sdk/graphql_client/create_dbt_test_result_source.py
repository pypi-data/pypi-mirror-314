from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceCreation


class CreateDbtTestResultSource(BaseModel):
    dbt_test_result_source_create: (
        "CreateDbtTestResultSourceDbtTestResultSourceCreate"
    ) = Field(alias="dbtTestResultSourceCreate")


class CreateDbtTestResultSourceDbtTestResultSourceCreate(SourceCreation):
    pass


CreateDbtTestResultSource.model_rebuild()
