from sqlalchemy.orm import sessionmaker

from config import create_orm_engine

class ORMManager:
    def __init__(self):
        self._engine = create_orm_engine()
        self._Session = sessionmaker(bind=self._engine)