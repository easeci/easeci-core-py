import unittest

from app.lib.output.output_method import TerminalOutputConsumer
from app.lib.pre.pipeline import PipelineWrapper
from app.lib.pre.prepare import prepare
from app.lib.runner.executor import PipelineExecutor
from app.tests.lib.output.utils import prepare_minimalistic_pipeline


class TestPipelineExecutor(unittest.TestCase):

    def test_should_constructor_initialize_object_and_prepare_OutputMethod(self):
        pipeline = prepare_minimalistic_pipeline()
        log_manager = None                      # not required now
        output_method = 'terminal'              # Output will be published in terminal
        executor = PipelineExecutor(prepare(pipeline, log_manager, output_method))

        self.assertIsNotNone(executor.output_consumer)
        self.assertEqual(type(executor.output_consumer), TerminalOutputConsumer)
        self.assertEqual(len(executor.output_publisher.consumers), 1)

    def test_should_publish_first_info_about_pipeline_parsing_start(self):
        pipeline = prepare_minimalistic_pipeline()
        log_manager = None
        output_method = 'terminal'
        executor = PipelineExecutor(prepare(pipeline, log_manager, output_method))
        executor.start()

        self.assertEqual(executor.output_publisher.event_queue.qsize(), 1)

    def test_should_publish_first_info_about_pipeline_parsing_start_and_consume_event(self):
        pipeline = prepare_minimalistic_pipeline()
        log_manager = None
        output_method = 'terminal'
        executor = PipelineExecutor(prepare(pipeline, log_manager, output_method))
        executor.start()

        # If OutputPublisher._autopublishing is False, we must manual handle event and publish it
        last_event = executor.output_publisher.event_queue.get()
        executor.output_publisher.publish(last_event)

        self.assertEqual(executor.output_publisher.event_queue.qsize(), 0)
