from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleUpdate


class UpdateNotificationRule(BaseModel):
    notification_rule_update: "UpdateNotificationRuleNotificationRuleUpdate" = Field(
        alias="notificationRuleUpdate"
    )


class UpdateNotificationRuleNotificationRuleUpdate(NotificationRuleUpdate):
    pass


UpdateNotificationRule.model_rebuild()
