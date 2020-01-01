from app.lib.pre.pipeline import PipelineWrapper

"""
prepare(...) function is responsible for validate and prepare object  
in order to next processing steps.
Returns PipelineWrapper object that is representation of instance ready for processing.
"""


def prepare(pipeline, output_method, logs_persister):
    return PipelineWrapper(pipeline, output_method, logs_persister)
