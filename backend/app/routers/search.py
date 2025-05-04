from fastapi import APIRouter, Depends, Query, HTTPException
from app.models.user import User
from app.models.games import Game, UserGame
from app.core.security import get_current_user
from typing import List
from app.schemas.user_search import UserPublicInfo

router = APIRouter()

@router.get("/search-users", response_model=List[UserPublicInfo])
async def search_users(query: str = Query(..., min_length=2), current_user: User = Depends(get_current_user)):
    users = await User.filter(username__icontains=query).exclude(id=current_user.id).limit(10)
    return [
        UserPublicInfo(id=u.id, username=u.username, avatar_url=u.avatar_url)
        for u in users
    ]


@router.get("/find-players", response_model=List[UserPublicInfo])
async def find_players(game_id: int, current_user: User = Depends(get_current_user)):
    players = await UserGame.filter(game_id=game_id).prefetch_related("user")
    return [
        UserPublicInfo(id=player.user.id, username=player.user.username, avatar_url=player.user.avatar_url)
        for player in players if player.user.id != current_user.id
    ]


@router.get("/find-players-by-game-name", response_model=List[UserPublicInfo])
async def find_players_by_name(name: str, current_user: User = Depends(get_current_user)):
    game = await Game.get_or_none(name__iexact=name)
    if not game:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    players = await UserGame.filter(game_id=game.id).prefetch_related("user")
    return [
        UserPublicInfo(id=player.user.id, username=player.user.username, avatar_url=player.user.avatar_url)
        for player in players if player.user.id != current_user.id
    ]