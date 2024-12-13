from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class CreateTagNotificationRuleCondition(BaseModel):
    tag_notification_rule_condition_create: (
        "CreateTagNotificationRuleConditionTagNotificationRuleConditionCreate"
    ) = Field(alias="tagNotificationRuleConditionCreate")


class CreateTagNotificationRuleConditionTagNotificationRuleConditionCreate(
    NotificationRuleConditionCreation
):
    pass


CreateTagNotificationRuleCondition.model_rebuild()
