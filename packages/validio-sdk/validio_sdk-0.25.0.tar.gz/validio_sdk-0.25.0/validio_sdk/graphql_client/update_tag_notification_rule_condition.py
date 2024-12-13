from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class UpdateTagNotificationRuleCondition(BaseModel):
    tag_notification_rule_condition_update: (
        "UpdateTagNotificationRuleConditionTagNotificationRuleConditionUpdate"
    ) = Field(alias="tagNotificationRuleConditionUpdate")


class UpdateTagNotificationRuleConditionTagNotificationRuleConditionUpdate(
    NotificationRuleConditionCreation
):
    pass


UpdateTagNotificationRuleCondition.model_rebuild()
