"""
How to install performer in our EaseCI backend service?
Just move script that contains class
"""
from lib.performer.external.scm import factorize

__all__ = [
    'scm'
]

name_resolver = {
    'scm': factorize()
}
