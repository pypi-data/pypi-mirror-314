from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_deployment import AgentDeployment
from ...types import UNSET, Response, Unset


def _get_kwargs(
    agent_name: str,
    environment_name: str,
    *,
    configuration: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["configuration"] = configuration

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/agents/{agent_name}/deployments/{environment_name}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AgentDeployment]:
    if response.status_code == 200:
        response_200 = AgentDeployment.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AgentDeployment]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_name: str,
    environment_name: str,
    *,
    client: AuthenticatedClient,
    configuration: Union[Unset, bool] = UNSET,
) -> Response[AgentDeployment]:
    """Get agent deployment by environment name

    Args:
        agent_name (str):
        environment_name (str):
        configuration (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentDeployment]
    """

    kwargs = _get_kwargs(
        agent_name=agent_name,
        environment_name=environment_name,
        configuration=configuration,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    agent_name: str,
    environment_name: str,
    *,
    client: AuthenticatedClient,
    configuration: Union[Unset, bool] = UNSET,
) -> Optional[AgentDeployment]:
    """Get agent deployment by environment name

    Args:
        agent_name (str):
        environment_name (str):
        configuration (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentDeployment
    """

    return sync_detailed(
        agent_name=agent_name,
        environment_name=environment_name,
        client=client,
        configuration=configuration,
    ).parsed


async def asyncio_detailed(
    agent_name: str,
    environment_name: str,
    *,
    client: AuthenticatedClient,
    configuration: Union[Unset, bool] = UNSET,
) -> Response[AgentDeployment]:
    """Get agent deployment by environment name

    Args:
        agent_name (str):
        environment_name (str):
        configuration (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentDeployment]
    """

    kwargs = _get_kwargs(
        agent_name=agent_name,
        environment_name=environment_name,
        configuration=configuration,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    agent_name: str,
    environment_name: str,
    *,
    client: AuthenticatedClient,
    configuration: Union[Unset, bool] = UNSET,
) -> Optional[AgentDeployment]:
    """Get agent deployment by environment name

    Args:
        agent_name (str):
        environment_name (str):
        configuration (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentDeployment
    """

    return (
        await asyncio_detailed(
            agent_name=agent_name,
            environment_name=environment_name,
            client=client,
            configuration=configuration,
        )
    ).parsed
