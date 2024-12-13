from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleDetails


class GetNotificationRule(BaseModel):
    notification_rule: Optional["GetNotificationRuleNotificationRule"] = Field(
        alias="notificationRule"
    )


class GetNotificationRuleNotificationRule(NotificationRuleDetails):
    pass


GetNotificationRule.model_rebuild()
