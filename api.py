import logging

from fastapi import Body, FastAPI
from pydantic import BaseModel

from app import handle_dialog

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)


class Request(BaseModel):
    request = Body(...)


# Задаем параметры приложения FastAPI.
@app.post("/")
async def main(request=Request):
    # Функция получает тело запроса и возвращает ответ.
    logging.info("Request: %r", request)

    response = {
        "version": request["version"],
        "session": request["session"],
        "response": {"end_session": False},
    }

    handle_dialog(request, response)

    logging.info("Response: %r", response)

    return response
