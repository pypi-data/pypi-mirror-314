from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class UpdateSeverityNotificationRuleCondition(BaseModel):
    severity_notification_rule_condition_update: (
        "UpdateSeverityNotificationRuleConditionSeverityNotificationRuleConditionUpdate"
    ) = Field(alias="severityNotificationRuleConditionUpdate")


class UpdateSeverityNotificationRuleConditionSeverityNotificationRuleConditionUpdate(
    NotificationRuleConditionCreation
):
    pass


UpdateSeverityNotificationRuleCondition.model_rebuild()
