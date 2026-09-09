from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:
    from .task_model import TaskModel

class GroupModel(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    user: Mapped[str] = relationship(back_populates="groups")
    tasks: Mapped[list[TaskModel]] = relationship(back_populates="group", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Group(ID={self.id}, title={self.title})"
