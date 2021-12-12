# generated by datamodel-codegen:
#   filename:  request_example.json
#   timestamp: 2021-11-28T19:00:48+00:00

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from models.custom import UserState


class Interfaces(BaseModel):
    screen: Dict[str, Any] = {}
    payments: Dict[str, Any] = {}
    account_linking: Dict[str, Any] = {}


class Meta(BaseModel):
    locale: str
    timezone: str
    client_id: str
    interfaces: Interfaces


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
    user_id: str
    new: bool


class Tokens(BaseModel):
    start: int
    end: int


class TaskName(BaseModel):
    type: str
    tokens: Tokens
    value: str


class Slots(BaseModel):
    task_name: Optional[TaskName]


class IntentSlots(BaseModel):
    slots: Slots


class Intents(BaseModel):
    add_task: Optional[IntentSlots]
    pause_task: Optional[IntentSlots]
    result_task: Optional[IntentSlots]
    results: Optional[IntentSlots]
    resume_task: Optional[IntentSlots]
    help: Optional[IntentSlots]


class Nlu(BaseModel):
    tokens: List[str]
    entities: List
    intents: Optional[Intents]


class Markup(BaseModel):
    dangerous_context: bool


class Request(BaseModel):
    command: str
    original_utterance: str
    nlu: Nlu
    markup: Markup
    type: str


class State(BaseModel):
    session: Optional[UserState]
    user: Optional[UserState]
    application: Optional[UserState]


class AliceRequest(BaseModel):
    meta: Meta
    request: Request
    session: Session
    state: Optional[State]
    version: str
