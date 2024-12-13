from pydantic import Field

from .base_model import BaseModel
from .fragments import IdentityProviderCreation


class CreateSamlIdentityProvider(BaseModel):
    saml_identity_provider_create: (
        "CreateSamlIdentityProviderSamlIdentityProviderCreate"
    ) = Field(alias="samlIdentityProviderCreate")


class CreateSamlIdentityProviderSamlIdentityProviderCreate(IdentityProviderCreation):
    pass


CreateSamlIdentityProvider.model_rebuild()
