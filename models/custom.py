from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


class Task(BaseModel):
    name: str
    date_time: datetime = None

    @validator("date_time", pre=True, always=True)
    def default_ts_created(cls, v):
        return v or datetime.utcnow()


class UserState(BaseModel):
    tasks: List[Task] = []
