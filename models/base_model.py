#!/usr/bin/python3
# BaseModel that defines all common attributes/methods for other classes:

import models
import uuid
from datetime import datetime

class BaseModel():

    """Declaring Public instance attributes:"""
    def __init__(self, *args, **kwargs):

        # if kwargs is not empty by using len() function.
        if len(kwargs) != 0:
            # pass kwargs for checking
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.fromisoformat(value)
                else:
                    self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    """
    For output into a string every instance of the class
    in respect to the format using f-string for return.
    """
    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    # Declaring Public instance methods
    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()

    # Manipulating dict method with return of the copy of a dictionary
    def to_dict(self):
        cpy_dict = self.__dict__.copy()
        cpy_dict['__class__'] = self.__class__.__name__
        cpy_dict['created_at'] = cpy_dict['created_at'].isoformat()
        cpy_dict['updated_at'] = cpy_dict['updated_at'].isoformat()
        return cpy_dict
