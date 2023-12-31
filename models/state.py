#!/usr/bin/python3
"""Defines the State class"""
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """Class state created"""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City",  backref="state", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """A relationship between state and city"""
            city_list = []
            all_cities = models.storage.all(City)
            for value in all_cities.values():
                if value.state_id == self.id:
                    city_list.append(value)
            return city_list
