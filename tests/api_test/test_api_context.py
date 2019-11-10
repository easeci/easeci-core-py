import unittest
from unittest.mock import MagicMock

from api.api_context import ApiContext


class TestApiContext(unittest.TestCase):

    def test_should_correctly_add_controller_and_initialize_this_with_predefined_list(self):
        api_context = ApiContext(MagicMock())
        api_context.init_controller_list()

        self.assertTrue(len(api_context.controllers_initialized) > 0)
