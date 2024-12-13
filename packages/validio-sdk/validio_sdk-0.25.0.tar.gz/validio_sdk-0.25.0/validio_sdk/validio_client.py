"""A client used to communicate with the Validio API."""

from collections.abc import Callable
from http import HTTPStatus
from pathlib import Path
from typing import Any

import httpx

import validio_sdk.metadata
from validio_sdk import UnauthorizedError, ValidioConnectionError
from validio_sdk.config import (
    VALIDIO_ACCESS_KEY_ENV,
    VALIDIO_ENDPOINT_ENV,
    VALIDIO_SECRET_ACCESS_KEY_ENV,
    Config,
    ValidioConfig,
)
from validio_sdk.graphql_client.client import Client

HOME_DIR = str(Path.home())


class ValidioAPIClient(Client):
    """An API client used to communicate with the Validio API."""

    def __init__(
        self,
        headers: dict[str, str] | None = None,
        validio_config: ValidioConfig | None = None,
    ):
        """
        Create a new API client.

        :param headers: Custom headers to apply to each request
        :param http_client: HTTP client to use for API calls
        :param validio_config: Config for the client to initialize from

        :returns: A `ValidioAPIClient` object
        """
        if validio_config is None:
            validio_config = Config().read()

        base_url = validio_config.endpoint
        graphql_endpoint = f"{base_url.rstrip('/')}/api"
        base_headers = {"user-agent": f"validio-sdk@{validio_sdk.metadata.version()}"}
        http_client = httpx.AsyncClient(
            headers=base_headers,
            auth=_add_api_token_auth_header(validio_config),
            timeout=60,
            event_hooks={"response": [_handle_unauthorized]},
        )

        super().__init__(graphql_endpoint, headers, http_client)

    async def execute(
        self,
        query: str,
        operation_name: str | None = None,
        variables: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Execute overwrites the client execution method to be able to manipulate
        thrown exceptions.

        :param query: The query to execute
        :param variables: Variables to the query
        """
        try:
            return await super().execute(query, operation_name, variables, **kwargs)
        except httpx.ConnectError as e:
            raise ValidioConnectionError(VALIDIO_ENDPOINT_ENV, e)


async def _handle_unauthorized(response: httpx.Response) -> None:
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise UnauthorizedError(VALIDIO_ACCESS_KEY_ENV, VALIDIO_SECRET_ACCESS_KEY_ENV)


def _add_api_token_auth_header(
    validio_config: ValidioConfig,
) -> Callable[[httpx.Request], httpx.Request]:
    """
    Add the API token to the authorization header.

    The format is: Authorization: <access_key>:<access_secret>
    """

    def inner(request: httpx.Request) -> httpx.Request:
        request.headers[
            "Authorization"
        ] = f"{validio_config.access_key}:{validio_config._access_secret}"
        return request

    return inner
