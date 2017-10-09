from bcrypt import gensalt, hashpw
from contextlib import contextmanager
from data.database import Session

@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.

    http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    """

    session = Session()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def encrypt_password(password):
    """
    Hashes a user password with a random salt using bcrypt,
    and returns the encrypted password.
    """

    return hashpw(password.encode("utf8"), gensalt())

