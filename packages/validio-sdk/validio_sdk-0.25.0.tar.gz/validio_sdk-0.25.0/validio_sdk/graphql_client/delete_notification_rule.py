from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleDeletion


class DeleteNotificationRule(BaseModel):
    notification_rule_delete: "DeleteNotificationRuleNotificationRuleDelete" = Field(
        alias="notificationRuleDelete"
    )


class DeleteNotificationRuleNotificationRuleDelete(NotificationRuleDeletion):
    pass


DeleteNotificationRule.model_rebuild()
