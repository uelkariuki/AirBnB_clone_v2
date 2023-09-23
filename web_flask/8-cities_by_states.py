#!/usr/bin/python3

"""
Script that starts a Flask web application with "/" route, "/",
"/c/<text>", "/python/<text>", "/number/<n>", "/number_template/<n>"
routes, "/states_list", "/cities_by_states" defined
"""


from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
""" Importing Flask, request and other required modules"""


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


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is cool"):
    """ Defines the /python/<text> route"""
    result = "Python %s" % text
    new_result = result.replace("_", " ")
    return new_result


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    """ Defines the '/number/<n>' route"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template_route(n):
    """ Defines the '/number_template/<n>' route"""
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """ Defines the "/number_odd_or_even/<n>" route"""
    return render_template('6-number_odd_or_even.html', n=n)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ method to handle @app.teardown_appcontext """
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """ Defines the '/states_list' route"""
    states_dictionary = storage.all(State)
    states = sorted(states_dictionary.values(), key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    states_dictionary = storage.all(State)
    states = sorted(states_dictionary.values(), key=lambda state: state.name)

    for state in states:
        state.cities = sorted(state.cities, key=lambda city: city.name)
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
