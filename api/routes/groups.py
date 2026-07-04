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

@router.post("/add")
def post_group(
    title: str
):
    group = tm.add_group(
        title=title
    )
    return f"Group id={group[0]} title={group[1]} is posted!"
