#!/usr/bin/python3

"""
Script that starts a Flask web application with "/" route, "/",
"/c/<text>", "/python/<text>", "/number/<n>", "/number_template/<n>"
routes defined
"""


from flask import Flask, render_template
""" Importing Flask, request"""


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home_page():
    """ Defines the route "/" """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def alt_home_page():
    """ Defines the route "/hbnb" """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """ Defines the /c/<text> route"""
    result = "C %s" % text
    new_result = result.replace("_", " ")
    return new_result


@app.route("/python/", strict_slashes=True)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is cool"):
    """ Defines the /python/<text> route"""
    result = "Python %s" % text
    new_result = result.replace("_", " ")
    return new_result


@app.route("/number/<int:n>")
def number_route(n):
    """ Defines the '/number/<n>' route"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>")
def inumber_template_route(n):
    """ Defines the '/number_template/<n>' route"""
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
