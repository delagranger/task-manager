from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    status: str
    group: str


class TaskPatch(BaseModel):
    title: str | None = None
    status: str | None = None
    group: str | None = None