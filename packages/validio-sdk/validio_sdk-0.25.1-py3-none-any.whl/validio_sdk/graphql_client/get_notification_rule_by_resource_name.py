from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import NotificationRuleDetails


class GetNotificationRuleByResourceName(BaseModel):
    notification_rule_by_resource_name: Optional[
        "GetNotificationRuleByResourceNameNotificationRuleByResourceName"
    ] = Field(alias="notificationRuleByResourceName")


class GetNotificationRuleByResourceNameNotificationRuleByResourceName(
    NotificationRuleDetails
):
    pass


GetNotificationRuleByResourceName.model_rebuild()
