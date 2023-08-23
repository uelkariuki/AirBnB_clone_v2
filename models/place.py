#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship


 # many to many relationship
place_amenity = Table('place_amenity', Base.metadata,
        Column("place_id", String(60), ForeignKey('places.id'), primary_key=True),
        Column("amenity_id", String(60), ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    # for DBStorage

    reviews = relationship("Review", backref="place", cascade="all, delete-orphan")

    @property
    def reviews(self):
        """
        getter attribute cities that returns the list of City
        instances with state_id equals to the current State.id
        """

        from models import storage

        # get all the cities in a dictionary
        total_reviews = storage.all(Review)
        review_result = []
        for review in total_reviews.values():
            if review.place_id == self.id:
                review_result.append(review)
        return review_result

    # for DBStorage
    amenities = relationship('Amenity', secondary=place_amenity, viewonly=False)

    # for FileStorage

    @property
    def amenities(self):
        """
        Getter attribute amenities that returns the list of
        Amenity instances based on the attribute amenity_ids
        that contains all Amenity.id linked to the Place
        """
        from models import storage
        amenity_result = []

        for id_amenity in self.amenity_ids:
            key = "Amenity." + id_amenity
            if key in storage.all():
                amenity_result.append(storage.all()[key])
            return amenity_result

    @amenities.setter
    def amenities(self, Amenity_obj):
        """
        Setter attribute amenities that handles append method
        for adding an Amenity.id to the attribute amenity_ids.
        This method should accept only Amenity object,
        otherwise, do nothing.
        """
        from models import Amenity

        if isinstance(Amenity_obj, Amenity):
            self.amenity_ids.append(Amenity_obj.id)
