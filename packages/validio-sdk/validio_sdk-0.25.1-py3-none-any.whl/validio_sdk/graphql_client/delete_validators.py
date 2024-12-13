from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DeleteValidators(BaseModel):
    validators_delete: "DeleteValidatorsValidatorsDelete" = Field(
        alias="validatorsDelete"
    )


class DeleteValidatorsValidatorsDelete(BaseModel):
    errors: List["DeleteValidatorsValidatorsDeleteErrors"]


class DeleteValidatorsValidatorsDeleteErrors(ErrorDetails):
    pass


DeleteValidators.model_rebuild()
DeleteValidatorsValidatorsDelete.model_rebuild()
