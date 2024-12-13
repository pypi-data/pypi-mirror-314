from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorCreation


class CreateNumericAnomalyValidatorWithDynamicThreshold(BaseModel):
    numeric_anomaly_validator_with_dynamic_threshold_create: (
        "CreateNumericAnomalyValidatorWithDynamicThresholdNumericAnomalyValidatorWithDynamicThresholdCreate"
    ) = Field(alias="numericAnomalyValidatorWithDynamicThresholdCreate")


class CreateNumericAnomalyValidatorWithDynamicThresholdNumericAnomalyValidatorWithDynamicThresholdCreate(
    ValidatorCreation
):
    pass


CreateNumericAnomalyValidatorWithDynamicThreshold.model_rebuild()
