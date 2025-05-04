from pydantic import BaseModel


class AllGamesResponse(BaseModel):
    game_id: int
    name: str
    followers: int


class GameFollowReq(BaseModel):
    game_id: int


class GameFollowRes(BaseModel):
    game_id: int
    name: str
    followers: int
