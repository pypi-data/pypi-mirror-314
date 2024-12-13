from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class UpdateSourceNotificationRuleCondition(BaseModel):
    source_notification_rule_condition_update: (
        "UpdateSourceNotificationRuleConditionSourceNotificationRuleConditionUpdate"
    ) = Field(alias="sourceNotificationRuleConditionUpdate")


class UpdateSourceNotificationRuleConditionSourceNotificationRuleConditionUpdate(
    NotificationRuleConditionCreation
):
    pass


UpdateSourceNotificationRuleCondition.model_rebuild()
