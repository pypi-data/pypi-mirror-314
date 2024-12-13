from pydantic import Field

from validio_sdk.scalars import JsonTypeDefinition

from .base_model import BaseModel


class InferAzureSynapseSchema(BaseModel):
    azure_synapse_infer_schema: JsonTypeDefinition = Field(
        alias="azureSynapseInferSchema"
    )
