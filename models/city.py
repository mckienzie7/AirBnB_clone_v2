#!/usr/bin/python3
"""Defines the City class"""
from models.base_model import BaseModel, Base
from models.place import Place
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Class City"""
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    places = relationship("Place",  backref="cities", cascade="delete")
