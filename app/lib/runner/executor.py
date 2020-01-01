"""
PipelineExecutor is main class for start gathering ingredients (variables, performers, objects etc.),
parsing declarative code and make another steps to prepare object
that is ready for executing on engine (distributed, local or remote system)
"""
import datetime

from app.lib.output.output_method import OutputMethod, OutputPublisher, OutputEvent, Signal


class PipelineExecutor:
    """
    pipeline - dictionary with main key `pipeline`, parsed yaml or any other
    """

    def __init__(self, pipeline_wrapper):
        self.pipeline_raw = pipeline_wrapper.pipeline
        self.log_manager = pipeline_wrapper.log_manager
        self.output_method = pipeline_wrapper.output_method
        self.prepare_output()
        if pipeline_valid(self.pipeline_raw)['hasError'] is True:
            pass

    def prepare_output(self):
        self.output_publisher = OutputPublisher()
        self.output_consumer = OutputMethod[self.output_method].value
        self.output_publisher.add_consumer(self.output_consumer)

    def start(self):
        self.parse_pipeline()

    def parse_pipeline(self):
        event = OutputEvent(Signal.a,
                            'Pipeline parsing started',
                            'Executor initialized correctly, and Pipeline parsing started at '
                            + str(datetime.datetime.today()))
        self.output_publisher.collect(event)


def pipeline_valid(pipeline):
    return {
        'hasError': True,
        'errors': {}
    }
