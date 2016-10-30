import unittest
from mock import MagicMock
from menu_planning.models import Starter
from menu_planning.services.starter_service import StarterService
from menu_planning.actions.starter_generator import StarterGenerator


class TestStarterGenerator(unittest.TestCase):

    def setUp(self):
        self.starter_service = StarterService()

    def test_valid(self):
        self.starter_service.get_random = MagicMock(return_value=Starter('Gazpacho'))

        starter_generator = StarterGenerator(starter_service=self.starter_service)

        assert starter_generator.is_valid()
