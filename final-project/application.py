from flask import flash, Flask, redirect, render_template, request, url_for
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

    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():

    return render_template("index.html")


@app.route("/entries", methods=["GET", "POST"])
def entries():

    return render_template("entries.html")

