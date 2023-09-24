#!/usr/bin/python3

"""
Script that starts a Flask web application with "/" route, "/",
"/c/<text>", "/python/<text>", "/number/<n>", "/number_template/<n>",
"/states_list", "/cities_by_states", "/cities_by_states", "/hbnb_filters" routes defined
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
    states_dict = storage.all(State)
    states = sorted(states_dict.values(), key=lambda state: state.name)
    cities_dict = storage.all(City)
    cities = sorted(cities_dict.values(), key=lambda city: city.name)
    amenity_dict= storage.all(Amenity)
    amenity = sorted(amenity_dict.values(), key=lambda amenity: amenity.name)
    place_dict = storage.all(Place)
    place = sorted(place_dict.values(), key=lambda place: place.name)

    return render_template('100-hbnb.html', states=states, cities=cities, amenity=amenity, place=place)


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
    """ Defines the '/cities_by_states' route"""
    states_dictionary = storage.all(State)
    states = sorted(states_dictionary.values(), key=lambda state: state.name)

    for state in states:
        state.cities = sorted(state.cities, key=lambda city: city.name)
    return render_template('8-cities_by_states.html', states=states)


@app.route("/states", strict_slashes=False)
def states():
    """ Defines the '/states' route"""
    states_dictionary = storage.all(State)
    states = sorted(states_dictionary.values(), key=lambda state: state.name)

    return render_template('9-states.html', states=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """ Defines the '/states/<id>' route"""
    states = storage.all(State).values()
    state = None
    for s in states:
        if s.id == id:
            state = s
            break

    if state is not None:
        state.cities = sorted(state.cities, key=lambda city: city.name)

    return render_template('9-states.html', state=state)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """ Defines the '/hbnb_filters' route"""
    states_dict = storage.all(State)
    states = sorted(states_dict.values(), key=lambda state: state.name)
    cities_dict = storage.all(City)
    cities = sorted(cities_dict.values(), key=lambda city: city.name)
    amenity_dict= storage.all(Amenity)
    amenity = sorted(amenity_dict.values(), key=lambda amenity: amenity.name)
    return render_template('10-hbnb_filters.html', states=states, cities=cities, amenity=amenity)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
