#!/usr/bin/python3
""""Create a web app to display states as a list"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Get all states in database"""
    states = storage.all("State")
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Close sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
