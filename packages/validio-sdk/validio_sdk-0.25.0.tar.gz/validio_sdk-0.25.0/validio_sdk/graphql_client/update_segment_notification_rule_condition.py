from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleConditionCreation


class UpdateSegmentNotificationRuleCondition(BaseModel):
    segment_notification_rule_condition_update: (
        "UpdateSegmentNotificationRuleConditionSegmentNotificationRuleConditionUpdate"
    ) = Field(alias="segmentNotificationRuleConditionUpdate")


class UpdateSegmentNotificationRuleConditionSegmentNotificationRuleConditionUpdate(
    NotificationRuleConditionCreation
):
    pass


UpdateSegmentNotificationRuleCondition.model_rebuild()
