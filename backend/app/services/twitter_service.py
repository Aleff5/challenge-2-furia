import os
import httpx
from datetime import datetime
from app.models.user import SocialAccount
from requests_oauthlib import OAuth1Session
import os
from pathlib import Path

from dotenv import load_dotenv
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
USER_INFO_URL = "https://api.twitter.com/1.1/account/verify_credentials.json"

# def get_twitter_auth_url():
#     oauth = OAuth1Session(
#         os.getenv("TWITTER_API_KEY"),
#         client_secret=os.getenv("TWITTER_API_SECRET"),
#         callback_uri=os.getenv("TWITTER_CALLBACK_URL")
#     )

#     tokens = oauth.fetch_request_token(REQUEST_TOKEN_URL)
#     auth_url = f"{AUTHENTICATE_URL}?oauth_token={tokens['oauth_token']}"
#     return auth_url, tokens

# def get_twitter_user_info(oauth_token, oauth_verifier):
#     oauth = OAuth1Session(
#         os.getenv("TWITTER_API_KEY"),
#         client_secret=os.getenv("TWITTER_API_SECRET"),
#         resource_owner_key=oauth_token,
#         verifier=oauth_verifier
#     )
#     tokens = oauth.fetch_access_token(ACCESS_TOKEN_URL)
#     oauth = OAuth1Session(
#         os.getenv("TWITTER_API_KEY"),
#         client_secret=os.getenv("TWITTER_API_SECRET"),
#         resource_owner_key=tokens['oauth_token'],
#         resource_owner_secret=tokens['oauth_token_secret']
#     )
#     user_info = oauth.get(USER_INFO_URL, params={"include_email": "true"}).json()
#     return user_info


TWITTER_CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
TWITTER_CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
TWITTER_REDIRECT_URI = os.getenv("TWITTER_REDIRECT_URI")
TWITTER_SCOPE = "tweet.read users.read like.read follows.read"
TWITTER_API_BASE = "https://api.twitter.com/2"
TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
USER_URL = f"{TWITTER_API_BASE}/users/me"
LIKES_URL = f"{TWITTER_API_BASE}/users/{{user_id}}/liked_tweets"
FOLLOWING_URL = f"{TWITTER_API_BASE}/users/{{user_id}}/following"

async def exchange_code_for_token(code: str, code_verifier: str):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": TWITTER_REDIRECT_URI,
        "client_id": TWITTER_CLIENT_ID,
        "code_verifier": code_verifier,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(TOKEN_URL, data=data, headers=headers)
        resp.raise_for_status()
        return resp.json()

async def get_twitter_user_data(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(USER_URL, headers=headers)
        resp.raise_for_status()
        return resp.json()

async def check_follow_furia(user_id: str, access_token: str) -> bool:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(FOLLOWING_URL.format(user_id=user_id), headers=headers)
        data = resp.json()
        return any(user["username"].lower() == "furiagg" for user in data.get("data", []))

async def check_likes_furia(user_id: str, access_token: str) -> int:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(LIKES_URL.format(user_id=user_id), headers=headers)
        data = resp.json()
        return sum(1 for tweet in data.get("data", []) if "furia" in tweet.get("text", "").lower())

async def save_twitter_account(user_id: int, username: str, profile_url: str, avatar_url: str):
    existing = await SocialAccount.get_or_none(user_id=user_id, platform="twitter")
    if existing:
        existing.username = username
        existing.profile_url = profile_url
        existing.avatar_url = avatar_url
        existing.last_checked = datetime.utcnow()
        await existing.save()
    else:
        await SocialAccount.create(
            user_id=user_id,
            platform="twitter",
            username=username,
            profile_url=profile_url,
            avatar_url=avatar_url,
            connected_at=datetime.utcnow(),
            last_checked=datetime.utcnow()
        )
