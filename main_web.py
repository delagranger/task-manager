from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes.tasks import router as tasks_router
from api.routes.groups import router as groups_router
from api.routes.pages import router as pages_router

from api.handlers.exception_handler import validation_error_handler

from exceptions.exceptions import (StatusNotFound, GIDNotFound, TIDNotFound, 
                                   GroupNotFound, GroupAlreadyExists, 
                                   SortTypeNotFound, FilterNotExists, 
                                   IncorrectLength
                                   )

from config import log_setup

log_setup()

app = FastAPI(
    title="Task Manager API",
    version="1.0",
    description="""
REST API для управления задачами и группами.

### Возможности

- создание задач;
- изменение задач;
- удаление задач;
- получение списка задач;
- создание и управление группами;
- сортировка и фильтрация результатов.

API разработан на FastAPI с использованием SQLAlchemy и PostgreSQL.
"""
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(GIDNotFound, validation_error_handler)
app.add_exception_handler(TIDNotFound, validation_error_handler)
app.add_exception_handler(GroupNotFound, validation_error_handler)
app.add_exception_handler(GroupAlreadyExists, validation_error_handler)
app.add_exception_handler(StatusNotFound, validation_error_handler)
app.add_exception_handler(SortTypeNotFound, validation_error_handler)
app.add_exception_handler(FilterNotExists, validation_error_handler)
app.add_exception_handler(IncorrectLength, validation_error_handler)

app.include_router(tasks_router, prefix="/api/v1")
app.include_router(groups_router, prefix="/api/v1")
app.include_router(pages_router)
     