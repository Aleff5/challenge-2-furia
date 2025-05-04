from pydantic import BaseModel
import datetime


class FollowRequest(BaseModel):
    user_to_follow_id: int


class FollowResponse(BaseModel):
    message: str
    followed_user_id: int
    followed_at: datetime.datetime
