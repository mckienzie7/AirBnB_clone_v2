#!/usr/bin/python3
""""Create a web app to display states as a list"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """Get all states in database"""
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Get all states in database"""
    states = storage.all("State").values()
    for state in states:
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(exc):
    """Close sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
