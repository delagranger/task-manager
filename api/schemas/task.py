from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str = "default task"
    status: str = "active"
    group: str = "default group"


class TaskPatch(BaseModel):
    title: str | None = None
    status: str | None = None
    group: str | None = None