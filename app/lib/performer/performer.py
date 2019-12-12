from abc import abstractmethod


class Performer:

    """
    This method should return note about extension's destination,
    author, organisation or basic information about licence or
    how to run this Performer.
    """

    @abstractmethod
    def about(self):
        raise NotImplementedError('about() method in Performer class is not implemented yet')
