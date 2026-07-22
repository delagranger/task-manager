from fastapi import APIRouter

from api.dependencies import tm
from api.schemas.task import TaskCreate, TaskPatch

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
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
 

@router.post("/")
def post_task(task: TaskCreate):
    return tm.add_task(
        title=task.title,
        status=task.status,
        group=task.group
    )


@router.delete("/{id}")
def delete_task(id: int):
    tm.delete_task(id)
    return {
        "message" : f"Task with id={id} deleted!"
    }


@router.patch("/{id}")
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