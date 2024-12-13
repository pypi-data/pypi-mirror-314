from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class MuteValidator(BaseModel):
    validator_mute: "MuteValidatorValidatorMute" = Field(alias="validatorMute")


class MuteValidatorValidatorMute(BaseModel):
    errors: List["MuteValidatorValidatorMuteErrors"]


class MuteValidatorValidatorMuteErrors(ErrorDetails):
    pass


MuteValidator.model_rebuild()
MuteValidatorValidatorMute.model_rebuild()
