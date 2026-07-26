from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions.exceptions import StatusNotFound, GIDNotFound, TIDNotFound, GroupNotFound, SortTypeNotFound, FilterNotExists, IncorrectLength


async def group_id_not_found_handler(request: Request, exc: GIDNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"Details": str(exc)})


async def task_id_not_found_handler(request: Request, exc: TIDNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"Details": str(exc)})


async def group_not_found_handler(request: Request, exc: GroupNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"Details": str(exc)})


async def status_not_found_handler(request: Request, exc: StatusNotFound) -> JSONResponse:
    return JSONResponse(status_code=400, content={"Details": str(exc)})


async def sort_type_not_found_handler(request: Request, exc: SortTypeNotFound) -> JSONResponse:
    return JSONResponse(status_code=400, content={"Details": str(exc)})


async def filter_not_exists_handler(request: Request, exc: FilterNotExists) -> JSONResponse:
    return JSONResponse(status_code=400, content={"Details": str(exc)})


async def incorrect_length_handler(request: Request, exc: IncorrectLength) -> JSONResponse:
    return JSONResponse(status_code=400, content={"Details": str(exc)})