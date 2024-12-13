from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorUpdate


class UpdateVolumeValidator(BaseModel):
    volume_validator_update: "UpdateVolumeValidatorVolumeValidatorUpdate" = Field(
        alias="volumeValidatorUpdate"
    )


class UpdateVolumeValidatorVolumeValidatorUpdate(ValidatorUpdate):
    pass


UpdateVolumeValidator.model_rebuild()
