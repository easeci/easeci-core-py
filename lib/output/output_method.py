import abc
from enum import Enum
from queue import Queue
from datetime import datetime


class OutputPublisher:
    _max_queue_size = 100     # TODO inject this value from general.yml when settings context will be ready
    _max_consumers_size = 15  # TODO
    _autopublishing = False   # TODO

    def __init__(self):
        self.consumers = set()
        self.event_queue = Queue()

    def add_consumer(self, consumer):
        if not issubclass(type(consumer), OutputConsumer):
            raise TypeError('You can add only OutputConsumer to set of consumers!')
        self.consumers.add(consumer)

    def collect(self, output_event):
        if self.event_queue.qsize() >= self._max_queue_size:
            raise self.QueueOverloadedException('Queue is overloaded because reached maximum size! '
                                                'Probably nothing consume this!')

        def timestamp():
            output_event.timestamp = datetime.now()
        if type(output_event) is not OutputEvent:
            raise OutputEvent.EventException('Cannot put to event_queue object different than '
                                             'lib.output.output_method.OutputEvent')
        timestamp()
        if self._autopublishing is True:
            self.publish(event=output_event)
        else:
            self.event_queue.put(output_event)

    class QueueOverloadedException(Exception):
        def __init__(self, message):
            super().__init__(message)

    def publish(self, event=None):
        def from_queue():
            if self.event_queue.qsize() == 0:
                _event = OutputEvent.EventError('Empty', 'Queue is empty')
                return OutputEvent(Signal.e, '', '', _event)
            last_event = self.event_queue.get()
            return send(last_event)

        def send(_event):
            for consumer in self.consumers:
                consumer.consume(_event)
            return _event

        if event is None:
            return from_queue()
        else:
            return send(event)


class OutputEvent:

    def __init__(self, signal, title, content, error=None):
        self.signal = signal
        self.timestamp = None
        self.title = title
        self.content = content
        self.error = error

    def __str__(self):
        def timestamp():
            if self.timestamp is None:
                return '-'
            else:
                return self.timestamp

        if self.error is not None:
            return self.error.__str__()
        return f'\n==> {self.title}' + \
               f'\n===> ended with signal: {self.signal}' \
               f'\n===> {self.content}' \
               f'\n===> timestamp: {timestamp()}'

    class EventError:

        def __init__(self, title, content):
            self.title = title
            self.content = content

        def __str__(self):
            return '\n*** *** Error occurred!' + \
                   f'\n*** Cause: {self.title}' + \
                   f'\n*** Message: {self.content}'

    class EventException(Exception):
        def __init__(self, message):
            super().__init__(message)


'''
Class Signal describes how the event was ended.
This is similar to Unix shell code.
    Statuses:
    a - everything went successfully
    b - event was ended with some error
    c - queue is empty
'''


class Signal(Enum):
    a = 0
    b = 1
    e = 2


class OutputConsumer(metaclass=abc.ABCMeta):
    _received = False

    def consume(self, event):
        raise NotImplementedError()


class TerminalOutputConsumer(OutputConsumer):
    def consume(self, event):
        self._received = True
        print(event)


class OutputMethod(Enum):
    terminal = TerminalOutputConsumer()
