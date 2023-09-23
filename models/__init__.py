#!/usr/bin/python3
"""
This module instantiates an object of class FileStorage and
class DBStorage depending of the value of the environment
variable HBNB_TYPE_STORAGE:
"""

import os

env_storage_type = os.getenv("HBNB_TYPE_STORAGE")
if env_storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
