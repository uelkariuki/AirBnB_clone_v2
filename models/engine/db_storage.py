#!/usr/bin/python3

"""
Creation of the New engine DBStorage
"""

from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, MetaData, text
import os

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

        user = os.environ.get("HBNB_MYSQL_USER")
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST')
        database = os.environ.get('HBNB_MYSQL_DB')

        self.__engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}/{database}", pool_pre_ping=True)

        if os.environ.get("HBNB_ENV") == "test":
            metadata = MetaData(bind=self.__engine)
            metadata.drop_all()

    def all(self, cls=None):
        """
        query on the current database session (self.__session)
        all objects depending of the class name (argument cls)
        """

        # self.__session = sessionmaker(bind=self.__engine)
        # session = self.__session()

        from console import HBNBCommand
        result = {}
        if cls is None:
            classes = [User, State, City, Amenity, Place, Review]

            session = self.__session()

            for Class in classes:
                objects = session.query(Class).all()
                print("Objects:", objects)
                for obj in objects:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    result[key] = obj

        else:
            class_ref = HBNBCommand.classes.get(cls)
            if class_ref:
                objects = self.__session.query(class_ref).all()

                for obj in objects:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    result[key] = obj

        return result

    def new(self, obj):
        """
        add the object to the current database session (self.__session)
        """
        self.__session = sessionmaker(bind=self.__engine)
        session = self.__session()

        session.add(obj)

    def save(self):
        """
        commit all changes of the current database session (self.__session)
        """

        self.__session = sessionmaker(bind=self.__engine)
        session = self.__session()

        session.commit()


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

        from models.city import City
        from models.state import State

        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)

        self.__session = scoped_session(Session)
