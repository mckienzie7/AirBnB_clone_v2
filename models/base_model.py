#!/usr/bin/python3
"""Base class for other classes"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import models
import uuid

Base = declarative_base()


class BaseModel:
    """The Base class"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """initializing class"""
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def __str__(self):
        """string representation of instance of the class"""
        return "[{}] ({}) {}"\
               .format(self.__class__.__name__, self.id, self.__dict__)


    def to_dict(self):
        """create dictionary"""
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in obj_dict.keys():
            del obj_dict["_sa_instance_state"]
        return obj_dict

    def delete(self):
        """Deleting an item."""
        models.storage.delete(self)
