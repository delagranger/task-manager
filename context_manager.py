from contextlib import contextmanager

@contextmanager
def orm_context_manager(Session):
    try:
        session = Session()
        yield session
    except:
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close()
