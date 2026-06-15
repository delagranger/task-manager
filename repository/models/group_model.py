from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from repository.models.base import Base

class GroupORM(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    tasks: Mapped[list["TaskORM"]] = relationship(back_populates="group", passive_deletes=True)

    def __repr__(self):
        return f"Group(ID={self.id}, title={self.title})"
