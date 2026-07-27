from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(
        default="default task",
        description="Название задачи",
        examples=["Купить молока"]
    )
    status: str = Field(
        default="active",
        description="Статус задачи",
        examples=["active"]
    )
    group: str = Field(
        default="default group",
        description="Название группы, к которой относится задача",
        examples=["Задачи по работе"]
    )


class TaskPatch(BaseModel):
    title: str | None = Field(
        default=None,
        description="Новое название задачи"
    )
    status: str | None = Field(
        default=None,
        description="Новый статус задачи"
    )
    group: str | None = Field(
        default=None,
        description="Новая группа задачи"
    )