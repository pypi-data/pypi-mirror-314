from pydantic import Field

from .base_model import BaseModel
from .fragments import ValidatorRecommendationApplication


class ApplyValidatorRecommendation(BaseModel):
    validator_recommendation_apply: (
        "ApplyValidatorRecommendationValidatorRecommendationApply"
    ) = Field(alias="validatorRecommendationApply")


class ApplyValidatorRecommendationValidatorRecommendationApply(
    ValidatorRecommendationApplication
):
    pass


ApplyValidatorRecommendation.model_rebuild()
