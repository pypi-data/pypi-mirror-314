from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class CreateTypeNotificationRuleCondition(BaseModel):
    type_notification_rule_condition_create: (
        "CreateTypeNotificationRuleConditionTypeNotificationRuleConditionCreate"
    ) = Field(alias="typeNotificationRuleConditionCreate")


class CreateTypeNotificationRuleConditionTypeNotificationRuleConditionCreate(
    NotificationRuleConditionCreation
):
    pass


CreateTypeNotificationRuleCondition.model_rebuild()
