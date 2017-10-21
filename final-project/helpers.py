from bcrypt import checkpw, gensalt, hashpw
from contextlib import contextmanager
from data.database import Session
from data.models import Birthday, Memo, Task, User
from datetime import datetime, date
from flask import request, redirect, session, url_for
from functools import wraps
from sqlalchemy.orm.exc import NoResultFound


def login_required(f):
    """
    Require the user to be logged in to access a route.

    http://flask.pocoo.org/docs/latest/patterns/viewdecorators
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@contextmanager
def db_session_scope():
    """
    Provide a transactional scope around a series of operations.

    http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    """

    db_session = Session()

    try:
        yield db_session
        db_session.commit()

    except:
        db_session.rollback()
        raise

    finally:
        db_session.close()


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

    with db_session_scope() as db_session:
        db_session.add(user)
        return True


def user_exists(username):
    """
    Check if user exists in the database, and returns a boolean.
    """

    with db_session_scope() as db_session:
        try:
            db_session.query(User).filter(User.username == username).one()
            return True
        except NoResultFound:
            return False


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

    with db_session_scope() as db_session:
        user = db_session.query(User).filter(User.username == username).one()
        return checkpw(password, user.password)


def get_user_id_from_username(username):
    """
    Look up a user by their username, and if it exists, return
    their id, else None.
    """

    with db_session_scope() as db_session:
        try:
            return db_session.query(User.id).filter(User.username == username).scalar()
        except NoResultFound:
            return None


def add_user_to_session(username):
    """
    Adds a user's id to the session by looking up their username.
    """

    user_id = get_user_id_from_username(username)
    session["user_id"] = user_id


def create_new_memo(text):
    """
    Create a new memo in the database.
    """

    user_id = session.get("user_id")

    with db_session_scope() as db_session:
        user = db_session.query(User).filter(User.id == user_id).one()
        user.memos += [Memo(text=text)]
        db_session.add(user)


def remove_memo_by_id(memo_id):
    """
    Remove a memo from the database by looking up its id.
    """

    with db_session_scope() as db_session:
        db_session.query(Memo).filter(Memo.id == memo_id).delete()


def remove_task_by_id(task_id):
    """
    Remove a task from the database by looking up its id.
    """

    with db_session_scope() as db_session:
        db_session.query(Task).filter(Task.id == task_id).delete()


def remove_birthday_by_id(birthday_id):
    """
    Remove a birthday from the database by looking up its id.
    """

    with db_session_scope() as db_session:
        db_session.query(Birthday).filter(Birthday.id == birthday_id).delete()


def remove_user_by_id(user_id):
    """
    Delete a user from the database, including all relational elements.
    """

    with db_session_scope() as db_session:
        user = db_session.query(User).filter(User.id == user_id).one()
        db_session.delete(user)


def change_user_password(args):
    """
    Allows a user to change their password.
    """

    user_id = session.get("user_id")
    old_password = args.get("oldpassword").encode("utf8")
    new_password = args.get("confirmation")

    with db_session_scope() as db_session:
        user = db_session.query(User).filter(User.id == user_id).one()
        if checkpw(old_password, user.password):
            user.password = encrypt_password(new_password)
            db_session.add(user)
            return True

        return False


def verify_change_password_form(args):
    """
    Verify user input for the change password form.
    """

    if not args.get("oldpassword") or not args.get("newpassword") \
    or not args.get("confirmation"):
        return False

    if len(args.get("newpassword")) < 8 or len(args.get("confirmation")) < 8 \
    or args.get("newpassword") != args.get("confirmation"):
        return False

    return True


def verify_create_task_form(args):
    """
    Verify user input when creating a new task.
    """

    if not args.get("task_date") or not args.get("task_text"):
        return False

    date = convert_date_to_object(args.get("task_date"))
    if date is None:
        return False

    if args.get("task_text") == "":
        return False

    return True


def create_new_task(args):
    """
    Create a new task in the database.
    """

    user_id = session.get("user_id")
    date = convert_date_to_object(args.get("task_date"))
    text = args.get("task_text")

    with db_session_scope() as db_session:
        user = db_session.query(User).filter(User.id == user_id).one()
        user.tasks += [Task(date=date, text=text)]
        db_session.add(user)

    return True


def verify_create_birthday_form(args):
    """
    Verify user input when creating a new birthday.
    """

    if not args.get("birthday_date") or not args.get("birthday_person"):
        return False

    date = convert_date_to_object(args.get("birthday_date"))
    if date is None:
        return False

    if args.get("birthday_person") == "":
        return False

    return True


def create_new_birthday(args):
    """
    Create a new birthday in the database.
    """

    user_id = session.get("user_id")
    date = convert_date_to_object(args.get("birthday_date"))
    person = args.get("birthday_person")

    with db_session_scope() as db_session:
        user = db_session.query(User).filter(User.id == user_id).one()
        user.birthdays += [Birthday(date=date, person=person)]
        db_session.add(user)

    return True


def convert_date_to_object(datestring):
    """
    Converts a date string to a python date object.
    If the conversion fails, the function will return None.

    String must be formatted as YYYY-MM-DD.
    """

    try:
        return datetime.strptime(datestring, "%Y-%m-%d").date()
    except ValueError:
        return None

