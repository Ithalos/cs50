from contextlib import contextmanager
from data.database import Session

@contextmanager
def session_scope():

    session = Session()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

