from fastapi import APIRouter, HTTPException, Depends 
from fastapi.responses import RedirectResponse
import httpx
# from app.services.twitter_service import get_twitter_auth_url, get_twitter_user_info
from app.models.user import User
from jose import jwt
from app.core.security import get_current_user
from app.services.social_services import save_social_account
from fastapi.responses import RedirectResponse
import os
import datetime
from app.services.score_service import add_score
from pathlib import Path

from dotenv import load_dotenv
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

router = APIRouter()


@router.get("/auth/social")
def redirect_to_discord():
    client_id = os.getenv("DISCORD_CLIENT_ID")
    redirect_uri = os.getenv("DISCORD_REDIRECT_URI")
    return RedirectResponse(
        f"https://discord.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify"
    )

@router.get("/auth/social/callback")
async def discord_callback(code: str, current_user: User = Depends(get_current_user)):
    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": os.getenv("DISCORD_CLIENT_ID"),
        "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(token_url, data=data, headers=headers)
        if token_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Erro ao obter token do Discord")
        token_data = token_resp.json()
        access_token = token_data["access_token"]

        # Obter dados do usuário
        user_resp = await client.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"}
        )   
        user_data = user_resp.json()
        if "id" not in user_data or "username" not in user_data:
            raise HTTPException(status_code=400, detail="Erro ao obter dados do Discord")
        avatar_id = user_data.get("avatar")
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{avatar_id}.png" if avatar_id else None


        # Salvar social
        await save_social_account(
            user_id=current_user.id,
            platform="discord",
            username=user_data["username"],
            profile_url=f"https://discord.com/users/{user_data['id']}",
            avatar_url=f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.png"
            )

        await add_score(current_user, 100)


    return RedirectResponse(url="http://localhost:5173/perfil")  # redirecione pro seu frontend