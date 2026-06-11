from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="group")

    def __repr__(self):
        return f"Group(ID={self.id}, title={self.title})"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="tasks")
    
    def __repr__(self):
        return f"Task(ID={self.id}, title={self.title}, status={self.status}, group={self.group})"