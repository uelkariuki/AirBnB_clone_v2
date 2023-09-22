#!/usr/bin/python3

"""
Script that starts a Flask web application with "/" route and "/"
routes defined
"""


from flask import Flask
""" Importing Flask """


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home_page():
    """ Defines the route "/" """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def alt_home_page():
    """ Defines the route "/hbnb" """
    return "HBNB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
