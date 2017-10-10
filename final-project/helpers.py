from bcrypt import checkpw, gensalt, hashpw
from contextlib import contextmanager
from data.database import Session
from data.models import User
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


def register_user(args):
    """
    Register a user in the database.
    """

    # Check if user exists first to prevent unneeded calculations
    username = args.get("username")
    if user_exists(username):
        return False

    password = encrypt_password(args.get("password"))
    user = User(username=username, password=password)

    with session_scope() as session:
        session.add(user)
        return True


def user_exists(username):
    """
    Check if user exists in the database, and returns a boolean.
    """

    with session_scope() as session:
        count = session.query(User).filter(User.username == username).count()
        if count == 1:
            return True
        elif count == 0:
            return False
        else:
            raise Exception("Multiple users with same name found!")


def verify_login_form(args):
    """
    Verify user input for the login form.
    Checks for the required parameters and their length.
    """

    if not args.get("username") or len(args.get("username")) < 4 \
    or not args.get("password") or len(args.get("password")) < 8:
        return False

    return True


def verify_user(args):
    """
    Check the given username and password against the database.
    """

    username = args.get("username")
    if not user_exists(username):
        return False

    password = args.get("password").encode("utf8")

    with session_scope() as session:
        user = session.query(User).filter(User.username == username).one()
        return checkpw(password, user.password)

