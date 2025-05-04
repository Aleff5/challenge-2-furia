# app/routers/follow.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import Follower
from app.models.user import User
from app.schemas.follow import FollowRequest, FollowResponse
from app.core.security import get_current_user
from tortoise.exceptions import IntegrityError
from datetime import datetime

router = APIRouter()

@router.post("/follow", response_model=FollowResponse)
async def follow_user(request: FollowRequest, current_user: User = Depends(get_current_user)):
    if request.user_to_follow_id == current_user.id:
        raise HTTPException(status_code=400, detail="Você não pode se seguir.")

    user_to_follow = await User.get_or_none(id=request.user_to_follow_id)
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="Usuário a ser seguido não encontrado")

    existing = await Follower.get_or_none(follower=current_user, following=user_to_follow)
    if existing:
        raise HTTPException(status_code=400, detail="Você já segue esse usuário.")

    try:
        follow = await Follower.create(
            follower=current_user,
            following=user_to_follow
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Falha ao seguir o usuário.")

    return FollowResponse(
        message="Usuário seguido com sucesso",
        followed_user_id=user_to_follow.id,
        followed_at=follow.created_at
    )



@router.get("/followers")
async def list_my_followers(current_user: User = Depends(get_current_user)):
    followers = await Follower.filter(following=current_user.id).prefetch_related("follower")
    return [
        {
            "user_id": f.follower.id,
            "username": f.follower.username,
            "followed_at": f.created_at
        }
        for f in followers
    ]


@router.get("/following")
async def list_who_i_follow(current_user: User = Depends(get_current_user)):
    following = await Follower.filter(follower=current_user.id).prefetch_related("following")
    return [
        {
            "user_id": f.following.id,
            "username": f.following.username,
            "followed_at": f.created_at
        }
        for f in following
    ]
