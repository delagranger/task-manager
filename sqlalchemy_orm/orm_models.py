from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass


class GroupORM(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    tasks: Mapped[list["TaskORM"]] = relationship(back_populates="group", passive_deletes=True)

    def __repr__(self):
        return f"Group(ID={self.id}, title={self.title})"


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(), nullable=False)
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id", ondelete="SET NULL"), nullable=True)
    group: Mapped["GroupORM"] = relationship(back_populates="tasks")
    
    def __repr__(self):
        return f"Task(ID={self.id}, title={self.title}, status={self.status}, group={self.group})"