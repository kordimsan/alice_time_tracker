import logging

from fastapi import Body, FastAPI

from app import handle_dialog
from models.request import AliceRequest
from models.response import AliceResponse

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)


@app.post("/", response_model=AliceResponse)
async def main(request: AliceRequest = Body(...)):  # noqa
    logging.info("Request: %r", request)

    response, tasks = handle_dialog(request)

    return AliceResponse(
        response=response,
        session=request.session,
        user_state_update=tasks,
        version=request.version,
    )
