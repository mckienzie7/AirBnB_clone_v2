#!/usr/bin/python3
"""A storage engine using mysqldb"""
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Class for storage using database"""
    __engine = None
    __session = None

    def __init__(self):
        """Intialize the class for storage"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}"
            .format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB")
            ),
            pool_pre_ping=True
        )

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Show all objects of a class or all objects if cls is None"""
        classes = {
            "State": State,
            "City": City,
            "User": User,
            "Place": Place,
            "Amenity": Amenity,
            "Review": Review
        }

        if cls is not None:
            cls = classes.get(cls)
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for class_ in classes.values():
                objs.extend(self.__session.query(class_).all())

        new_dict = {}
        for obj in objs:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """Add a new object"""
        self.__session.add(obj)

    def save(self):
        """Save a new object"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close method"""
        self.__session.close()
