from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorUpdate


class UpdateNumericValidator(BaseModel):
    numeric_validator_update: "UpdateNumericValidatorNumericValidatorUpdate" = Field(
        alias="numericValidatorUpdate"
    )


class UpdateNumericValidatorNumericValidatorUpdate(ValidatorUpdate):
    pass


UpdateNumericValidator.model_rebuild()
