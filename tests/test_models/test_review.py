#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.review import Review
import os
from os import getenv

class test_review(test_basemodel):
    """ test review class"""

    def __init__(self, *args, **kwargs):
        """ initialization"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """ testing the place id"""
        new = self.value()
        self.assertEqual(type(new.place_id), str if 
                        os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.text), str
                         if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))
