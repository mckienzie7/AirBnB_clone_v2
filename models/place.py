#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity
from os import getenv
import models

association_table = Table('place_amenity', Base.metadata,
    Column('place_id', ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """A relationship between review and place"""
            reviews_list = []
            all_reviews = models.storage.all(Review)
            for value in all_reviews.values():
                if value.place_id == self.id:
                    reviews_list.append(value)
            return reviews_list

        @property
        def amenities(self):
            amenities_list = []
            all_amenities = models.storage.all(Review)
            for value in all_amenities.values():
                if value.place_id in self.amenity_ids:
                    amenities_list.append(value)
            return amenities_list

        @amenities.setter
        def amenities(self, amenity):
            if type(amenity) == Amenity:
                self.amenity_ids.append(amenity.id)
