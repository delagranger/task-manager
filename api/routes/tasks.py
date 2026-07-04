from fastapi import APIRouter

from api.dependencies import tm

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
def get_tasks(
    sort_type: str = "id",
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

@router.post("/add")
def post_task(
        title: str,
        status: str,
        group: str
):
    task = tm.add_task(
        title=title,
        status=status,
        group=group
    )
    return f"Task id={task[0]} title={task[1]} is posted!"