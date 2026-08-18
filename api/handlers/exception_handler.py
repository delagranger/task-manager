from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions.exceptions import StatusNotFound, GIDNotFound, TIDNotFound, GroupNotFound, GroupAlreadyExists, SortTypeNotFound, FilterNotExists, IncorrectLength, DefaultGroupProtectedError


STATUS_CODES = {
    GIDNotFound: 404,
    TIDNotFound: 404,
    GroupNotFound: 404,
    GroupAlreadyExists: 404,
    StatusNotFound: 400,
    SortTypeNotFound: 400,
    FilterNotExists: 400,
    IncorrectLength: 400,
    DefaultGroupProtectedError: 403,
}


async def validation_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=STATUS_CODES[type(exc)], content={"detail": str(exc)})
