from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class UnmuteValidator(BaseModel):
    validator_unmute: "UnmuteValidatorValidatorUnmute" = Field(alias="validatorUnmute")


class UnmuteValidatorValidatorUnmute(BaseModel):
    errors: List["UnmuteValidatorValidatorUnmuteErrors"]


class UnmuteValidatorValidatorUnmuteErrors(ErrorDetails):
    pass


UnmuteValidator.model_rebuild()
UnmuteValidatorValidatorUnmute.model_rebuild()
