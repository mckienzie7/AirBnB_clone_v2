#!/usr/bin/python3
""""Create a web app to display states as a list"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Get all states in database"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(exc):
    """Close sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
