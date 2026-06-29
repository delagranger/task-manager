from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from repository.models.base import Base

if TYPE_CHECKING:
    from repository.models.task_model import TaskModel

class GroupModel(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    tasks: Mapped[list[TaskModel]] = relationship(back_populates="group", passive_deletes=True)

    def __repr__(self) -> str:
        return f"Group(ID={self.id}, title={self.title})"
