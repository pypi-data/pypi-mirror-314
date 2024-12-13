from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorUpdate


class UpdateRelativeTimeValidator(BaseModel):
    relative_time_validator_update: (
        "UpdateRelativeTimeValidatorRelativeTimeValidatorUpdate"
    ) = Field(alias="relativeTimeValidatorUpdate")


class UpdateRelativeTimeValidatorRelativeTimeValidatorUpdate(ValidatorUpdate):
    pass


UpdateRelativeTimeValidator.model_rebuild()
