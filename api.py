import logging
from pprint import pprint

from fastapi import Body, FastAPI

from app import handle_dialog
from models.request import AliceRequest
from models.response import AliceResponse

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)


@app.get("/")
async def check_api():
    return "Task tracker has deployed!"


@app.post("/", response_model=AliceResponse)
async def main(request: AliceRequest = Body(...)):  # noqa
    pprint(request)

    response, tasks = handle_dialog(request)

    return AliceResponse(
        response=response,
        session=request.session,
        session_state=tasks if not request.state.user else None,
        user_state_update=tasks if request.state.user else None,
        version=request.version,
    )
