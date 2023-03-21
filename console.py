#!/usr/bin/python3
"""entry point of the command interpreter"""
import cmd
import sys
import re
import os
from datetime import datetime
import uuid
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
# import shlex  # for splitting the line along spaces except in double quotes


class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '
    classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review}

    def do_quit(self, line):
        "Quit command to exit the program"
        return True

    do_EOF = do_quit

    def do_create(self, args):
        """ Create an object of any class"""
        ignored_attrs = ('id', 'created_at', 'updated_at', '__class__')
        class_name = ''
        name_pattern = r'(?P<name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'
        class_match = re.match(name_pattern, args)
        obj_kwargs = {}
        if class_match is not None:
            class_name = class_match.group('name')
            params_str = args[len(class_name):].strip()
            params = params_str.split(' ')
            str_pattern = r'(?P<t_str>"([^"]|\")*")'
            float_pattern = r'(?P<t_float>[-+]?\d+\.\d+)'
            int_pattern = r'(?P<t_int>[-+]?\d+)'
            param_pattern = '{}=({}|{}|{})'.format(
                name_pattern,
                str_pattern,
                float_pattern,
                int_pattern
            )
            for param in params:
                param_match = re.fullmatch(param_pattern, param)
                if param_match is not None:
                    key_name = param_match.group('name')
                    str_v = param_match.group('t_str')
                    float_v = param_match.group('t_float')
                    int_v = param_match.group('t_int')
                    if float_v is not None:
                        obj_kwargs[key_name] = float(float_v)
                    if int_v is not None:
                        obj_kwargs[key_name] = int(int_v)
                    if str_v is not None:
                        obj_kwargs[key_name] = str_v[1:-1].replace('_', ' ')
        else:
            class_name = args
        if not class_name:
            print("** class name missing **")
            return
        elif class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            if not hasattr(obj_kwargs, 'id'):
                obj_kwargs['id'] = str(uuid.uuid4())
            if not hasattr(obj_kwargs, 'created_at'):
                obj_kwargs['created_at'] = str(datetime.now())
            if not hasattr(obj_kwargs, 'updated_at'):
                obj_kwargs['updated_at'] = str(datetime.now())
            new_instance = HBNBCommand.classes[class_name](**obj_kwargs)
            new_instance.save()
            print(new_instance.id)
        else:
            new_instance = HBNBCommand.classes[class_name]()
            for key, value in obj_kwargs.items():
                if key not in ignored_attrs:
                    setattr(new_instance, key, value)
            new_instance.save()
            print(new_instance.id)

    def do_show(self, line):
        """shows an object"""
        if not len(line):
            print("** class name missing **")
            return
        strings = split(line)
        if strings[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(strings) == 1:
            print("** instance id missing **")
            return
        keyValue = strings[0] + '.' + strings[1]
        if keyValue not in storage.all().keys():
            print("** no instance found **")
        else:
            print(storage.all()[keyValue])

    def do_destroy(self, line):
        """deletes an object"""
        if not len(line):
            print("** class name missing **")
            return
        strings = split(line)
        if strings[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(strings) == 1:
            print("** instance id missing **")
            return
        keyValue = strings[0] + '.' + strings[1]
        if keyValue not in storage.all().keys():
            print("** no instance found **")
            return
        del storage.all()[keyValue]
        storage.save()

    def do_all(self, line):
        """prints all"""
        if not len(line):
            print([obj for obj in storage.all().values()])
            return
        strings = split(line)
        if strings[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        print([obj for obj in storage.all().values()
               if strings[0] == type(obj).__name__])

    def do_update(self, line):
        """updates an object"""
        if not len(line):
            print("** class name missing **")
            return
        strings = split(line)
        for string in strings:
            if string.startswith('"') and string.endswith('"'):
                string = string[1:-1]
        if strings[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(strings) == 1:
            print("** instance id missing **")
            return
        keyValue = strings[0] + '.' + strings[1]
        if keyValue not in storage.all().keys():
            print("** no instance found **")
            return
        if len(strings) == 2:
            print("** attribute name missing **")
            return
        if len(strings) == 3:
            print("** value missing **")
            return
        try:
            setattr(storage.all()[keyValue], strings[2], eval(strings[3]))
        except:
            setattr(storage.all()[keyValue], strings[2], strings[3])

    def emptyline(self):
        """passes"""
        pass

    def stripper(self, st):
        """strips that line"""
        newstring = st[st.find("(")+1:st.rfind(")")]
        newstring = shlex.shlex(newstring, posix=True)
        newstring.whitespace += ','
        newstring.whitespace_split = True
        return list(newstring)

    def dict_strip(self, st):
        """tries to find a dict while stripping"""
        newstring = st[st.find("(")+1:st.rfind(")")]
        try:
            newdict = newstring[newstring.find("{")+1:newstring.rfind("}")]
            return eval("{" + newdict + "}")
        except:
            return None

    def default(self, line):
        """defaults"""
        subArgs = self.stripper(line)
        strings = list(shlex.shlex(line, posix=True))
        if strings[0] not in HBNBCommand.classes:
            print("*** Unknown syntax: {}".format(line))
            return
        if strings[2] == "all":
            self.do_all(strings[0])
        elif strings[2] == "count":
            count = 0
            for obj in storage.all().values():
                if strings[0] == type(obj).__name__:
                    count += 1
            print(count)
            return
        elif strings[2] == "show":
            key = strings[0] + " " + subArgs[0]
            self.do_show(key)
        elif strings[2] == "destroy":
            key = strings[0] + " " + subArgs[0]
            self.do_destroy(key)
        elif strings[2] == "update":
            newdict = self.dict_strip(line)
            if type(newdict) is dict:
                for key, val in newdict.items():
                    keyVal = strings[0] + " " + subArgs[0]
                    self.do_update(keyVal + ' "{}" "{}"'.format(key, val))
            else:
                key = strings[0]
                for arg in subArgs:
                    key = key + " " + '"{}"'.format(arg)
                self.do_update(key)
        else:
            print("*** Unknown syntax: {}".format(line))
            return


if __name__ == '__main__':
    HBNBCommand().cmdloop()
