from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorUpdate


class UpdateFreshnessValidator(BaseModel):
    freshness_validator_update: "UpdateFreshnessValidatorFreshnessValidatorUpdate" = (
        Field(alias="freshnessValidatorUpdate")
    )


class UpdateFreshnessValidatorFreshnessValidatorUpdate(ValidatorUpdate):
    pass


UpdateFreshnessValidator.model_rebuild()
