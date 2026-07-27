from fastapi import APIRouter

from api.dependencies import tm
from api.schemas.group import GroupCreate, GroupPatch

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get(
        "/",
        summary="Получить список групп",
        description=(
        "Возвращает список всех групп, отсортированных по выбранному полю. "
        "Для каждой группы также отображается список связанных задач."
        ),
        status_code=200,
        responses={
        200: {"description": "Список групп успешно получен."},
        400: {"description": "Передан некорректный параметр сортировки."},
        }
)
def get_groups(sort_type: str = "id"):
    return tm.list_groups(sort_type)


@router.post(
        "/",
        summary="Создать новую группу",
        description=(
        "Создает новую группу для задач. "
        "Перед сохранением проверяется корректность названия группы."
        ),
        status_code=201,
        responses={
        201: {"description": "Группа успешно создана."},
        404: {"description": "Группа уже существует"},
        400: {"description": "Некорректное название группы."},
        }
)
def post_group(group: GroupCreate):
    return tm.add_group(group.title)


@router.delete(
        "/{id}",
        summary="Удалить группу",
        description=(
        "Удаляет группу по идентификатору. "
        "Все задачи, принадлежавшие удаляемой группе, автоматически "
        "переносятся в группу default group."
        ),
        status_code=200,
        responses={
        200: {"description": "Группа успешно удалена."},
        404: {"description": "Группа с указанным идентификатором не найдена."},
        }
)
def delete_group(id: int):
    tm.delete_group(id)
    return {
        "message" : f"Group with id={id} deleted!"
    }


@router.patch(
        "/{id}",
        summary="Изменить группу",
        description=(
        "Изменяет название группы."
        ),
        status_code=200,
        responses={
        200: {"description": "Группа успешно обновлена."},
        400: {"description": "Переданы некорректные данные."},
        404: {"description": "Группа с указанным идентификатором не найдена, либо группа с переданным названием уже существует."},
        }
)
def patch_group(id: int, group: GroupPatch):
    new_group = tm.patch_group(
        id, group.title
    )
    return {
        "message": f"Group ID={new_group[0]} title={new_group[1]}"
    }