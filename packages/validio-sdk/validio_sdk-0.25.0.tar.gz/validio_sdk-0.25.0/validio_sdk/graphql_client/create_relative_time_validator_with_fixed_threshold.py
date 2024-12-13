from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateRelativeTimeValidatorWithFixedThreshold(BaseModel):
    relative_time_validator_with_fixed_threshold_create: (
        "CreateRelativeTimeValidatorWithFixedThresholdRelativeTimeValidatorWithFixedThresholdCreate"
    ) = Field(alias="relativeTimeValidatorWithFixedThresholdCreate")


class CreateRelativeTimeValidatorWithFixedThresholdRelativeTimeValidatorWithFixedThresholdCreate(
    ValidatorCreation
):
    pass


CreateRelativeTimeValidatorWithFixedThreshold.model_rebuild()
