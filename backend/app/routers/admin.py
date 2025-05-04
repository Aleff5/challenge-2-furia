import datetime
from app.models.user import User, Follower, SocialAccount
from app.models.sorteios import Sorteio, UserSorteio
from tortoise.transactions import in_transaction
from app.models.events import Event, UserEvent
from app.models.games import Game, UserGame
from tortoise.functions import Count


from fastapi import APIRouter, HTTPException, Depends, Response


router = APIRouter()

@router.get("/total_users")
async def get_total_users():
    total_users = await User.all().count()
    return {"total_users": total_users} 

@router.get("/users_by_state")
async def get_users_by_state():
    users_by_state = await User.all().group_by("estado").annotate(total=Count("id")).values("estado", "total")
    resultado = [{"estado": u["estado"], "total": u["total"]} for u in users_by_state if u["estado"]]
    return resultado

@router.get("/most_followed_games")
async def get_most_followed_games():
    top_games = await Game.all().order_by("-followers").limit(10)
    ranking = [{ "nome": game.name, "seguidores": game.followers } for game in top_games]
    return ranking


@router.get("/event_engagement")
async def get_event_engagement():
    data = await UserEvent.all().group_by("event_id").annotate(total=Count("user_id")).values("event_id", "total")
    eventos = await Event.all().values("id", "title")
    evento_map = {e["id"]: e["title"] for e in eventos}
    return [
        {
            "event_id": item["event_id"],
            "title": evento_map.get(item["event_id"], "Desconhecido"),
            "participantes": item["total"]
        }
        for item in data
    ]


@router.get("/verified-users")
async def get_verified_users():
    total = await User.filter(is_verified=True).count()
    return {"usuarios_verificados": total}

@router.get("/age-distribution")
async def get_age_distribution():
    faixa_etaria = {
        "13-17": await User.filter(idade__gte=13, idade__lte=17).count(),
        "18-24": await User.filter(idade__gte=18, idade__lte=24).count(),
        "25-34": await User.filter(idade__gte=25, idade__lte=34).count(),
        "35-44": await User.filter(idade__gte=35, idade__lte=44).count(),
        "45+": await User.filter(idade__gte=45).count(),
    }
    return faixa_etaria

@router.get("/user-ranking")
async def get_user_ranking():
    top_users = await User.all().order_by("-score").limit(10).values("username", "score")
    return top_users

@router.get("/sorteios-ativos")
async def get_active_sorteios():
    today = datetime.datetime.today().date()
    sorteios = await Sorteio.filter(start_date__lte=today, end_date__gte=today).values("id", "title", "start_date", "end_date")
    return {"ativos": sorteios}

@router.get("/eventos-ativos")
async def get_active_events():
    today = datetime.datetime.today().date()
    eventos = await Event.filter(event_date__gte=today).values("id", "title", "event_date")
    return {"ativos": eventos}


@router.get("/crescimento-usuarios")
async def get_user_growth():
    query = """
        SELECT DATE_TRUNC('month', created_at) AS mes, COUNT(id) AS total
        FROM users
        WHERE created_at >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY mes
        ORDER BY mes;
    """
    async with in_transaction() as conn:
        rows = await conn.execute_query_dict(query)

    return [{"mes": row["mes"].strftime("%Y-%m"), "total": row["total"]} for row in rows]

