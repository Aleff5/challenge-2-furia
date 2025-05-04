# app/routers/steam.py

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.core.security import get_current_user
from app.models.user import User
from app.services.social_services import save_social_account
from app.services.score_service import add_score


import os
import httpx
import urllib.parse
import re

router = APIRouter()

STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

@router.get("/auth/social")
def steam_login():
    """Redireciona para login da Steam via OpenID"""
    return_url = os.getenv("STEAM_REDIRECT_URI")
    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": return_url,
        "openid.realm": return_url,
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
    }
    query = urllib.parse.urlencode(params)
    return RedirectResponse(url=f"{STEAM_OPENID_URL}?{query}")



@router.get("/auth/social/callback")
async def steam_callback(request: Request, current_user: User = Depends(get_current_user)):
    
    params = dict(request.query_params)
    params["openid.mode"] = "check_authentication"

    async with httpx.AsyncClient() as client:
        resp = await client.post(STEAM_OPENID_URL, data=params)
        if "is_valid:true" not in resp.text:
            raise HTTPException(status_code=400, detail="Falha na autenticação com a Steam")

    # Extrai steamid do openid.claimed_id
    claimed_id = request.query_params.get("openid.claimed_id", "")
    
    if not claimed_id:
        raise HTTPException(status_code=400, detail="openid.claimed_id não encontrado")


    match = re.search(r"https://steamcommunity.com/openid/id/(\d+)", claimed_id)
    if not match:
        raise HTTPException(status_code=400, detail="SteamID inválido")

    steamid = match.group(1)

    
    api_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steamid}"
    async with httpx.AsyncClient() as client:
        profile_resp = await client.get(api_url)
        profile_data = profile_resp.json().get("response", {}).get("players", [])

    if not profile_data:
        raise HTTPException(status_code=400, detail="Perfil Steam não encontrado")

    profile = profile_data[0]

    await save_social_account(
        user_id=current_user.id,
        platform="steam",
        username = profile.get("personaname", "unknown"),
        profile_url = profile.get("profileurl", ""),
        avatar_url = profile.get("avatarfull", "")

    )
    await add_score(current_user, 100)

    return RedirectResponse(url="http://localhost:5173/perfil")
