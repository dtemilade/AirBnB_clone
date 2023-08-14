#!/usr/bin/python3

import cmd
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from models import storage
from models.user import User

# declaring class definition
class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    __classes = ["BaseModel", "User", "State", "City", "Place", "Review",
            "Amenity"]

    def do_EOF(self, line):
        """for EOF function\n"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program\n"""
        return True

    def emptyline(self):
        return

    def do_create(self, arg):
        """ function to creates a new instance of BaseModel\n"""
        args = arg.split()
        if len(args) == 0:
            # class name missing
            print("** class name missing **")
        elif args[0] not in self.__classes:
            # class name doesn’t exist
            print("** class doesn't exist **")
        else:
            # new instance created with id
            new_obj = eval(f"{args[0]}()")
            print(new_obj.id)
            storage.save()

    def do_show(self, arg):
        """function to print an instance based on the class name and id\n"""
        args = arg.split()
        if len(args) == 0:
            # class name missing
            print("** class name missing **")
        elif args[0] not in self.__classes:
            # class name doesn’t exist
            print("** class doesn't exist **")
        elif len(args) == 1:
            # the id is missing
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[f"{args[0]}.{args[1]}"])

    def do_destroy(self, arg):
        """function to delete an instance based on the class name and id\n"""
        args = arg.split()
        if len(args) == 0:
            # class name missing
            print("** class name missing **")
        elif args[0] not in self.__classes:
            # class name doesn’t exist
            print("** class doesn't exist **")
        elif len(args) == 1:
            # the id is missing
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("no instance found")
        else:
            del storage.all()[f"{args[0]}.{args[1]}"]
            storage.save()

    def do_all(self, arg):
        args = arg.split()
        if len(args) == 0:
            print([str(value) for value in storage.all().values()])
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        else:
            print([str(v) for k, v in storage.all().items() if
                k.startswith(args[0])])

    def do_update(self, arg):
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            obj_class = args[0]
            obj_id = args[1]
            obj_key = obj_class + "." + obj_id
            obj = storage.all()[obj_key]
            attr_name = args[2]
            attr_value = args[3]
            # strip if start with double_quote
            if attr_value[0] == '"':
                attr_value = attr_value[1:-1]

            if hasattr(obj, attr_name):
                obj_type = type(getattr(obj, attr_name))
                if obj_type in [str, float, int]:
                    attr_value = obj_type(attr_value)
                    setattr(obj, attr_name, attr_value)
                else:
                    setattr(obj, attr_name, attr_value)
                storage.save()

    # updates on console sets to default.
    def default(self, arg):
        args = arg.split()
        """Conditional statement for output"""
        if args[0] in self.__classes:
            # for retrieve all instances of a class
            if args[1] == "all()":
                self.do_all(args[0])
            # for retrieve the number of instances of a class
            elif args[1] == "count()":
                val_count = [v for k, v in storage.all().items() if
                        k.startswith(args[0])]
                print(len(val_count))
            # retrieve an instance based on its ID:
            elif args[1].startswith("show"):
                val_id = args[1].split('"')[1]
                self.do_show(f"{args[0]} {val_id}")
            # to destroy an instance based on his ID: 
            elif args[1].startswith("destroy"):
                val_id = args[1].split('"')[1]
                self.do_destroy(f"{args[0]} {val_id}")
            #  to update an instance based on his ID:
            elif args[1].startswith("update"):
                split_case = args[1].split('(')
                split_case = split_case[1].split(')')
                split_case = split_case[0].split(', ')
                val_id = split_case[0].strip('"')
                attr_name = split_case[1].strip('"')
                attr_value = split_case[2].strip('"')
                self.do_update(f"{args[0]} {val_id} {attr_name} {attr_value}")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
