from pydantic import Field

from .base_model import BaseModel
from .fragments import IdentityProviderUpdate


class UpdateSamlIdentityProvider(BaseModel):
    saml_identity_provider_update: (
        "UpdateSamlIdentityProviderSamlIdentityProviderUpdate"
    ) = Field(alias="samlIdentityProviderUpdate")


class UpdateSamlIdentityProviderSamlIdentityProviderUpdate(IdentityProviderUpdate):
    pass


UpdateSamlIdentityProvider.model_rebuild()
