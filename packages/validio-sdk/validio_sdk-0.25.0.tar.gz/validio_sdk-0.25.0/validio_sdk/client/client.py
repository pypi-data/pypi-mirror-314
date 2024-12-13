"""A client used to send GraphQL requests with sensible defaults for Validio.

The client simply wraps a [gql.client.Client] and works the same way regarding
sessions to support safe use of the client in parallel. More details can be
found at https://gql.readthedocs.io/en/latest/advanced/async_advanced_usage.html
"""

import logging
from typing import Any

from gql import Client as GqlClient
from gql import gql
from gql.client import AsyncClientSession
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.aiohttp import log as aiohttp_logger

import validio_sdk.metadata
from validio_sdk.config import Config, ValidioConfig

USER_AGENT = f"validio-sdk@{validio_sdk.metadata.version()}"


class Session:
    """A session to perform multiple requests.

    **NOTE!** The client used in the examples below is in beta and breaking
    changes may happen.

    A session will support running multiple requests with the same client. It
    will ensure the connection is open and not closed until the session goes out
    of scope.
    """

    def __init__(self, session: AsyncClientSession):
        """Constructor.

        :params session: An `AsyncClientSession` created from a GraphQL client
        """
        self.session = session

    async def execute(self, query: str, **kwargs) -> Any:  # type: ignore
        """Execute a query in the session.

        :param query: The query to be executed
        :param kwargs: Arguments matching the GraphQL client e.g. `variable_values`
            and `operation_name`.
        :returns: The API response
        """
        graphql_query = gql(query)
        return await self.session.execute(graphql_query, **kwargs)


class Client:
    """A GraphQL client with sensible defaults for Validio.

    **NOTE!** The client used in the examples below is in beta and breaking
    changes may happen.

    It will be created by reading the Validio configuration just like the CLI
    tool and ensure the correct headers are passed.

    If no `ValidioConfig` is passed when constructing the client, it will
    fallback to first look for required environment variables:

    - `VALIDIO_ENDPOINT`
    - `VALIDIO_ACCESS_KEY`
    - `VALIDIO_SECRET_ACCESS_KEY`

    If not all of them are found, it will look for a configuration file. It will
    first look in the path set in `VALIDIO_CONFIG_PATH` and if that one is empty
    it will look in the default OS dependant system directory.
    """

    def __init__(
        self,
        config: ValidioConfig | None = None,
        user_agent: str = USER_AGENT,
        headers: dict[str, str] = {},
    ):
        """Constructor.

        :param config: Optional `ValidioConfig` to use to set config.
        :param user_agent: The `User-Agent` header to use for the requests
        :param headers: Additional headers to set.
        :returns: A client that can execute GraphQL operations
        """
        if config is None:
            config = Config().read()

        headers = {
            "User-Agent": user_agent,
            "Authorization": f"{config.access_key}:{config._access_secret}",
            **headers,
        }
        api_url = f"{config.endpoint.rstrip('/')}/api"
        transport = AIOHTTPTransport(url=api_url, headers=headers)

        aiohttp_logger.setLevel(logging.WARNING)

        self.client = GqlClient(transport=transport, fetch_schema_from_transport=True)

    async def __aenter__(self):  # type: ignore
        """Enter async context.

        Will return a session to reuse transport for API calls. This is needed
        to do concurrent requests to ensure the transport is opened, waits for
        each request and don't close the connection before exiting the context.
        """
        session = await self.client.connect_async()  # type: ignore
        return Session(session)

    async def __aexit__(self, *args):  # type: ignore
        """Exit context.

        Will close the session.
        """
        await self.client.close_async()  # type: ignore

    async def execute(self, query: str, **kwargs) -> Any:  # type: ignore
        """Execute a GraphQL request.

        :param query: The query to be executed
        :param kwargs: Arguments matching the GraphQL client e.g. `variable_values`
            and `operation_name`.
        :returns: The API response
        """
        async with self as session:
            return await session.execute(query, **kwargs)
