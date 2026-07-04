from pydantic import BaseModel


class GroupCreate(BaseModel):
    title: str


class GroupPatch(BaseModel):
    title: str | None = None