"""
Loads file to application in read-only mode.
returns object of class File
"""
import os


def file_load(path):
    with (open(path, 'r', encoding="utf-8")) as file:
        return File(path, file.read())


class File:
    def __init__(self, path, content):
        self.path = path
        self.content = content


"""
First argument must be of type lib.io.io_facade.File
Save file in two modes:
 if `append` parameter is set as `True`, content will be append to file
 if `append` parameter is set as `False` content will override file
If file not exist, this method will create one.
"""


def file_save(file, append=True):
    def write_file(mode):
        with open(file.path, mode, encoding='utf-8') as file_opened:
            file_opened.write(file.content)
            file_opened.close()
    if type(file) is not File:
        raise IOError('Argument of this method must be type of lib.io.io_facade.File !')
    if not file_exist(file.path):
        os.system('touch ' + file.path)
        file_save(file, append)
    else:
        if append:
            write_file('a')
        else:
            write_file('w')


"""
Permanently remove file
 returns `0` (zero) if file was removed
 returns `1` (one) if file not was removed
"""


def file_delete(path):
    if file_exist(path):
        os.system('rm ' + path)
        return 0
    else:
        return 1


"""
Change part of content in file
 `path` is a path to file
 `old` is a string that represents old content to replace with new
 `new` is a string that represents new content
Returns
 `0` (zero) if file was changed
 `1` (one) if file was not changed
"""


def file_change(path, old, new):
    if not file_exist(path):
        return 1
    content = file_load(path).content
    if content.__contains__(old):
        content = content.replace(old, new)
        file_save(File(path, content), False)
        return 0
    return 1


"""
Check if file exists, returns boolean value
"""


def file_exist(path):
    return os.path.isfile(path)
