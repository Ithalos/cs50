from data.models import Birthday, Memo
from flask import flash, Flask, redirect, render_template, request, session, url_for
from helpers import *
from os import getenv


app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("FLASK_SECRET_KEY")


@app.route("/", methods=["GET"])
def index():
    """
    Display the index page.
    """

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Allow a person to register a user account.
    """

    if request.method == "POST":
        if verify_register_form(request.form):
            if register_user(request.form):
                flash("Registration successful!", "message")
                add_user_to_session(request.form.get("username"))
                return redirect(url_for("index"))

            else:
                flash("User already exists!", "error")
        else:
            flash("Invalid form submission!", "error")

        return redirect(url_for("register"))

    # Request method is GET
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Allow a person to log in with their user account.
    """

    if request.method == "POST":
        if verify_login_form(request.form):
            if verify_user(request.form):
                flash("Logged in!", "message")
                add_user_to_session(request.form.get("username"))
                return redirect(url_for("index"))

            else:
                flash("Username and/or password incorrect!", "error")
        else:
            flash("Invalid form submission!", "error")

        return redirect(url_for("login"))

    # Request method is GET
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    """
    Log the user out.
    """

    session.pop("user_id", None)
    return redirect(url_for("index"))


@app.route("/userprofile", methods=["GET"])
@login_required
def userprofile():
    """
    Display a user's profile page.
    """

    return render_template("userprofile.html", username=get_username_from_id())


@app.route("/change_password", methods=["POST"])
@login_required
def change_password():
    """
    Allow a user to change their password.
    """

    if verify_change_password_form(request.form):
        if change_user_password(request.form):
            flash("Successfully changed password!", "message")

        else:
            flash("Failed to change password!", "error")
    else:
        flash("Incorrect form submission!", "error")

    return redirect(url_for("userprofile"))


@app.route("/remove_account", methods=["POST"])
@login_required
def remove_account():
    """
    Delete a user's account from the database.
    """

    if request.form.get("remove") is not None:
        remove_user_by_id(session.get("user_id"))

    flash("Account removed successfully!", "message")
    return redirect(url_for("logout"))


@app.route("/memos", methods=["GET"])
@login_required
def memos():
    """
    Display the memos page, where users can view, create and remove memos.
    """

    user_id = session.get("user_id")
    with db_session_scope() as db_session:
        memos = db_session.query(Memo).filter(Memo.user_id == user_id).all()
        return render_template("memos.html", memos=memos)


@app.route("/create_memo", methods=["POST"])
@login_required
def create_memo():
    """
    Create a new memo.
    """

    memo_text = request.form.get("memo_text")

    if memo_text and memo_text != "":
        create_new_memo(memo_text)
        flash("New memo created!", "message")
    else:
        flash("You cannot create an empty memo!", "error")

    return redirect(url_for("memos"))


@app.route("/remove_memo", methods=["POST"])
@login_required
def remove_memo():
    """
    Remove a memo.
    """

    remove_memo_by_id(request.form.get("memo_id"))
    return redirect(url_for("memos"))


@app.route("/tasks", methods=["GET"])
@login_required
def tasks():
    """
    Display the tasks page, where users can view, create and remove tasks.
    """

    user_id = session.get("user_id")
    with db_session_scope() as db_session:
        tasks = db_session.query(Task).filter(Task.user_id == user_id).order_by(Task.date).all()
        return render_template("tasks.html", tasks=tasks)


@app.route("/create_task", methods=["POST"])
@login_required
def create_task():
    """
    Create a new task.
    """

    if verify_create_task_form(request.form):
        if create_new_task(request.form):
            flash("New task created!", "message")

        else:
            flash("Could not create task!", "error")
    else:
        flash("Incorrect form submission!", "error")

    return redirect(url_for("tasks"))


@app.route("/remove_task", methods=["POST"])
@login_required
def remove_task():
    """
    Remove a task.
    """

    remove_task_by_id(request.form.get("task_id"))
    return redirect(url_for("tasks"))


@app.route("/birthdays", methods=["GET"])
@login_required
def birthdays():
    """
    Display the birthdays page, where users can view, create and remove birthdays.
    """

    user_id = session.get("user_id")
    with db_session_scope() as db_session:
        birthdays = db_session.query(Birthday).filter(Birthday.user_id == user_id).order_by(Birthday.date).all()
        return render_template("birthdays.html", birthdays=birthdays)


@app.route("/create_birthday", methods=["POST"])
@login_required
def create_birthday():

    if verify_create_birthday_form(request.form):
        if create_new_birthday(request.form):
            flash("New birthday created!", "message")

        else:
            flash("Could not create birthday!", "error")
    else:
        flash("Incorrect form submission!", "error")

    return redirect(url_for("birthdays"))


@app.route("/remove_birthday", methods=["POST"])
@login_required
def remove_birthday():

    remove_birthday_by_id(request.form.get("birthday_id"))
    return redirect(url_for("birthdays"))

