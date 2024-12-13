from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleDetails


class ListNotificationRules(BaseModel):
    notification_rules_list: List["ListNotificationRulesNotificationRulesList"] = Field(
        alias="notificationRulesList"
    )


class ListNotificationRulesNotificationRulesList(NotificationRuleDetails):
    pass


ListNotificationRules.model_rebuild()
