import os
from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")


@app.route("/", methods=["GET"])
def index():

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    return render_template("login.html")

