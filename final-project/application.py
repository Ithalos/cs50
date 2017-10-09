import os
from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")


@app.route("/", methods=["GET"])
def index():

    return render_template("index.html")

