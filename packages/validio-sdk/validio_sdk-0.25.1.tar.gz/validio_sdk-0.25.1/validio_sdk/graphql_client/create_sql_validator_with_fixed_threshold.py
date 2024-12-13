from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateSqlValidatorWithFixedThreshold(BaseModel):
    sql_validator_with_fixed_threshold_create: (
        "CreateSqlValidatorWithFixedThresholdSqlValidatorWithFixedThresholdCreate"
    ) = Field(alias="sqlValidatorWithFixedThresholdCreate")


class CreateSqlValidatorWithFixedThresholdSqlValidatorWithFixedThresholdCreate(
    ValidatorCreation
):
    pass


CreateSqlValidatorWithFixedThreshold.model_rebuild()
