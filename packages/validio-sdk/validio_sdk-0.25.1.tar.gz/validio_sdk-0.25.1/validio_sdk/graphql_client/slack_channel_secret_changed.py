from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class SlackChannelSecretChanged(BaseModel):
    slack_channel_secret_changed: (
        "SlackChannelSecretChangedSlackChannelSecretChanged"
    ) = Field(alias="slackChannelSecretChanged")


class SlackChannelSecretChangedSlackChannelSecretChanged(BaseModel):
    errors: List["SlackChannelSecretChangedSlackChannelSecretChangedErrors"]
    token: bool
    signing_secret: bool = Field(alias="signingSecret")


class SlackChannelSecretChangedSlackChannelSecretChangedErrors(ErrorDetails):
    pass


SlackChannelSecretChanged.model_rebuild()
SlackChannelSecretChangedSlackChannelSecretChanged.model_rebuild()
