from contextlib import contextmanager
from collections.abc import Generator
from sqlalchemy.orm import Session, sessionmaker

@contextmanager
def orm_context_manager(session_factory: sessionmaker[Session]) -> Generator[Session, None, None]:
    try:
        session = session_factory()
        yield session
    except:
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close()
