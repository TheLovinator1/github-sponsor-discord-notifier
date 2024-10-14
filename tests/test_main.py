from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from httpx._models import Response

from main import app, raise_if_wrong_header, send_webhook

if TYPE_CHECKING:
    from requests import Response

client = TestClient(app)

HTTP_STATUS_CODE_ERROR = 500
HTTP_STATUS_CODE_SUCCESS = 200


# Test for raise_if_wrong_header function
def test_raise_if_wrong_header_missing() -> None:
    """Test that the raise_if_wrong_header function raises HTTPException when header is missing."""
    request = MagicMock()
    request.headers = {}

    with pytest.raises(HTTPException) as exc_info:
        raise_if_wrong_header(request)

    assert exc_info.value.status_code == HTTP_STATUS_CODE_ERROR
    assert exc_info.value.detail == "No header found."


def test_raise_if_wrong_header_incorrect() -> None:
    """Test that the raise_if_wrong_header function raises HTTPException when header is incorrect."""
    request = MagicMock()
    request.headers = {"x-github-event": "push"}

    with pytest.raises(HTTPException) as exc_info:
        raise_if_wrong_header(request)

    assert exc_info.value.status_code == HTTP_STATUS_CODE_ERROR
    assert exc_info.value.detail == "Only sponsorships are allowed."


def test_raise_if_wrong_header_correct() -> None:
    """Test that the raise_if_wrong_header function passes when header is 'sponsorship'."""
    request = MagicMock()
    request.headers = {"x-github-event": "sponsorship"}

    # Should not raise any exceptions
    raise_if_wrong_header(request)


# Test for /webhook route
def test_webhook_route_sponsor_event() -> None:
    """Test that the /webhook route works as expected."""
    headers: dict[str, str] = {"x-github-event": "sponsorship"}
    json_data: dict[str, dict[str, dict[str, str]]] = {
        "sponsorship": {
            "sponsorable": {"login": "your-username"},
            "sponsor": {
                "login": "sponsor-username",
                "avatar_url": "https://example.com/avatar.jpg",
                "html_url": "https://github.com/sponsor-username",
            },
            "tier": {"name": "$1 one time"},
        },
    }

    # Mock send_webhook to avoid sending real requests to Discord.
    with patch("main.send_webhook") as mock_send_webhook:
        mock_send_webhook.return_value = MagicMock()  # Mock Discord Response

        response = client.post("/webhook", headers=headers, json=json_data)

        assert response.status_code == HTTP_STATUS_CODE_SUCCESS
        assert response.json() == {"status": "SUCCESS"}
        mock_send_webhook.assert_called_once_with(json_data)


def test_webhook_route_incorrect_event() -> None:
    """Test that the /webhook route rejects non-sponsorship events."""
    headers: dict[str, str] = {"x-github-event": "push"}
    json_data: dict[str, Any] = {}

    response = client.post("/webhook", headers=headers, json=json_data)

    assert response.status_code == HTTP_STATUS_CODE_ERROR
    assert response.json() == {"detail": "Only sponsorships are allowed."}


# Test for send_webhook function
def test_send_webhook() -> None:
    """Test that the send_webhook function sends correct data to Discord."""
    json_data: dict[str, dict[str, dict[str, str]]] = {
        "sponsorship": {
            "sponsorable": {"login": "your-username"},
            "sponsor": {
                "login": "sponsor-username",
                "avatar_url": "https://example.com/avatar.jpg",
                "html_url": "https://github.com/sponsor-username",
            },
            "tier": {"name": "$1 one time"},
        },
    }

    # Mock DiscordWebhook and DiscordEmbed
    with patch("main.DiscordWebhook") as mock_discord_webhook, patch("main.DiscordEmbed") as mock_discord_embed:
        mock_hook = mock_discord_webhook.return_value
        mock_embed = mock_discord_embed.return_value

        response: Response = send_webhook(json_data)

        # Check that the webhook was created with the correct URL and embed
        mock_discord_webhook.assert_called_once_with(
            url=os.getenv("WEBHOOK_URL"),
            rate_limit_retry=True,
            username="GitHub sponsors",
        )
        mock_hook.add_embed.assert_called_once_with(mock_embed)
        mock_hook.execute.assert_called_once()
        assert response == mock_hook.execute()


def test_send_webhook_failure() -> None:
    """Test handling of a failed webhook request to Discord."""
    json_data: dict[str, dict[str, dict[str, str]]] = {
        "sponsorship": {
            "sponsorable": {"login": "your-username"},
            "sponsor": {
                "login": "sponsor-username",
                "avatar_url": "https://example.com/avatar.jpg",
                "html_url": "https://github.com/sponsor-username",
            },
            "tier": {"name": "$1 one time"},
        },
    }

    with patch("main.DiscordWebhook") as mock_discord_webhook:
        mock_hook = mock_discord_webhook.return_value
        mock_hook.execute.return_value.status_code = HTTP_STATUS_CODE_ERROR

        response = send_webhook(json_data)
        assert response.status_code == HTTP_STATUS_CODE_ERROR


def test_send_webhook_missing_keys() -> None:
    """Test handling when required keys are missing in the GitHub payload."""
    incomplete_json: dict[str, dict[str, dict[str, str]]] = {"sponsorship": {"sponsor": {"login": "sponsor-username"}}}

    with pytest.raises(KeyError):
        send_webhook(incomplete_json)


def test_send_webhook_various_tiers() -> None:
    """Test sending webhooks with different sponsor tiers."""
    json_data: dict[str, dict[str, dict[str, str]]] = {
        "sponsorship": {
            "sponsorable": {"login": "your-username"},
            "sponsor": {
                "login": "sponsor-username",
                "avatar_url": "https://example.com/avatar.jpg",
                "html_url": "https://github.com/sponsor-username",
            },
            "tier": {"name": "$10 per month"},
        },
    }

    with patch("main.DiscordWebhook") as mock_discord_webhook:
        mock_hook = mock_discord_webhook.return_value
        send_webhook(json_data)
        mock_hook.execute.assert_called_once()


if __name__ == "__main__":
    pytest.main()
