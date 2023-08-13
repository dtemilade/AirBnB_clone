#!/usr/bin/python3
# Recreation of a BaseModel from another one with a dictionary representation.

from models.base_model import BaseModel
import json
from models.user import User

class FileStorage():
    # Declare Private class attributes
    __file_path = "file.json"
    __objects = {}

    # Declare Public instance methods
    def all(self):
        return self.__objects

    def new(self, obj):
        # initialize key with f-string
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        # open file to write and serialize
        with open(self.__file_path, "w", encoding="utf-8") as f:
            dict_s = {k : v.to_dict() for k, v in self.__objects.items()}
            json.dump(dict_s, f)

    def reload(self):
        try:
            # open file to read and deserialize
            with open(self.__file_path, "r", encoding="utf-8") as f:
                obj_dict = json.load(f)
                for dict_r in obj_dict.values():
                    cls_name = dict_r["__class__"]
                    del dict_r["__class__"]
                    self.new(eval(f"{cls_name}")(**dict_r))

        except FileNotFoundError:
            return
