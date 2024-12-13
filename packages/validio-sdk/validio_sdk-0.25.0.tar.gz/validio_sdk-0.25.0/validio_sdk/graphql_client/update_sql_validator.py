from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorUpdate


class UpdateSqlValidator(BaseModel):
    sql_validator_update: "UpdateSqlValidatorSqlValidatorUpdate" = Field(
        alias="sqlValidatorUpdate"
    )


class UpdateSqlValidatorSqlValidatorUpdate(ValidatorUpdate):
    pass


UpdateSqlValidator.model_rebuild()
