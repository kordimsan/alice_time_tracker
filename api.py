import logging
import os

from fastapi import Body, FastAPI
from logtail import LogtailHandler

from app import handle_dialog
from models.request import AliceRequest
from models.response import AliceResponse

app = FastAPI()

handler = LogtailHandler(source_token=os.environ.get("LOGTAIL_SOURCE_TOKEN"))
logger = logging.getLogger(__name__)
logger.handlers = []
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


@app.get("/")
async def check_api():
    return "Task tracker has deployed!"


@app.post("/", response_model=AliceResponse)
async def main(request: AliceRequest = Body(...)):  # noqa
    logger.info("Request: %r", request)

    response, tasks = handle_dialog(request)

    return AliceResponse(
        response=response,
        session=request.session,
        user_state_update=tasks,
        version=request.version,
    )
