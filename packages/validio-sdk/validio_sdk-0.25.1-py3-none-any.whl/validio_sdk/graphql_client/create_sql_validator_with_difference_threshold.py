from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateSqlValidatorWithDifferenceThreshold(BaseModel):
    sql_validator_with_difference_threshold_create: (
        "CreateSqlValidatorWithDifferenceThresholdSqlValidatorWithDifferenceThresholdCreate"
    ) = Field(alias="sqlValidatorWithDifferenceThresholdCreate")


class CreateSqlValidatorWithDifferenceThresholdSqlValidatorWithDifferenceThresholdCreate(
    ValidatorCreation
):
    pass


CreateSqlValidatorWithDifferenceThreshold.model_rebuild()
