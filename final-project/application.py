from data.models import Memo
from flask import flash, Flask, redirect, render_template, request, session, url_for
from helpers import *
from os import getenv


app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("FLASK_SECRET_KEY")


@app.route("/", methods=["GET"])
def index():

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        if verify_register_form(request.form):
            if register_user(request.form):
                flash("Registration successful!", "message")
                add_user_to_session(request.form.get("username"))
                return redirect(url_for("entries"))

            else:
                flash("User already exists!", "error")
        else:
            flash("Invalid form submission!", "error")

        return redirect(url_for("register"))

    # Request method is GET
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        if verify_login_form(request.form):
            if verify_user(request.form):
                flash("Logged in!", "message")
                add_user_to_session(request.form.get("username"))
                return redirect(url_for("entries"))

            else:
                flash("Username and/or password incorrect!", "error")
        else:
            flash("Invalid form submission!", "error")

        return redirect(url_for("login"))

    # Request method is GET
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():

    session.pop("user_id", None)
    return redirect(url_for("index"))


@app.route("/memos", methods=["GET"])
@login_required
def memos():

    user_id = session.get("user_id")
    with db_session_scope() as db_session:
        memos = db_session.query(Memo).filter(Memo.user_id == user_id).all()
        return render_template("memos.html", memos=memos)


@app.route("/create_memo", methods=["POST"])
@login_required
def create_memo():

    memo_text = request.form.get("memo_text")

    if memo_text != "":
        create_new_memo(memo_text)
    else:
        flash("You cannot create an empty memo!", "error")

    return redirect(url_for("memos"))


@app.route("/remove_memo", methods=["POST"])
@login_required
def remove_memo():

    remove_memo_by_id(request.form.get("memo_id"))
    return redirect(url_for("memos"))

