from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorUpdate


class UpdateNumericDistributionValidator(BaseModel):
    numeric_distribution_validator_update: (
        "UpdateNumericDistributionValidatorNumericDistributionValidatorUpdate"
    ) = Field(alias="numericDistributionValidatorUpdate")


class UpdateNumericDistributionValidatorNumericDistributionValidatorUpdate(
    ValidatorUpdate
):
    pass


UpdateNumericDistributionValidator.model_rebuild()
