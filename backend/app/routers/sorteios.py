from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.services.score_service import add_score
from typing import List
from datetime import datetime
from app.models.sorteios import Sorteio, UserSorteio
from app.models.user import User
from app.schemas.sorteio import TodosSorteios, EntrarSorteioReq, EntrarSorteioRes
from app.core.security import get_current_user

router = APIRouter()

# 🔹 1. Listar todos os sorteios
@router.get("/all", response_model=List[TodosSorteios])
async def list_all():
    raffles = await Sorteio.all()
    return [
        TodosSorteios(
            sorteio_id=r.id,
            title=r.title,
            description=r.description,
            start_date=r.start_date,
            end_date=r.end_date
        ) for r in raffles
    ]


@router.post("/join", response_model=EntrarSorteioRes)
async def join_sorteio(req: EntrarSorteioReq, current_user: User = Depends(get_current_user)):
    raffle = await Sorteio.get_or_none(id=req.sorteio_id)
    if not raffle:
        raise HTTPException(status_code=404, detail="Sorteio não encontrado")

    already = await UserSorteio.get_or_none(user_id=current_user.id, sorteio_id=req.sorteio_id)
    if already:
        raise HTTPException(status_code=400, detail="Você já está inscrito neste sorteio")

    # 🔧 Aqui usamos datetime com timezone (UTC)
    entry = await UserSorteio.create(
        user_id=current_user.id,
        sorteio_id=req.sorteio_id,
        # joined_at=datetime.now(timezone.utc)  
    )

    await add_score(current_user, 50)

    return EntrarSorteioRes(
        sorteio_id=raffle.id,
        title=raffle.title,
        joined_at=entry.joined_at
    )


# 🔹 3. Ver meus sorteios
@router.get("/myraffles", response_model=List[EntrarSorteioRes])
async def my_raffles(current_user: User = Depends(get_current_user)):
    user_sorteios = await UserSorteio.filter(user_id=current_user.id).prefetch_related("sorteio")

    return [
        EntrarSorteioRes(
            sorteio_id=us.sorteio.id,
            title=us.sorteio.title,
            joined_at=us.joined_at
        ) for us in user_sorteios
    ]
