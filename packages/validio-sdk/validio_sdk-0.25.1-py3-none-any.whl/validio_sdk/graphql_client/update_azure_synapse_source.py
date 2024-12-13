from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceUpdate


class UpdateAzureSynapseSource(BaseModel):
    azure_synapse_source_update: "UpdateAzureSynapseSourceAzureSynapseSourceUpdate" = (
        Field(alias="azureSynapseSourceUpdate")
    )


class UpdateAzureSynapseSourceAzureSynapseSourceUpdate(SourceUpdate):
    pass


UpdateAzureSynapseSource.model_rebuild()
