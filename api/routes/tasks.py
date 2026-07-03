from fastapi import APIRouter

from api.dependencies import tm

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
def get_tasks():
    return tm.list_tasks(
        sort_type="id",
        filtered=True,
        status="active",
        group=""
    )
