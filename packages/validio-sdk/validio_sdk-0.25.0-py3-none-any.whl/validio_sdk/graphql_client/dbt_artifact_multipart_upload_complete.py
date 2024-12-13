from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DbtArtifactMultipartUploadComplete(BaseModel):
    dbt_artifact_multipart_upload_complete: (
        "DbtArtifactMultipartUploadCompleteDbtArtifactMultipartUploadComplete"
    ) = Field(alias="dbtArtifactMultipartUploadComplete")


class DbtArtifactMultipartUploadCompleteDbtArtifactMultipartUploadComplete(BaseModel):
    errors: List[
        "DbtArtifactMultipartUploadCompleteDbtArtifactMultipartUploadCompleteErrors"
    ]


class DbtArtifactMultipartUploadCompleteDbtArtifactMultipartUploadCompleteErrors(
    ErrorDetails
):
    pass


DbtArtifactMultipartUploadComplete.model_rebuild()
DbtArtifactMultipartUploadCompleteDbtArtifactMultipartUploadComplete.model_rebuild()
