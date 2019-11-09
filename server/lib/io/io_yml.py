from yaml.scanner import ScannerError
from yaml import load, dump, FullLoader
import json

from lib.io.io_file import file_load, file_save, File

"""
Load .yml configuration file and returns dictionary
"""


def yml_load(path):
    file = file_load(path)
    try:
        return load(file.content, Loader=FullLoader)
    except ScannerError:
        return {}


"""
Get one parameter from whole .yml file structure
 `path` is absolute path to file on local disk
 `refs` is path to yml property for example: author.data.name
Returns value of parameter or None if not exist this one
"""


def yml_get(path, refs):
    yaml = yml_load(path)
    refs = refs.split('.')
    ln = len(refs)
    c = 0
    while c < ln:
        try:
            yaml = yaml[refs[c]]
        except KeyError:
            return None
        c = c + 1
    return yaml


"""
Create and save new .yml file in proper format built from dictionary
 `yml_path` is absolute path to file where to save, must end with .yml extension
            or it will be added automatically
 `val` must be dictionary
Returns lib.io.io_facade.File
"""


def yml_create(yml_path, val):
    if (yml_path is None) or (val is None) or (type(val) is not dict):
        return
    content = dump(val)
    file = File(yml_path, content)
    file_save(file)
    return file


"""
Appends new parameters to .yml configuration file
 `path` represents absolute path to .yml file
 `val` is a tuple with two indexes.
        First object must be a reference to yaml object value
        Second object is a value to set for key expressed in reference
Returns dictionary with appended new value
"""


def yml_append(path, val):
    if path is None or type(val) is not tuple or val[0] is None or val[1] is None:
        return None
    yaml_as_dict = yml_load(path)
    refs = val[0].split('.')
    refs_passed = []

    yaml_last_val = yaml_as_dict

    def parse_and_save():
        def insert():
            def replace(old, new):
                return str(yaml_as_dict).replace(old, new)

            def build():
                dict_built = {new_key: val[1]}
                for index, item in enumerate(list(yaml_last_val.keys())):
                    dict_built[list(yaml_last_val.keys())[index]] = yaml_last_val[list(yaml_last_val.keys())[index]]
                return dict_built

            new_key = refs_passed[len(refs_passed) - 1]
            if type(yaml_last_val) is dict:
                _old = str(yaml_last_val)
                _new = str(build())
                return replace(_old, _new)
            if type(yaml_last_val) is int or type(yaml_last_val) is float:
                return replace(str(yaml_last_val), str({new_key: val[1]}))
            return replace("'" + str(yaml_last_val) + "'", str({new_key: val[1]}))
        jsonified = insert().replace("'", "\"")
        casted = json.loads(jsonified)
        file_save(File(path, dump(casted)), False)
        return casted

    for ref in refs:
        refs_passed.append(ref)
        try:
            try:
                yaml_last_val = yaml_last_val[ref]
            except TypeError:
                return parse_and_save()
        except KeyError:
            return parse_and_save()
    return parse_and_save()


"""
Change value of one field in .yml config file
 `path` is absolute path to .yml file
 `val` is a tuple. First value in tuple is path to yml field for example: app.config.path
                   Second value in tuple is value of field to change
"""


def yml_change(path, val):
    pass


"""
Deletes full one parameter in .yml config file
"""


def yml_delete(path, key):
    pass
