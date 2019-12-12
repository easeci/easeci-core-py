import unittest

from app.lib.performer.preprocessor import consume_performer


class TestPreprocessor(unittest.TestCase):

    def test_consume_performer_should_correctly_instantiate_Performer_class(self):
        invocation = 'scm.pull(url)'
        instance = consume_performer(invocation)
        instance.pull('https://github.com/easeci/easeci-core')

        self.assertIsNotNone(instance)
