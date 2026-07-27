from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from api.dependencies import tm

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get(
        "/",
        include_in_schema=False,
        summary="Главная страница",
        description=(
        "Отображает HTML-страницу со списком всех задач. "
        "Данные извлекаются из базы данных и передаются в шаблон "
        "index.html для последующего рендеринга."
        ),
        response_description="HTML-страница со списком задач",
        responses={
        200: {"description": "Страница успешно сформирована."},
        500: {"description": "Ошибка при получении данных из базы данных."},
        }
)
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


@router.get(
        "/groups-page",
        include_in_schema=False,
        summary="Страница групп",
        description=(
        "Отображает HTML-страницу со списком всех групп. "
        "Для каждой группы выводятся связанные с ней задачи. "
        "Данные передаются в шаблон groups.html."
        ),
        response_description="HTML-страница со списком групп",
        responses={
        200: {"description": "Страница успешно сформирована."},
        500: {"description": "Ошибка при получении данных из базы данных."},
        }
)
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