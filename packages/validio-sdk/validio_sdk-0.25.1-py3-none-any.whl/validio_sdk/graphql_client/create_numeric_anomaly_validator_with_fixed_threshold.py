from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateNumericAnomalyValidatorWithFixedThreshold(BaseModel):
    numeric_anomaly_validator_with_fixed_threshold_create: (
        "CreateNumericAnomalyValidatorWithFixedThresholdNumericAnomalyValidatorWithFixedThresholdCreate"
    ) = Field(alias="numericAnomalyValidatorWithFixedThresholdCreate")


class CreateNumericAnomalyValidatorWithFixedThresholdNumericAnomalyValidatorWithFixedThresholdCreate(
    ValidatorCreation
):
    pass


CreateNumericAnomalyValidatorWithFixedThreshold.model_rebuild()
