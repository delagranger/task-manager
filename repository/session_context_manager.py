from contextlib import contextmanager
from collections.abc import Generator
from sqlalchemy.orm import Session, sessionmaker
import logging

log = logging.getLogger(__name__)

@contextmanager
def session_scope(session_factory: sessionmaker, operation: str) -> Generator[Session, None, None]:
    session = session_factory()
    try:
        yield session
    except Exception:
        session.rollback()
        log.exception("%s: FAILED", operation)
        raise
    else:
        session.commit()
    finally:
        session.close()
