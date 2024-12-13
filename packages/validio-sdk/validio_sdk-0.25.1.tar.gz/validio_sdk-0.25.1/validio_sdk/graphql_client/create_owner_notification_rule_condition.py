from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class CreateOwnerNotificationRuleCondition(BaseModel):
    owner_notification_rule_condition_create: (
        "CreateOwnerNotificationRuleConditionOwnerNotificationRuleConditionCreate"
    ) = Field(alias="ownerNotificationRuleConditionCreate")


class CreateOwnerNotificationRuleConditionOwnerNotificationRuleConditionCreate(
    NotificationRuleConditionCreation
):
    pass


CreateOwnerNotificationRuleCondition.model_rebuild()
