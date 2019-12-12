from app.lib.performer.performer import Performer


"""
This function must be defined in each module that will be treated as Performer in EaseCI
By invoke of this, program creates instance if Performer's descending class 
"""


def factorize():
    return Scm()


"""
This function must be defined in each module that will be treated as Performer in EaseCI
By invoke of this, program will know all properties (methods) that was defined in class
"""


def _get_class():
    return Scm


"""
Each class that acts as Performer in EaseCI have to extends Performer class
You should override `abstract` methods defined in Performer class
"""


class Scm(Performer):

    def about(self):
        return 'This is Performer to execute checkout\n' \
               'and pull source code from repository'

    def pull(self, repository_url):
        print('Fetching repository: ' + repository_url)
