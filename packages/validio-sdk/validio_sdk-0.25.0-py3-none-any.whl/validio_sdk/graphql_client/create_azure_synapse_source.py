from pydantic import Field

from .base_model import BaseModel
from .fragments import SourceCreation


class CreateAzureSynapseSource(BaseModel):
    azure_synapse_source_create: "CreateAzureSynapseSourceAzureSynapseSourceCreate" = (
        Field(alias="azureSynapseSourceCreate")
    )


class CreateAzureSynapseSourceAzureSynapseSourceCreate(SourceCreation):
    pass


CreateAzureSynapseSource.model_rebuild()
