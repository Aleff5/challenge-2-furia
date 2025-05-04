from pydantic import BaseModel
import datetime
from typing import Optional


class JoinEventReq(BaseModel):
    event_id: int


class JoinEventRes(BaseModel):
    event_id: int
    title: str
    joined_at: datetime.datetime


class MyEventsRes(BaseModel):
    event_id: int
    title: str
    description: Optional[str]
    event_date: datetime.datetime
    joined_at: datetime.datetime


class AllEventsRes(BaseModel):
    event_id: int
    title: str
    description: Optional[str]
    event_date: datetime.datetime


