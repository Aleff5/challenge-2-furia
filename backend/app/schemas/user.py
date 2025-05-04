import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    idade: Optional[int] = None
    nome: str
    cpf: str
    bio: Optional[str] = None
    score: int = 0
    estado: Optional[str] = None
    endereco: Optional[str] = None
    interesses: Optional[str] = None
    documento_url: Optional[str] = None
    avatar_url: Optional[str] = None
    discord: Optional[str] = None
    twitter: Optional[str] = None
    steam: Optional[str] = None
    google: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    nome: str
    avatar_url: Optional[str] = None
    score: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class UserPublicInfo(BaseModel):
    id: int
    username: str
    avatar_url: Optional[str]






