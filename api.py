import logging

from fastapi import Body, FastAPI

from app import handle_dialog
from models.request import AliceRequest

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)


@app.post("/")
async def main(request: AliceRequest = Body(...)):  # noqa
    logging.info("Request: %r", request)
    response = handle_dialog(request)
    logging.info("Response: %r", response)
    return response
