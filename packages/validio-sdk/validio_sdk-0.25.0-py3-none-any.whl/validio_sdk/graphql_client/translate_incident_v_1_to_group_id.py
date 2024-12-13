from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel


class TranslateIncidentV1ToGroupId(BaseModel):
    translate_incident_v_1: Optional[
        "TranslateIncidentV1ToGroupIdTranslateIncidentV1"
    ] = Field(alias="translateIncidentV1")


class TranslateIncidentV1ToGroupIdTranslateIncidentV1(BaseModel):
    old_id: str = Field(alias="oldId")
    group_id: Any = Field(alias="groupId")
    incident_id: Any = Field(alias="incidentId")


TranslateIncidentV1ToGroupId.model_rebuild()
