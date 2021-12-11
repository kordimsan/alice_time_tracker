from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


class Task(BaseModel):
    id: str = "stop_any_task"
    name: str = None
    date_time: datetime = None

    @validator("date_time", pre=True, always=True)
    def default_ts_created(cls, v):
        return v or datetime.utcnow()


class UserState(BaseModel):
    tasks: List[Task] = []
