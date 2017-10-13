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

