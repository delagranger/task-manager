from fastapi import FastAPI

from api.routes.tasks import router as tasks_router
from api.routes.groups import router as groups_router
from api.routes.pages import router as pages_router
from config import log_setup

log_setup()

app = FastAPI()

app.include_router(tasks_router, prefix="/api/v1")
app.include_router(groups_router, prefix="/api/v1")
app.include_router(pages_router)
    