from fastapi import APIRouter

from api.dependencies import tm
from api.schemas.task import TaskCreate, TaskPatch

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
        "/",
        summary="Получить список всех задач",
        description="Возвращает список всех задач, отсортированных и отфильтрованных по опциональным параметрам",
        status_code=200,
        responses={
            200: {"description": "Список задач успешно получен."},
            400: {"description": "Некорректные параметры сортировки или фильтрации."},
            404: {"description": "Указанная группа не найдена."}
        }
)
def get_tasks(sort_type: str = "id",
              filtered: bool = False,
              status: str = "",
              group: str = ""
              ):
    return tm.list_tasks(
        sort_type,
        filtered,
        status,
        group
    )


@router.post(
        "/",
        summary="Создать новую задачу",
        description=(
        "Создает новую задачу и сохраняет ее в базе данных. "
        "Перед созданием проверяются корректность статуса, длина названия "
        "и существование указанной группы."
        ),
        status_code=201,
        responses={
        201: {"description": "Задача успешно создана."},
        400: {"description": "Некорректные данные задачи."},
        404: {"description": "Указанная группа не существует."},
        }
)
def post_task(task: TaskCreate):
    return tm.add_task(
        title=task.title,
        status=task.status,
        group=task.group
    )


@router.delete(
        "/{id}",
        summary="Удалить задачу",
        description=(
        "Удаляет задачу по ее идентификатору."
        ),
        status_code=200,
        responses={
        200: {"description": "Задача успешно удалена."},
        404: {"description": "Задача с указанным идентификатором не найдена."},
        }
)
def delete_task(id: int):
    tm.delete_task(id)
    return {
        "message" : f"Task with id={id} deleted!"
    }


@router.patch(
        "/{id}",
        summary="Изменить задачу",
        description=(
        "Частично обновляет данные существующей задачи. "
        "Можно изменить название, статус и группу. "
        "Перед сохранением изменений выполняется валидация переданных значений."
        ),
        status_code=200,
        responses={
        200: {"description": "Задача успешно обновлена."},
        400: {"description": "Переданы некорректные данные."},
        404: {"description": "Задача или указанная группа не найдены."},
        }
)
def patch_task(id: int, task: TaskPatch):
    new_task = tm.patch_task(
        id=id,
        title=task.title,
        status=task.status,
        group=task.group
    )
    return {
        "message": f"Task ID={new_task[0]} title={new_task[1]}, status={new_task[2]}, group={new_task[3]}"
    }