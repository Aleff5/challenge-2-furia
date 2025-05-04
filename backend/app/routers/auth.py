from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
# from app.services.twitter_service import get_twitter_auth_url, get_twitter_user_info
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.schemas.auth import LoginResponse, LoginRequest
from passlib.hash import bcrypt 
from jose import jwt
from app.core.security import get_current_user
from fastapi.responses import RedirectResponse
from app.services.score_service import add_score
import os
import datetime



SECRET_KEY = "default_dev_secret"  
 # depois colocar isso num .env
ALGORITHM = "HS256"

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    existing_user = await User.get_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hash(user.password)

    user_obj = await User.create(
        username=user.username,
        email=user.email,
        password=hashed_password,
        nome=user.nome,
        cpf=user.cpf,
        bio=user.bio,
        estado=user.estado,
        endereco=user.endereco,
        interesses=user.interesses,
        documento_url=user.documento_url,
        avatar_url=user.avatar_url,
        discord=user.discord,
        twitter=user.twitter,
        steam=user.steam,
        google=user.google
)


    await add_score(user_obj, 200)

    return user_obj

@router.post("/login")
async def login(user: LoginRequest, response: Response):
    existing_user = await User.get_or_none(email=user.email)
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Usuário não existe")

    if not bcrypt.verify(user.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Senha inválida")

    # Gerar JWT Token
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    to_encode = {"sub": str(existing_user.id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Definir o cookie no Response original
    response.set_cookie(
        key="access_token",
        value=encoded_jwt,
        httponly=True,
        max_age=7200,
        expires=7200,
        secure=True,
        samesite="None"
    )

    return {"message": "Login efetuado com sucesso"}



   
@router.post("/admin/login")
async def admin_login(user: LoginRequest, response: Response):
    existing_user = await User.get_or_none(email=user.email)
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Usuário não existe")

    if not bcrypt.verify(user.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Senha inválida")

    if not existing_user.admin:
        raise HTTPException(status_code=403, detail="Acesso negado: não é administrador")

    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    to_encode = {
        "sub": str(existing_user.id),
        "exp": expire,
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    response.set_cookie(
        key="access_token",
        value=encoded_jwt,
        httponly=True,
        max_age=7200,
        expires=7200,
        secure=True,
        samesite="None"
    )

    return {"message": "Login de administrador efetuado com sucesso"}