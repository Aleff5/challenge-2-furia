import os
import hashlib
import base64
import secrets
from uuid import uuid4
from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from app.core.security import get_current_user
from app.models.user import User
from app.services.score_service import add_score
from app.services.twitter_service import (
    exchange_code_for_token,
    get_twitter_user_data,
    save_twitter_account,
    check_follow_furia,
    check_likes_furia
)
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

router = APIRouter()

# Simulação de armazenamento de sessão (substituir por Redis ou banco real)
session_storage = {}

@router.get("/auth/social/")
async def twitter_login():
    # Geração segura do PKCE
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode()

    # Geração de state único
    state = uuid4().hex

    # Armazenamento temporário (exemplo simplificado)
    session_storage[state] = code_verifier

    redirect_uri = os.getenv("TWITTER_REDIRECT_URI")
    client_id = os.getenv("TWITTER_CLIENT_ID")
    scope = "tweet.read users.read like.read follows.read"

    auth_url = (
        "https://twitter.com/i/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        f"&state={state}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )

    return RedirectResponse(auth_url)


@router.get("/auth/social/callback")
async def twitter_callback(request: Request, current_user: User = Depends(get_current_user)):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state:
        raise HTTPException(status_code=400, detail="Código ou state ausente")

    code_verifier = session_storage.pop(state, None)
    if not code_verifier:
        raise HTTPException(status_code=400, detail="Verifier não encontrado ou expirado")

    # Troca o código por token
    token_data = await exchange_code_for_token(code, code_verifier)
    access_token = token_data["access_token"]

    # Obtém dados do Twitter
    user_data = await get_twitter_user_data(access_token)
    username = user_data["data"]["username"]
    user_id_str = user_data["data"]["id"]

    await save_twitter_account(
        user_id=current_user.id,
        username=username,
        profile_url=f"https://twitter.com/{username}",
        avatar_url="https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png"
    )

    await add_score(current_user, 100)

    if await check_follow_furia(user_id_str, access_token):
        await add_score(current_user, 100)

    likes = await check_likes_furia(user_id_str, access_token)
    if likes > 0:
        await add_score(current_user, likes * 25)

    frontend_url = os.getenv("FRONTEND_REDIRECT_URL", "http://localhost:8000/perfil")
    return RedirectResponse(url=frontend_url)
