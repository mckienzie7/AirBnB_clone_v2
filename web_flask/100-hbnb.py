#!/usr/bin/python3
""""Create a web app to display states as a list"""
from models import storage
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Get all states in database"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    return render_template("100-hbnb.html", states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exc):
    """Close sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug="True")
