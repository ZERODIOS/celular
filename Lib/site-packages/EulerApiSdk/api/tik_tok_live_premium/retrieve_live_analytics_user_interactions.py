from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.live_analytics_user_interactions_api_response import LiveAnalyticsUserInteractionsAPIResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    room_id: str,
    user_id: str,
    x_oauth_token: str | Unset = UNSET,
    x_cookie_header: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_oauth_token, Unset):
        headers["x-oauth-token"] = x_oauth_token

    if not isinstance(x_cookie_header, Unset):
        headers["x-cookie-header"] = x_cookie_header

    params: dict[str, Any] = {}

    params["room_id"] = room_id

    params["user_id"] = user_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/webcast/live_analytics/user_interactions",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> LiveAnalyticsUserInteractionsAPIResponse | None:
    if response.status_code == 200:
        response_200 = LiveAnalyticsUserInteractionsAPIResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[LiveAnalyticsUserInteractionsAPIResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    room_id: str,
    user_id: str,
    x_oauth_token: str | Unset = UNSET,
    x_cookie_header: str | Unset = UNSET,
) -> Response[LiveAnalyticsUserInteractionsAPIResponse]:
    """Requires Premium Routes Addon - Find out how long a user watched your stream, the # of comments
    sent, likes, the comments themselves, and more analytics data.

    **Note:** The session you attach must own the livestream to check analytics for a given `room_id`.

    Returns details about a user's activity in a room including comments, likes, shares, and watch
    duration.

    **Authentication:** Provide exactly one of the following headers:
    - `x-oauth-token`: An OAuth access token. The sessionId and ttTargetIdc are resolved from the stored
    OAuth session. [Read More](https://www.eulerstream.com/docs/oauth)
    - `x-cookie-header`: A cookie header string containing `sessionid` and `tt-target-idc` cookies from
    TikTok.

    Args:
        room_id (str):
        user_id (str):
        x_oauth_token (str | Unset):
        x_cookie_header (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LiveAnalyticsUserInteractionsAPIResponse]
    """

    kwargs = _get_kwargs(
        room_id=room_id,
        user_id=user_id,
        x_oauth_token=x_oauth_token,
        x_cookie_header=x_cookie_header,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    room_id: str,
    user_id: str,
    x_oauth_token: str | Unset = UNSET,
    x_cookie_header: str | Unset = UNSET,
) -> LiveAnalyticsUserInteractionsAPIResponse | None:
    """Requires Premium Routes Addon - Find out how long a user watched your stream, the # of comments
    sent, likes, the comments themselves, and more analytics data.

    **Note:** The session you attach must own the livestream to check analytics for a given `room_id`.

    Returns details about a user's activity in a room including comments, likes, shares, and watch
    duration.

    **Authentication:** Provide exactly one of the following headers:
    - `x-oauth-token`: An OAuth access token. The sessionId and ttTargetIdc are resolved from the stored
    OAuth session. [Read More](https://www.eulerstream.com/docs/oauth)
    - `x-cookie-header`: A cookie header string containing `sessionid` and `tt-target-idc` cookies from
    TikTok.

    Args:
        room_id (str):
        user_id (str):
        x_oauth_token (str | Unset):
        x_cookie_header (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LiveAnalyticsUserInteractionsAPIResponse
    """

    return sync_detailed(
        client=client,
        room_id=room_id,
        user_id=user_id,
        x_oauth_token=x_oauth_token,
        x_cookie_header=x_cookie_header,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    room_id: str,
    user_id: str,
    x_oauth_token: str | Unset = UNSET,
    x_cookie_header: str | Unset = UNSET,
) -> Response[LiveAnalyticsUserInteractionsAPIResponse]:
    """Requires Premium Routes Addon - Find out how long a user watched your stream, the # of comments
    sent, likes, the comments themselves, and more analytics data.

    **Note:** The session you attach must own the livestream to check analytics for a given `room_id`.

    Returns details about a user's activity in a room including comments, likes, shares, and watch
    duration.

    **Authentication:** Provide exactly one of the following headers:
    - `x-oauth-token`: An OAuth access token. The sessionId and ttTargetIdc are resolved from the stored
    OAuth session. [Read More](https://www.eulerstream.com/docs/oauth)
    - `x-cookie-header`: A cookie header string containing `sessionid` and `tt-target-idc` cookies from
    TikTok.

    Args:
        room_id (str):
        user_id (str):
        x_oauth_token (str | Unset):
        x_cookie_header (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LiveAnalyticsUserInteractionsAPIResponse]
    """

    kwargs = _get_kwargs(
        room_id=room_id,
        user_id=user_id,
        x_oauth_token=x_oauth_token,
        x_cookie_header=x_cookie_header,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    room_id: str,
    user_id: str,
    x_oauth_token: str | Unset = UNSET,
    x_cookie_header: str | Unset = UNSET,
) -> LiveAnalyticsUserInteractionsAPIResponse | None:
    """Requires Premium Routes Addon - Find out how long a user watched your stream, the # of comments
    sent, likes, the comments themselves, and more analytics data.

    **Note:** The session you attach must own the livestream to check analytics for a given `room_id`.

    Returns details about a user's activity in a room including comments, likes, shares, and watch
    duration.

    **Authentication:** Provide exactly one of the following headers:
    - `x-oauth-token`: An OAuth access token. The sessionId and ttTargetIdc are resolved from the stored
    OAuth session. [Read More](https://www.eulerstream.com/docs/oauth)
    - `x-cookie-header`: A cookie header string containing `sessionid` and `tt-target-idc` cookies from
    TikTok.

    Args:
        room_id (str):
        user_id (str):
        x_oauth_token (str | Unset):
        x_cookie_header (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LiveAnalyticsUserInteractionsAPIResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            room_id=room_id,
            user_id=user_id,
            x_oauth_token=x_oauth_token,
            x_cookie_header=x_cookie_header,
        )
    ).parsed
