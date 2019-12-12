import unittest
import app.lib.performer.external.scm as scm
from app.lib.performer.preprocessor import consume_performer


class TestPerformer(unittest.TestCase):

    def test_factorize_should_return_initialized_instance(self):
        instance = scm.factorize()

        self.assertIsNotNone(instance)
        self.assertEqual(type(scm.Scm()), type(instance))

    def test_get_class_should_return_class_of_Performer_descendant_implemented_in_current_module(self):
        clazz = scm._get_class()

        self.assertEqual(scm.Scm, clazz)

    def test_co(self):
        invocation = 'scm.pull(url)'
        result = consume_performer(invocation)
        result.pull('https://github.com/easeci/easeci-core')
