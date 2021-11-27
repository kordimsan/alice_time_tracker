import logging

from fastapi import Body, FastAPI

from app import handle_dialog
from models.request import AliceRequest

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)


# Задаем параметры приложения FastAPI.
@app.post("/")
async def main(request: AliceRequest = Body(...)):  # noqa
    # Функция получает тело запроса и возвращает ответ.
    logging.info("Request: %r", request)
    request = request.dict()
    response = {
        "version": request["version"],
        "session": request["session"],
        "response": {"end_session": False},
    }

    handle_dialog(request, response)

    logging.info("Response: %r", response)

    return response
