from app.lib.output.output_method import Signal, OutputEvent
import random


def prepare_event():
    signal = Signal.a
    title = 'Fetching tags from Git remote repository'
    content = 'Correctly fetched refs/tags from remote git@github.com:easeci/easeci-core.git'
    return OutputEvent(signal, title, content)


def prepare_event_sequence():
    def rand_signal():
        signal = random.randint(0, 1)
        if signal == 0:
            signal = Signal.a
        else:
            signal = Signal.b
        return signal

    return [
            OutputEvent(rand_signal(), 'Prepare environment', 'Environment was prepared to build process'),
            OutputEvent(rand_signal(), 'Checking out repository code', 'Code was checkout from remote repository'),
            OutputEvent(rand_signal(), 'Building code', 'Code was built in this step'),
            OutputEvent(rand_signal(), 'Publish on server', 'Artifact was published on server in this step')
    ]


def prepare_minimalistic_pipeline():
    return {
        'pipeline': {

        }
    }
