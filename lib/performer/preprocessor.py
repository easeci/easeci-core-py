from lib.performer.external import *
from lib.performer.external import name_resolver

"""
This module parse Pipeline and extracts method that should be executed
as it is wrote in declarative Pipeline code
"""


# Example invoke in declarative code:
# scm.pull(repository_url)

def consume_performer(invocation):
    module = invocation.split('.')[0]
    return name_resolver[module]
