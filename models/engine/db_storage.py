#!/usr/bin/python3

"""
Creation of the New engine DBStorage
"""

from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, MetaData, text
from os import getenv

from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """ Class DBStorage for the new engine DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """ Public instance method"""

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)

        self.__session = scoped_session(Session)

        user = getenv("HBNB_MYSQL_USER")
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(f"mysql+mysqldb://{user}:\
{password}@{host}/{database}", pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session (self.__session)
        all objects depending of the class name (argument cls)
        """

        result = {}
        if cls:
            objects_query = self.__session.query(cls)

            for obj in objects_query.all():
                key = f'{obj.__class__.__name__}.{obj.id}'
                result[key] = obj

        else:
            classes = ['User', 'State', 'City', 'Amenity', 'Place', 'Review']
            for Class in classes:
                objects_query = self.__session.query(Class)
                for obj in objects_query.all():
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    result[key] = obj
        return result

    def new(self, obj):
        """
        add the object to the current database session (self.__session)
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes of the current database session (self.__session)
        """

        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session obj if not None
        """

        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database(feature of SQLAlchemy)
        (WARNING: all classes who inherit from Base must be
        imported before calling
        Base.metadata.create_all(engine))
        """

        Base.metadata.create_all(self.__engine)

        Session_make = sessionmaker(bind=self.__engine, expire_on_commit=False)

        Session = scoped_session(Session_make)
        self.__session = Session()

    def close(self):
        """ method to close the SQLALchemy session"""
        self.__session.close()
