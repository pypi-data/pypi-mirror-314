from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateGcpStorageSource(BaseModel):
    gcp_storage_source_update: "UpdateGcpStorageSourceGcpStorageSourceUpdate" = Field(
        alias="gcpStorageSourceUpdate"
    )


class UpdateGcpStorageSourceGcpStorageSourceUpdate(SourceUpdate):
    pass


UpdateGcpStorageSource.model_rebuild()
