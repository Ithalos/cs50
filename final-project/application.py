from flask import Flask, render_template, session
from helpers import *
from os import getenv

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("FLASK_SECRET_KEY")


@app.route("/", methods=["GET"])
def index():

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

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

