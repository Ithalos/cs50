from bcrypt import gensalt, hashpw
from contextlib import contextmanager
from data.database import Session
from sqlalchemy.orm.exc import NoResultFound

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

    except NoResultFound:
        session.rollback()
        raise

    finally:
        session.close()


def encrypt_password(password):
    """
    Hashes a user password with a random salt using bcrypt,
    and returns the encrypted password.
    """

    return hashpw(password.encode("utf8"), gensalt())


def verify_register_form(args):
    """
    Verify user input for the registry form.
    Checks for the required parameters and their length.
    """

    if not args.get("username") or len(args.get("username")) < 4 \
    or not args.get("password") or len(args.get("password")) < 8 \
    or not args.get("confirmation") or len(args.get("confirmation")) < 8 \
    or args.get("password") != args.get("confirmation"):
        return False

    return True

