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
