from fastapi import FastAPI # type: ignore
from app.core.database import init_db
from app.routers.auth import router as auth_router
from app.routers.discord import router as discord_router
from app.routers.events import router as events_router
from app.routers.follow import router as follow_router
from app.routers.game import router as game_router
from app.routers.search import router as search_router
from app.routers.sorteios import router as sorteio_router
from app.routers import steam
from app.routers.admin import router as admin_router   
from app.routers.twitter import router as twitter_router
from app.routers.verify import router as verify_router
from app.routers.ia import router as ia_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv(dotenv_path=".env")


app = FastAPI()


# Origem do frontend, você pode ajustar depois para o domínio real em produção
origins = [
    "http://localhost:5173",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],            # ou ["*"] em desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await init_db()


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(events_router, prefix="/events", tags=["eventos"])
app.include_router(sorteio_router, prefix="/sorteio", tags=["sorteios"])
app.include_router(game_router, prefix="/game", tags=["games"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

app.include_router(ia_router, prefix="/ia", tags=["IA"])
app.include_router(follow_router, prefix="/user", tags=["Follow"])
app.include_router(discord_router, prefix="/discord", tags=["Discord"])
app.include_router(search_router)
app.include_router(steam.router, prefix="/steam"    , tags=["Steam"])
app.include_router(twitter_router, prefix="/twitter", tags=["Twitter"])
app.include_router(verify_router, prefix="/documents", tags=["Upload de Documentos"])

@app.get("/")
def read_root():
    return {"message": "Furia Hub API - Online"}
