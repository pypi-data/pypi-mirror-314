from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorUpdate


class UpdateRelativeVolumeValidator(BaseModel):
    relative_volume_validator_update: (
        "UpdateRelativeVolumeValidatorRelativeVolumeValidatorUpdate"
    ) = Field(alias="relativeVolumeValidatorUpdate")


class UpdateRelativeVolumeValidatorRelativeVolumeValidatorUpdate(ValidatorUpdate):
    pass


UpdateRelativeVolumeValidator.model_rebuild()
