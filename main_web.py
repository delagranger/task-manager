from fastapi import FastAPI

from api.routes.tasks import router as tasks_router
from api.routes.groups import router as groups_router
from api.routes.pages import router as pages_router

from api.handlers.exception_handler import (group_id_not_found_handler, 
                                            task_id_not_found_handler, 
                                            group_not_found_handler, 
                                            status_not_found_handler, 
                                            sort_type_not_found_handler, 
                                            filter_not_exists_handler, 
                                            incorrect_length_handler
                                            )

from exceptions.exceptions import (StatusNotFound, GIDNotFound, TIDNotFound, 
                                   GroupNotFound, SortTypeNotFound, FilterNotExists, 
                                   IncorrectLength
                                   )

from config import log_setup

log_setup()

app = FastAPI()

app.add_exception_handler(GIDNotFound, group_id_not_found_handler)
app.add_exception_handler(TIDNotFound, task_id_not_found_handler)
app.add_exception_handler(GroupNotFound, group_not_found_handler)
app.add_exception_handler(StatusNotFound, status_not_found_handler)
app.add_exception_handler(SortTypeNotFound, sort_type_not_found_handler)
app.add_exception_handler(FilterNotExists, filter_not_exists_handler)
app.add_exception_handler(IncorrectLength, incorrect_length_handler)

app.include_router(tasks_router, prefix="/api/v1")
app.include_router(groups_router, prefix="/api/v1")
app.include_router(pages_router)
    