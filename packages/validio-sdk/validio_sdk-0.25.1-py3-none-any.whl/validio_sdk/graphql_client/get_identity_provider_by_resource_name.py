from datetime import datetime
from typing import Annotated, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel


class GetIdentityProviderByResourceName(BaseModel):
    identity_provider_by_resource_name: Optional[
        Annotated[
            Union[
                "GetIdentityProviderByResourceNameIdentityProviderByResourceNameIdentityProvider",
                "GetIdentityProviderByResourceNameIdentityProviderByResourceNameSamlIdentityProvider",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="identityProviderByResourceName")


class GetIdentityProviderByResourceNameIdentityProviderByResourceNameIdentityProvider(
    BaseModel
):
    typename__: Literal["IdentityProvider", "LocalIdentityProvider"] = Field(
        alias="__typename"
    )
    id: str
    name: str
    disabled: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")


class GetIdentityProviderByResourceNameIdentityProviderByResourceNameSamlIdentityProvider(
    BaseModel
):
    typename__: Literal["SamlIdentityProvider"] = Field(alias="__typename")
    id: str
    name: str
    disabled: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    config: "GetIdentityProviderByResourceNameIdentityProviderByResourceNameSamlIdentityProviderConfig"


class GetIdentityProviderByResourceNameIdentityProviderByResourceNameSamlIdentityProviderConfig(
    BaseModel
):
    entry_point: str = Field(alias="entryPoint")
    entity_id: str = Field(alias="entityId")
    cert: str


GetIdentityProviderByResourceName.model_rebuild()
GetIdentityProviderByResourceNameIdentityProviderByResourceNameSamlIdentityProvider.model_rebuild()
