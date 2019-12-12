import subprocess

"""
This method show current directory
"""


def pwd():
    stdout = subprocess.check_output('pwd', shell=True)
    return stdout.decode('utf-8').strip()
