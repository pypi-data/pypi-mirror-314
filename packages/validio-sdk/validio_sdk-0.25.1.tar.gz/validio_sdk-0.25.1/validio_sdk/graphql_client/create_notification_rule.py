from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleCreation


class CreateNotificationRule(BaseModel):
    notification_rule_create: "CreateNotificationRuleNotificationRuleCreate" = Field(
        alias="notificationRuleCreate"
    )


class CreateNotificationRuleNotificationRuleCreate(NotificationRuleCreation):
    pass


CreateNotificationRule.model_rebuild()
