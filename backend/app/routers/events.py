from typing import List
from fastapi import APIRouter, HTTPException, Depends  
from app.services.score_service import add_score
from app.models.events import Event, UserEvent
from app.schemas.events import JoinEventReq, JoinEventRes, MyEventsRes,  AllEventsRes
from app.models.user import User
from app.core.security import get_current_user
import datetime


router = APIRouter()

@router.post("/join", response_model=JoinEventRes)
async def JoinEvent(evento:JoinEventReq, currentUser: User = Depends(get_current_user)):
    eventoObj = await Event.get_or_none(id=evento.event_id)
    if not eventoObj:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    
    alreadyJoined = await UserEvent.get_or_none(user_id=currentUser.id, event_id=evento.event_id )
    if alreadyJoined:
        raise HTTPException(status_code=400, detail="Você já se inscreveu nesse evento")
    
    await UserEvent.create(user_id=currentUser.id, event_id=evento.event_id)

    await add_score(currentUser, 50)

    return JoinEventRes(
        event_id=eventoObj.id,
        title=eventoObj.title,
        joined_at=datetime.datetime.utcnow()
    )

@router.get("/myevents", response_model=List[MyEventsRes])
async def MyEvents(currentUser: User = Depends(get_current_user)):
    userEvents = await UserEvent.filter(user_id=currentUser.id).prefetch_related("event")

    events = []
    for userEvent in userEvents:
        event = userEvent.event
        events.append(MyEventsRes(
            event_id=event.id,
            title=event.title,
            description=event.description,
            event_date=event.event_date,
            joined_at=userEvent.joined_at  
        ))
    return events

@router.get("/allevents", response_model=List[AllEventsRes])
async def all_events():
    events = await Event.all()
    return [
        AllEventsRes(
            event_id=event.id,
            title=event.title,
            description=event.description,
            event_date=event.event_date
        ) for event in events
    ]




