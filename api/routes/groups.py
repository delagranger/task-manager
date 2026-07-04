from fastapi import APIRouter

from api.dependencies import tm
from api.schemas.group import GroupCreate, GroupPatch

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/")
def get_groups(sort_type: str = "id"):
    return tm.list_groups(sort_type)


@router.post("/")
def post_group(group: GroupCreate):
    return tm.add_group(group.title)


@router.delete("/{id}")
def delete_group(id: int):
    tm.delete_group(id)
    return {
        "message" : f"Group with id={id} deleted!"
    }


@router.patch("/{id}")
def patch_group(group_id: int,group: GroupPatch):
    return tm.patch_group(group_id, group.title)