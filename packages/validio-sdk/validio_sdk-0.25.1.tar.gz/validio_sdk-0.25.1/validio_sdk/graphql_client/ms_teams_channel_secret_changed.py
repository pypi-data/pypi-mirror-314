from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class MsTeamsChannelSecretChanged(BaseModel):
    ms_teams_channel_secret_changed: (
        "MsTeamsChannelSecretChangedMsTeamsChannelSecretChanged"
    ) = Field(alias="msTeamsChannelSecretChanged")


class MsTeamsChannelSecretChangedMsTeamsChannelSecretChanged(BaseModel):
    errors: List["MsTeamsChannelSecretChangedMsTeamsChannelSecretChangedErrors"]
    client_id: bool = Field(alias="clientId")
    client_secret: bool = Field(alias="clientSecret")


class MsTeamsChannelSecretChangedMsTeamsChannelSecretChangedErrors(ErrorDetails):
    pass


MsTeamsChannelSecretChanged.model_rebuild()
MsTeamsChannelSecretChangedMsTeamsChannelSecretChanged.model_rebuild()
