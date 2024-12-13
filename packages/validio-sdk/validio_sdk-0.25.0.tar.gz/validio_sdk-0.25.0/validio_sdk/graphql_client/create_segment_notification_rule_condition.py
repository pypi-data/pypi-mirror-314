from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class CreateSegmentNotificationRuleCondition(BaseModel):
    segment_notification_rule_condition_create: (
        "CreateSegmentNotificationRuleConditionSegmentNotificationRuleConditionCreate"
    ) = Field(alias="segmentNotificationRuleConditionCreate")


class CreateSegmentNotificationRuleConditionSegmentNotificationRuleConditionCreate(
    NotificationRuleConditionCreation
):
    pass


CreateSegmentNotificationRuleCondition.model_rebuild()
