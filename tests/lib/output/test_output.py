import unittest

from lib.output.output_method import OutputPublisher, OutputEvent, TerminalOutputConsumer
from tests.lib.output.utils import prepare_event, prepare_event_sequence


class TestOutput(unittest.TestCase):

    def test_should_new_object_have_empty_queue(self):
        out = OutputPublisher()

        self.assertIsNotNone(out.event_queue)
        self.assertEqual(0, out.event_queue.qsize())
        self.assertEqual(True, out.event_queue.empty())

    def test_should_cannot_put_to_queue_other_object_than_OutputEvent(self):
        out = OutputPublisher()
        ob = 'wrong object'

        with self.assertRaises(OutputEvent.EventException):
            out.collect(ob)
        self.assertEqual(0, out.event_queue.qsize())

    def test_should_put_correctly_OutputEvent_to_queue(self):
        out = OutputPublisher()
        event = prepare_event()
        out.collect(event)

        self.assertIsNotNone(out.event_queue)
        self.assertEqual(1, out.event_queue.qsize())

    def test_should_put_correctly_many_OutputEvent_objects_to_queue(self):
        out = OutputPublisher()
        event_list = prepare_event_sequence()
        for event in event_list:
            out.collect(event)

        self.assertIsNotNone(out.event_queue)
        self.assertEqual(len(event_list), out.event_queue.qsize())

    def test_should_first_event_put_on_queue_should_first_out(self):
        out = OutputPublisher()
        event_list = prepare_event_sequence()
        first_event = event_list[0]
        for event in event_list:
            out.collect(event)

        first_on_queue = out.event_queue.get()
        self.assertEqual(len(event_list) - 1, out.event_queue.qsize())
        self.assertEqual(first_event.signal, first_on_queue.signal)
        self.assertEqual(first_event.title, first_on_queue.title)
        self.assertEqual(first_event.content, first_on_queue.content)
        self.assertEqual(first_event.error, first_on_queue.error)
        self.assertIsNotNone(first_on_queue.timestamp)

    def test_should_queue_be_overloaded_and_raise_exception(self):
        out = OutputPublisher()

        with self.assertRaises(OutputPublisher.QueueOverloadedException):
            [out.collect(prepare_event()) for _ in range(out._max_queue_size + 1)]

    def test_should_consume_one_event_successfully(self):
        out = OutputPublisher()
        out.collect(prepare_event())

        consumed = out.publish()
        self.assertIsNotNone(consumed)
        self.assertIsNotNone(consumed.timestamp)
        self.assertEqual(0, out.event_queue.qsize())

    def test_should_not_consume_event_if_queue_is_just_empty(self):
        out = OutputPublisher()

        consumed = out.publish()
        self.assertIsNotNone(consumed)
        self.assertIsNotNone(consumed.error)

#   Observer Design Pattern workflow tests (here OutputPublisher acts as Observable, and OutputConsumer as Observer)

    def test_should_add_consumer_with_success(self):
        publisher = OutputPublisher()
        consumer = TerminalOutputConsumer()
        publisher.add_consumer(consumer)

        self.assertIsNotNone(publisher.consumers)
        self.assertEqual(1, len(publisher.consumers))

    def test_should_not_add_observer_because_type_is_not_OutputConsumer(self):
        publisher = OutputPublisher()
        bad_type_consumer = 'string'

        with self.assertRaises(TypeError):
            publisher.add_consumer(bad_type_consumer)

        self.assertIsNotNone(publisher.consumers)
        self.assertEqual(0, len(publisher.consumers))

    def test_should_collect_event_and_publish_it_to_each_consumer(self):
        publisher = OutputPublisher()
        consumer = TerminalOutputConsumer()
        publisher.add_consumer(consumer)

        event = prepare_event()
        publisher.collect(event)
        publisher.publish()

        self.assertTrue(consumer._received)
        self.assertEqual(0, publisher.event_queue.qsize())
        self.assertEqual(1, len(publisher.consumers))

    def test_should_publishing_without_collecting_events_on_queue(self):
        publisher = OutputPublisher()
        consumer = TerminalOutputConsumer()
        publisher.add_consumer(consumer)

        event = prepare_event()
        publisher.publish(event=event)

        self.assertTrue(consumer._received)
        self.assertEqual(0, publisher.event_queue.qsize())
        self.assertEqual(1, len(publisher.consumers))
