import os
import sys

import requests
from discord_webhook import DiscordEmbed, DiscordWebhook
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

# Take environment variables from .env.
load_dotenv(verbose=True)

# Get the webhook URL.
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", default=None)
if not WEBHOOK_URL:
    sys.exit("You need to fill out the .env or add WEBHOOK_URL to your environment.")


@app.get("/")
async def root():
    """
    Our index page.
    """
    return {"message": "Hello World"}


@app.post("/webhook")
async def webhook(request: Request) -> dict[str, str]:
    """
    This is where GitHub will send webhooks to.

    First we check if the x-github-event header is for sponsorships.
    Then we parse your username, their username, avatar, URL to profile, sponsor tier and then create the message
    that we will send to Discord.

    Args:
        request: The HTTP request that contains the JSON from GitHub.

    Returns:
        A message that everything was a success.
    """
    # The JSON response from GitHub.
    response = await request.json()

    # Check if header is correct.
    await check_header(request)

    # Send webhook to Discord.
    send_webhook(response)

    # Return a message so GitHub will be happy.
    return {"status": "SUCCESS"}


async def check_header(request) -> None:
    """
    Check if header is correct.

    Every webhook from GitHub has a header with the name of the event that triggered the delivery.

    Args:
        request: The HTTP request that contains the JSON from GitHub.

    Raises:
        HTTPException: If the header is not "sponsorship".
    """
    x_github_event: str = request.headers.get("x-github-event")
    if x_github_event != "sponsorship":
        raise HTTPException(status_code=500, detail="Only sponsorships are allowed.")


def send_webhook(response, webhook_url=WEBHOOK_URL) -> requests.Response:
    """
    Create the webhook and send to Discord.

    Args:
        response: The JSON response from GitHub.
        webhook_url: The URL to the webhook.
    """
    # Your GitHub username.
    owner_username = response["sponsorship"]["sponsorable"]["login"]

    # Their username, avatar and URL to profile.
    sponsor_login = response["sponsorship"]["sponsor"]["login"]
    sponsor_avatar = response["sponsorship"]["sponsor"]["avatar_url"]
    sponsor_url = response["sponsorship"]["sponsor"]["html_url"]

    # The name of the sponsor tier, for example '$1 one time'.
    sponsor_tier_name = response["sponsorship"]["tier"]["name"]

    # The message we will send to Discord.
    message = f"{owner_username} got a sponsor from {sponsor_login}:\n{sponsor_tier_name}"

    # Send a webhook to Discord.
    hook = DiscordWebhook(url=webhook_url, rate_limit_retry=True, username="GitHub sponsors")
    embed = DiscordEmbed(description=message, color="171515")
    embed.set_author(name=sponsor_login, url=sponsor_url, icon_url=sponsor_avatar)
    hook.add_embed(embed)
    return hook.execute()
