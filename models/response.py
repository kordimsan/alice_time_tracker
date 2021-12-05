# generated by datamodel-codegen:
#   filename:  response_example.json
#   timestamp: 2021-11-27T19:09:05+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, validator

from models.custom import UserState


class User(BaseModel):
    user_id: str


class Application(BaseModel):
    application_id: str


class Session(BaseModel):
    message_id: int
    session_id: str
    skill_id: str
    user: Optional[User]
    application: Application
    new: bool
    user_id: str


class Button(BaseModel):
    title: str
    hide: bool


class Response(BaseModel):
    end_session: bool = False
    text: str
    tts: str = None
    buttons: List[Button] = []

    @validator("tts", pre=True, always=True)
    def default_tts(cls, v, *, values, **kwargs):
        return v or values["text"]


class AliceResponse(BaseModel):
    response: Response
    session: Session
    session_state: Optional[dict]
    user_state_update: Optional[UserState]
    application_state: Optional[dict]
    version: str
