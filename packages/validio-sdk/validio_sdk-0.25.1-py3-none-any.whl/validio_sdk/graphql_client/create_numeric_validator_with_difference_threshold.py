from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateNumericValidatorWithDifferenceThreshold(BaseModel):
    numeric_validator_with_difference_threshold_create: (
        "CreateNumericValidatorWithDifferenceThresholdNumericValidatorWithDifferenceThresholdCreate"
    ) = Field(alias="numericValidatorWithDifferenceThresholdCreate")


class CreateNumericValidatorWithDifferenceThresholdNumericValidatorWithDifferenceThresholdCreate(
    ValidatorCreation
):
    pass


CreateNumericValidatorWithDifferenceThreshold.model_rebuild()
