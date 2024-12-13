from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class UpdateOwnerNotificationRuleCondition(BaseModel):
    owner_notification_rule_condition_update: (
        "UpdateOwnerNotificationRuleConditionOwnerNotificationRuleConditionUpdate"
    ) = Field(alias="ownerNotificationRuleConditionUpdate")


class UpdateOwnerNotificationRuleConditionOwnerNotificationRuleConditionUpdate(
    NotificationRuleConditionCreation
):
    pass


UpdateOwnerNotificationRuleCondition.model_rebuild()
