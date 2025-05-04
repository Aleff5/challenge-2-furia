from typing import List
from fastapi import APIRouter, HTTPException, Depends  
from app.models.games import Game, UserGame
from app.schemas.games import AllGamesResponse, GameFollowReq, GameFollowRes
from app.models.user import User
from app.core.security import get_current_user
import datetime

router = APIRouter()


@router.post("/follow", response_model=GameFollowRes)
async def follow_game(game: GameFollowReq, current_user: User = Depends(get_current_user)):
    gameObj = await Game.get_or_none(id=game.game_id)
    if not gameObj:
        raise HTTPException(status_code=404, detail="Game not found")

    alreadyFollowing = await UserGame.get_or_none(user_id=current_user.id, game_id=game.game_id)
    if alreadyFollowing:
        raise HTTPException(status_code=400, detail="You are already following this game")

    await UserGame.create(user_id=current_user.id, game_id=game.game_id)

    gameObj.followers += 1
    await gameObj.save()

    return GameFollowRes(
        game_id=gameObj.id,
        name=gameObj.name,
        followers=gameObj.followers
    )

@router.get("/following", response_model=List[GameFollowRes])
async def following_games(current_user: User = Depends(get_current_user)):
    # Buscar todos os jogos que o usuário está seguindo
    user_games = await UserGame.filter(user_id=current_user.id).prefetch_related("game")

    # Montar a resposta
    games = []
    for user_game in user_games:
        game = user_game.game
        games.append(GameFollowRes(
            game_id=game.id,
            name=game.name,
            followers=game.followers
        ))

    return games    

@router.get("/all", response_model=List[AllGamesResponse])
async def ShowAllGames():
    games = await Game.all()
    allGames = []
    for game in games:
        allGames.append(AllGamesResponse(
            game_id=game.id,
            name=game.name,
            followers=game.followers
        ))
    return allGames