from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User
from app.models.games import UserGame
from app.services.rss_colector import fetch_rss_feeds
from app.services.classify_news import classify_news_by_user

router = APIRouter()

@router.get("/news")
async def personalized_news(current_user: User = Depends(get_current_user)):
    news = fetch_rss_feeds()
    

    user_games = await UserGame.filter(user=current_user).prefetch_related("game")
    games_followed = [ug.game.name for ug in user_games]
    
    user_profile = {
        "bio": current_user.bio or "",
        "interests": current_user.interesses.split(",") if current_user.interesses else [],  # Convertendo string para lista
        "games_followed": games_followed
    }
    
    return classify_news_by_user(news, user_profile)
