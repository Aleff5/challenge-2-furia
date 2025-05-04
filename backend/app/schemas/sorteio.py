from pydantic import BaseModel
import datetime
from typing import Optional


class EntrarSorteioReq(BaseModel):
    sorteio_id: int


class EntrarSorteioRes(BaseModel):
    sorteio_id: int
    title: str
    joined_at: datetime.datetime


class TodosSorteios(BaseModel):
    sorteio_id: int
    title: str
    description: Optional[str]
    start_date: datetime.datetime
    end_date: datetime.datetime
