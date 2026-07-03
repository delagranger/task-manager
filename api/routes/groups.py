from fastapi import APIRouter

from api.dependencies import tm

router = APIRouter(prefix="/groups", tags=["groups"])

@router.get("/")
def get_groups():
    return tm.list_groups(
        sort_type="id"
    )
