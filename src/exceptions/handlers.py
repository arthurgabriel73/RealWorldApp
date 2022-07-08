from starlette.requests import Request
from starlette.responses import JSONResponse
from src.exceptions.api_exception import APIException


def handle_api_exception(request: Request, exc: APIException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content={"error": exc.message}
    )
