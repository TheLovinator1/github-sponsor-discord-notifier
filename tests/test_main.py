from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

import pytest
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from starlette.testclient import TestClient

from main import app, raise_if_wrong_header, send_webhook

if TYPE_CHECKING:
    from requests import Response

client = TestClient(app)
json_boi: dict[str, str | dict[str, str | dict[str, str | int | bool]] | dict[str, str | int | bool]] = {
    "action": "created",
    "sponsorship": {
        "node_id": 'S_kwDAX"OAD9fc84ASDAasf',
        "created_at": "2022-11-23T12:57:58+00:00",
        "sponsorable": {
            "login": "TheLovinator1",
            "id": 4153203,
            "node_id": "MDQ61asXasjQxNTMyMDM=",
            "avatar_url": "https://avatars.githubusercontent.com/u/4153203?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/TheLovinator1",
            "html_url": "https://github.com/TheLovinator1",
            "followers_url": "https://api.github.com/users/TheLovinator1/followers",
            "following_url": "https://api.github.com/users/TheLovinator1/following{" "/other_user}",
            "gists_url": "https://api.github.com/users/TheLovinator1/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/TheLovinator1/starred{" "/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/TheLovinator1/subscriptions",
            "organizations_url": "https://api.github.com/users/TheLovinator1/orgs",
            "repos_url": "https://api.github.com/users/TheLovinator1/repos",
            "events_url": "https://api.github.com/users/TheLovinator1/events{/privacy}",
            "received_events_url": "https://api.github.com/users/TheLovinator1/received_events",
            "type": "User",
            "site_admin": False,
        },
        "maintainer": {
            "login": "TheLovinator1",
            "id": 4153203,
            "node_id": "MDQ61asXasjQxNTMyMDM=",
            "avatar_url": "https://avatars.githubusercontent.com/u/4153203?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/TheLovinator1",
            "html_url": "https://github.com/TheLovinator1",
            "followers_url": "https://api.github.com/users/TheLovinator1/followers",
            "following_url": "https://api.github.com/users/TheLovinator1/following{" "/other_user}",
            "gists_url": "https://api.github.com/users/TheLovinator1/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/TheLovinator1/starred{" "/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/TheLovinator1/subscriptions",
            "organizations_url": "https://api.github.com/users/TheLovinator1/orgs",
            "repos_url": "https://api.github.com/users/TheLovinator1/repos",
            "events_url": "https://api.github.com/users/TheLovinator1/events{/privacy}",
            "received_events_url": "https://api.github.com/users/TheLovinator1/received_events",
            "type": "User",
            "site_admin": False,
        },
        "sponsor": {
            "login": "testing",
            "id": 1,
            "node_id": "U_kgDOBwX9RA",
            "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/testing",
            "html_url": "https://github.com/testing",
            "followers_url": "https://api.github.com/users/testing/followers",
            "following_url": "https://api.github.com/users/testing/following{/other_user}",
            "gists_url": "https://api.github.com/users/testing/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/testing/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/testing/subscriptions",
            "organizations_url": "https://api.github.com/users/testing/orgs",
            "repos_url": "https://api.github.com/users/testing/repos",
            "events_url": "https://api.github.com/users/testing/events{/privacy}",
            "received_events_url": "https://api.github.com/users/testing/received_events",
            "type": "User",
            "site_admin": False,
        },
        "privacy_level": "public",
        "tier": {
            "node_id": "ST_kwDOAD9fc84AAiB5",
            "created_at": "2022-03-02T23:11:37Z",
            "description": "- Buy me coffee.\r\n\r\nMore coffee = more code.\r\n",
            "monthly_price_in_cents": 100,
            "monthly_price_in_dollars": 1,
            "name": "$1 one time",
            "is_one_time": True,
            "is_custom_amount": False,
        },
    },
    "sender": {
        "login": "testing",
        "id": 1,
        "node_id": "U_kasfafwX9RA",
        "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/testing",
        "html_url": "https://github.com/testing",
        "followers_url": "https://api.github.com/users/testing/followers",
        "following_url": "https://api.github.com/users/testing/following{/other_user}",
        "gists_url": "https://api.github.com/users/testing/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/testing/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/testing/subscriptions",
        "organizations_url": "https://api.github.com/users/testing/orgs",
        "repos_url": "https://api.github.com/users/testing/repos",
        "events_url": "https://api.github.com/users/testing/events{/privacy}",
        "received_events_url": "https://api.github.com/users/testing/received_events",
        "type": "User",
        "site_admin": False,
    },
}


def test_send_webhook() -> None:
    """Test if webhook is sent without errors."""
    load_dotenv(verbose=True)
    webhook_url: str | None = os.environ.get("WEBHOOK_URL", default=None)
    if not webhook_url:
        msg = "No webhook URL found."
        raise ValueError(msg)

    hook: Response = send_webhook(json_boi, webhook_url)
    assert hook.ok


def test_check_header() -> None:
    """Test if check_header works."""

    class DummyRequest:
        # Create a dummy Request object with the necessary headers
        def __init__(self: DummyRequest, headers: dict[str, str]) -> None:
            self.headers = headers

    # Test case 1: Correct header ("sponsorship")
    request_correct = DummyRequest(headers={"x-github-event": "sponsorship"})
    request_correct = cast(Request, request_correct)
    raise_if_wrong_header(request_correct)  # This should not raise any exceptions

    # Test case 2: Missing header
    request_missing = DummyRequest(headers={})
    request_missing = cast(Request, request_missing)
    with pytest.raises(HTTPException) as exc_info:
        raise_if_wrong_header(request_missing)
    assert exc_info.value.status_code == 500  # noqa: PLR2004
    assert exc_info.value.detail == "No header found."

    # Test case 3: Incorrect header ("push" instead of "sponsorship")
    request_incorrect = DummyRequest(headers={"x-github-event": "push"})
    request_incorrect = cast(Request, request_incorrect)
    with pytest.raises(HTTPException) as exc_info:
        raise_if_wrong_header(request_incorrect)
    assert exc_info.value.status_code == 500  # noqa: PLR2004
    assert exc_info.value.detail == "Only sponsorships are allowed."
