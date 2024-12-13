from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class WebhookChannelSecretChanged(BaseModel):
    webhook_channel_secret_changed: (
        "WebhookChannelSecretChangedWebhookChannelSecretChanged"
    ) = Field(alias="webhookChannelSecretChanged")


class WebhookChannelSecretChangedWebhookChannelSecretChanged(BaseModel):
    errors: List["WebhookChannelSecretChangedWebhookChannelSecretChangedErrors"]
    auth_header: bool = Field(alias="authHeader")


class WebhookChannelSecretChangedWebhookChannelSecretChangedErrors(ErrorDetails):
    pass


WebhookChannelSecretChanged.model_rebuild()
WebhookChannelSecretChangedWebhookChannelSecretChanged.model_rebuild()
