from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateSqlValidatorWithDynamicThreshold(BaseModel):
    sql_validator_with_dynamic_threshold_create: (
        "CreateSqlValidatorWithDynamicThresholdSqlValidatorWithDynamicThresholdCreate"
    ) = Field(alias="sqlValidatorWithDynamicThresholdCreate")


class CreateSqlValidatorWithDynamicThresholdSqlValidatorWithDynamicThresholdCreate(
    ValidatorCreation
):
    pass


CreateSqlValidatorWithDynamicThreshold.model_rebuild()
