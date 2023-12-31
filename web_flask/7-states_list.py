#!/usr/bin/python3
""""Create a web app to display states as a list"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Get all states in database"""
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Close sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
