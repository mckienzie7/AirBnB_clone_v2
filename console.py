#!/usr/bin/python3
"""creating a console"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """console class"""
    prompt = "(hbnb) "
    __classes = {"BaseModel": BaseModel,
                 "User": User, "Place": Place, "State": State,
                 "City": City, "Amenity": Amenity, "Review": Review}

    def do_quit(self, line):
        """type quit to exit the console"""
        return True

    def do_EOF(self, line):
        """press ctr - d to exit"""
        return True

    def emptyline(self):
        """command for an empty line."""
        pass

    def do_create(self, line):
        """command to create a new class. Type name of class to ccreate"""
        entry = line.split(" ")
        if len(line) == 0:
            print("** class name missing **")
        elif entry[0] not in self.__classes.keys():
            print("** class doesn't exist **")
        else:
            new_dict = {}
            lis1 = entry[1:]
            for item in lis1:
                if "=" in item:
                    lis2 = item.split("=")
                    key = lis2[0]
                    value = lis2[1]
                    if value[0] == '"':
                        value = value.replace('"', '').replace("_", " ")
                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            try:
                                value = float(value)
                            except ValueError:
                                continue
                    new_dict[key] = value
            print(new_dict)
            new_instance = self.__classes[entry[0]](**new_dict)
            new_instance.save()
            print(new_instance.id)

    def do_show(self, line):
        """show a string representation ofobject based on class and id"""
        info = storage.all()
        entry = line.split(" ")
        if len(entry) == 0:
            printentry = line.split(" ")
        if len(line) == 0:
            print("** class name missing **")
        elif entry[0] not in self.__classes.keys():
            print("** class doesn't exist **")
        elif len(entry) < 2:
            print("** instance id missing **")
        elif "{}.{}".format(entry[0], entry[1]) not in info.keys():
            print("** no instance found **")
        else:
            instance = info["{}.{}".format(entry[0], entry[1])]
            print(instance)

    def do_destroy(self, line):
        """to destroy an object of the given id"""
        info = storage.all()
        entry = line.split(" ")
        if len(line) == 0:
            print("** class name missing **")
        elif entry[0] not in self.__classes.keys():
            print("** class doesn't exist **")
        elif len(entry) < 2:
            print("** instance id missing **")
        elif "{}.{}".format(entry[0], entry[1]) not in info.keys():
            print("** no instance found **")
        else:
            del(info["{}.{}".format(entry[0], entry[1])])
            storage.save()

    def do_all(self, line):
        """list all instances based on class or all"""
        info = storage.all()
        entry = line.split(" ")
        lis = []
        if len(line) == 0:
            for key, val in info.items():
                lis.append(str(val))
        elif entry[0] not in self.__classes.keys():
            print("** class doesn't exist **")

        else:
            for key, val in info.items():
                cls = key.split(".")
                if cls[0] == entry[0]:
                    lis.append(str(val))

        print(lis)

    def do_update(self, line):
        """adding or udating an attribute in instance already created"""
        info = storage.all()
        entry = line.split(" ")
        if len(line) == 0:
            print("** class name missing **")
        elif entry[0] not in self.__classes.keys():
            print("** class doesn't exist **")
        elif len(entry) < 2:
            print("** instance id missing **")
        elif "{}.{}".format(entry[0], entry[1]) not in info.keys():
            print("** no instance found **")
        elif len(entry) < 3:
            print("** attribute name missing **")
        elif len(entry) < 4:
            print("** value missing **")
        else:
            insta = info["{}.{}".format(entry[0], entry[1])]
            value = entry[3]
            if value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            else:
                value = value
            try:
                insta.__dict__[entry[2]] = eval(value)
                insta.save()
            except Exception:
                insta.__dict__[entry[2]] = value
                insta.save()

    def default(self, line):
        """to retrieve all instances of a class by using: <class name>.all()"""
        k = line.split(".")
        if len(line) == 0:
            return
        else:
            args_class = k[0]
            if args_class in HBNBCommand.__classes:
                if len(k) == 2:
                    if k[1] == "all()":
                        HBNBCommand.do_all(self, args_class)
                    elif k[1] == "count()":
                        HBNBCommand.do_count(self, args_class)
                    elif k[1][0:4] == "show":
                        id = k[1][6:-2]
                        args = "{} {}".format(k[0], id)
                        HBNBCommand.do_show(self, args)
                    elif k[1][0:7] == "destroy":
                        id = k[1][9:-2]
                        args = "{} {}".format(k[0], id)
                        HBNBCommand.do_destroy(self, args)

                    elif k[1][:6] == "update":
                        info = k[1][7:-1]
                        value = info.split(", ")
                        id = value[0][1:-1]
                        attr = value[1][1:-1]
                        attr_val = value[2]
                        args = "{} {} {} {}".format(k[0], id, attr, attr_val)
                        HBNBCommand.do_update(self, args)

    def do_count(self, line):
        """count number of objects of a class"""
        k = line.split(" ")
        if len(line) == 0:
            return
        else:
            count = 0
            if k[0] in HBNBCommand.__classes:
                for key in storage.all().keys():
                    j = key.split(".")
                    if k[0] == j[0]:
                        count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
