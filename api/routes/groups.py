from fastapi import APIRouter

from api.dependencies import tm

router = APIRouter(prefix="/groups", tags=["groups"])

@router.get("/")
def get_groups(
    sort_type: str = "id"
):
    return tm.list_groups(
        sort_type
    )
