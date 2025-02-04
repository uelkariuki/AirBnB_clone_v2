#!/usr/bin/python3
""" State Module for HBNB project """

import models
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from os import getenv


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    # for DBStorage
    cities = relationship("City", backref="state",
                          cascade="all, delete-orphan")

    # for FileStorage

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            getter attribute cities that returns the list of City
            instances with state_id equals to the current State.id
            """

            from models import storage

        # get all the cities in a dictionary
            total_cities = storage.all(City)

            city_result = []
            for city in total_cities.values():
                if city.state_id == self.id:
                    city_result.append(city)
            return city_result
