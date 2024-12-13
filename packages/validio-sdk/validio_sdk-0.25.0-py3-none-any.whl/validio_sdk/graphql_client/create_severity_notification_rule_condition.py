from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class CreateSeverityNotificationRuleCondition(BaseModel):
    severity_notification_rule_condition_create: (
        "CreateSeverityNotificationRuleConditionSeverityNotificationRuleConditionCreate"
    ) = Field(alias="severityNotificationRuleConditionCreate")


class CreateSeverityNotificationRuleConditionSeverityNotificationRuleConditionCreate(
    NotificationRuleConditionCreation
):
    pass


CreateSeverityNotificationRuleCondition.model_rebuild()
