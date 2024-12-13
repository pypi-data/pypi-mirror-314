from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class UpdateTypeNotificationRuleCondition(BaseModel):
    type_notification_rule_condition_update: (
        "UpdateTypeNotificationRuleConditionTypeNotificationRuleConditionUpdate"
    ) = Field(alias="typeNotificationRuleConditionUpdate")


class UpdateTypeNotificationRuleConditionTypeNotificationRuleConditionUpdate(
    NotificationRuleConditionCreation
):
    pass


UpdateTypeNotificationRuleCondition.model_rebuild()
