class PipelineWrapper:

    def __init__(self, pipeline, log_manager, output_method):
        self.pipeline = pipeline
        self.log_manager = log_manager
        self.output_method = output_method
