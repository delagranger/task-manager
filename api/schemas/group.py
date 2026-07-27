from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    title: str = Field(
        default=None,
        description="Название новой группы",
        examples=["Задачи по работе"]
    )


class GroupPatch(BaseModel):
    title: str | None = Field(
        default=None,
        description="Новое название группы",
        examples=["Задачи по работе"]
    )