from yaml.scanner import ScannerError
from yaml import load, dump, FullLoader

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
"""


def yml_append(path, val):
    pass


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
