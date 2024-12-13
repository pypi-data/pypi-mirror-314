from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class CreateSourceNotificationRuleCondition(BaseModel):
    source_notification_rule_condition_create: (
        "CreateSourceNotificationRuleConditionSourceNotificationRuleConditionCreate"
    ) = Field(alias="sourceNotificationRuleConditionCreate")


class CreateSourceNotificationRuleConditionSourceNotificationRuleConditionCreate(
    NotificationRuleConditionCreation
):
    pass


CreateSourceNotificationRuleCondition.model_rebuild()
