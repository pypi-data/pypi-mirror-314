from typing import Any, List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DbtArtifactMultipartUploadCreate(BaseModel):
    dbt_artifact_multipart_upload_create: (
        "DbtArtifactMultipartUploadCreateDbtArtifactMultipartUploadCreate"
    ) = Field(alias="dbtArtifactMultipartUploadCreate")


class DbtArtifactMultipartUploadCreateDbtArtifactMultipartUploadCreate(BaseModel):
    id: Any
    errors: List[
        "DbtArtifactMultipartUploadCreateDbtArtifactMultipartUploadCreateErrors"
    ]


class DbtArtifactMultipartUploadCreateDbtArtifactMultipartUploadCreateErrors(
    ErrorDetails
):
    pass


DbtArtifactMultipartUploadCreate.model_rebuild()
DbtArtifactMultipartUploadCreateDbtArtifactMultipartUploadCreate.model_rebuild()
