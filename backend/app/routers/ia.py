
from fastapi import APIRouter, HTTPException, Depends 
from fastapi.responses import RedirectResponse
import httpx
# from app.services.twitter_service import get_twitter_auth_url, get_twitter_user_info
from app.models.user import User
from app.models.games import Game, UserGame
from jose import jwt
from app.core.security import get_current_user
from app.services.social_services import save_social_account
from fastapi.responses import RedirectResponse
import os
import datetime
from app.services.score_service import add_score
from pathlib import Path
from app.services.rss_colector import fetch_rss_feeds
from app.services.classify_news import classify_news_by_user
router = APIRouter()

@router.get("/personalized_news")


async def personalized_news(current_user: User = Depends(get_current_user)):
    # Busca as notícias
    news = fetch_rss_feeds()

    # Busca os jogos seguidos pelo usuário
    user_game_relations = await UserGame.filter(user_id=current_user.id).prefetch_related("game")
    games_followed = [rel.game.name for rel in user_game_relations]

    # Trata os interesses
    interesses = current_user.interesses.split(",") if current_user.interesses else []

    # Monta o perfil
    user_profile = {
        "bio": current_user.bio or "",
        "interests": interesses,
        "games_followed": games_followed
    }

    # Classifica via Gemini
    resultado = classify_news_by_user(news, user_profile)
    return resultado