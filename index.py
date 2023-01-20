from app import AliceHandler
from models.request import AliceRequest
from models.response import AliceResponse


def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """

    request = AliceRequest(**event)

    handler = AliceHandler(request)
    response = handler.handle_dialog()
    tasks = handler.tasks

    if not request.state:
        return AliceResponse(
            response=response,
            session=request.session,
            session_state=[],
            user_state_update=[],
            version=request.version,
        ).dict()
    else:
        return AliceResponse(
            response=response,
            session=request.session,
            session_state=tasks if not request.state.user else None,
            user_state_update=tasks if request.state.user else None,
            version=request.version,
        ).dict()
