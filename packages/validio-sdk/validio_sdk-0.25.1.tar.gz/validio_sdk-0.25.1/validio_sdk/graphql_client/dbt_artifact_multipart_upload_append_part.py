from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import ErrorDetails


class DbtArtifactMultipartUploadAppendPart(BaseModel):
    dbt_artifact_multipart_upload_append_part: (
        "DbtArtifactMultipartUploadAppendPartDbtArtifactMultipartUploadAppendPart"
    ) = Field(alias="dbtArtifactMultipartUploadAppendPart")


class DbtArtifactMultipartUploadAppendPartDbtArtifactMultipartUploadAppendPart(
    BaseModel
):
    errors: List[
        "DbtArtifactMultipartUploadAppendPartDbtArtifactMultipartUploadAppendPartErrors"
    ]


class DbtArtifactMultipartUploadAppendPartDbtArtifactMultipartUploadAppendPartErrors(
    ErrorDetails
):
    pass


DbtArtifactMultipartUploadAppendPart.model_rebuild()
DbtArtifactMultipartUploadAppendPartDbtArtifactMultipartUploadAppendPart.model_rebuild()
