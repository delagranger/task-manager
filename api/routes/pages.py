from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from api.dependencies import tm

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def index(request: Request):

    tasks = tm.list_tasks(
        sort_type="id",
        filtered=False,
        status="",
        group=""
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "tasks": tasks
        }
    )


@router.get("/groups-page")
def groups_page(request: Request):

    groups = tm.list_groups(
        sort_type="id"
    )

    return templates.TemplateResponse(
        request=request,
        name="groups.html",
        context={
            "groups": groups
        }
    )