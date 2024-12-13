from datetime import datetime
from typing import Annotated, List, Literal, Union

from pydantic import Field

from .base_model import BaseModel


class ListIdentityProviders(BaseModel):
    identity_providers_list: List[
        Annotated[
            Union[
                "ListIdentityProvidersIdentityProvidersListIdentityProvider",
                "ListIdentityProvidersIdentityProvidersListSamlIdentityProvider",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="identityProvidersList")


class ListIdentityProvidersIdentityProvidersListIdentityProvider(BaseModel):
    typename__: Literal["IdentityProvider", "LocalIdentityProvider"] = Field(
        alias="__typename"
    )
    id: str
    name: str
    disabled: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")


class ListIdentityProvidersIdentityProvidersListSamlIdentityProvider(BaseModel):
    typename__: Literal["SamlIdentityProvider"] = Field(alias="__typename")
    id: str
    name: str
    disabled: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    config: "ListIdentityProvidersIdentityProvidersListSamlIdentityProviderConfig"


class ListIdentityProvidersIdentityProvidersListSamlIdentityProviderConfig(BaseModel):
    entry_point: str = Field(alias="entryPoint")
    entity_id: str = Field(alias="entityId")
    cert: str


ListIdentityProviders.model_rebuild()
ListIdentityProvidersIdentityProvidersListSamlIdentityProvider.model_rebuild()
