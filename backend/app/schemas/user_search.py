from pydantic import BaseModel

class UserPublicInfo(BaseModel):
    id: int
    username: str
    avatar_url: str | None
