from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DbtArtifactUpload(BaseModel):
    dbt_artifact_upload: "DbtArtifactUploadDbtArtifactUpload" = Field(
        alias="dbtArtifactUpload"
    )


class DbtArtifactUploadDbtArtifactUpload(BaseModel):
    errors: List["DbtArtifactUploadDbtArtifactUploadErrors"]


class DbtArtifactUploadDbtArtifactUploadErrors(ErrorDetails):
    pass


DbtArtifactUpload.model_rebuild()
DbtArtifactUploadDbtArtifactUpload.model_rebuild()
