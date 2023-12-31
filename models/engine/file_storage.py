#!/usr/bin/python3
"""File storage for instances of a class created"""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Class created"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of instantiated objects in __objects.

        If a cls is specified, returns a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        if cls is not None:
            cls_dict = {}
            for key, value in self.__objects.items():
                cls_nm = key.split(".")
                if eval(cls_nm[0]) == cls:
                    cls_dict[key] = value
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Add a new instance of a class to _-objects"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """serialization"""
        obj_dict = {}
        for key, obj in self.__objects.items():
            obj_dict[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """from json string to python objects"""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                dicti = json.load(file)
            for val in dicti.values():
                clsnm = eval(val["__class__"])
                obj = clsnm(**val)
                self.new(obj)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists."""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """Close"""
        self.reload()
