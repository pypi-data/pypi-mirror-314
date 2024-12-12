from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.check_payload_request_body import CheckPayloadRequestBody
from ...models.guardrail_check import GuardrailCheck
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CheckPayloadRequestBody,
    dryrun: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["dryrun"] = dryrun

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/checks",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GuardrailCheck]:
    if response.status_code == 200:
        response_200 = GuardrailCheck.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GuardrailCheck]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CheckPayloadRequestBody,
    dryrun: Union[Unset, bool] = UNSET,
) -> Response[GuardrailCheck]:
    """Check payload

    Args:
        dryrun (Union[Unset, bool]):
        body (CheckPayloadRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GuardrailCheck]
    """

    kwargs = _get_kwargs(
        body=body,
        dryrun=dryrun,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CheckPayloadRequestBody,
    dryrun: Union[Unset, bool] = UNSET,
) -> Optional[GuardrailCheck]:
    """Check payload

    Args:
        dryrun (Union[Unset, bool]):
        body (CheckPayloadRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GuardrailCheck
    """

    return sync_detailed(
        client=client,
        body=body,
        dryrun=dryrun,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CheckPayloadRequestBody,
    dryrun: Union[Unset, bool] = UNSET,
) -> Response[GuardrailCheck]:
    """Check payload

    Args:
        dryrun (Union[Unset, bool]):
        body (CheckPayloadRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GuardrailCheck]
    """

    kwargs = _get_kwargs(
        body=body,
        dryrun=dryrun,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CheckPayloadRequestBody,
    dryrun: Union[Unset, bool] = UNSET,
) -> Optional[GuardrailCheck]:
    """Check payload

    Args:
        dryrun (Union[Unset, bool]):
        body (CheckPayloadRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GuardrailCheck
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            dryrun=dryrun,
        )
    ).parsed
