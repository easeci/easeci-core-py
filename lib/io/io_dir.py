import subprocess
import os


def execute(cmd):
    result = subprocess.check_call(cmd, shell=True)
    if result == 0:
        return True
    else:
        return False


"""
Create dir in full, absolute `path` provided as argument
Return True if directory created with success
Return False if directory not created
"""


def dir_create(path):
    try:
        return execute('mkdir ' + path)
    except subprocess.CalledProcessError:
        return False


"""
Change name of directory pointed at absolute `path`
and `new_name` parameter
"""


def dir_change_name(path, new_name):
    parts = path.split('/')
    parts = list(filter(lambda part: len(part) != 0, parts))
    val_to_change = parts[len(parts) - 1]
    command = 'mv ' + path + ' ' + path.replace(val_to_change, new_name)
    try:
        return execute(command)
    except subprocess.CalledProcessError:
        return False


"""
Remove directory from provided `path`.
If directory is not empty, it cannot be removed.
If you want to remove directory with content, set `force` as True
"""


def dir_delete(path, force=False):
    command = 'rm -r ' + path
    try:
        if len(os.listdir(path)) != 0:
            if force is True:
                execute(command)
            else:
                return False
        else:
            execute(command)
    except FileNotFoundError:
        return False


"""
Returns True if directory exists, or False if directory not exists
"""


def is_dir_exist(path):
    return os.path.isdir(path)
