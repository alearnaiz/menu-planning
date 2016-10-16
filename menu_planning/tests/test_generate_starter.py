import unittest
from mock import MagicMock
from menu_planning.models import Starter
from menu_planning.services.starter_service import StarterService
from menu_planning.actions.generate_starter import GenerateStarter


class TestGenerateStarter(unittest.TestCase):

    def setUp(self):
        self.starter_service = StarterService

    def test_valid(self):
        self.starter_service.get_random = MagicMock(return_value=Starter('Gazpacho'))

        generate_starter = GenerateStarter( starter_service=self.starter_service)

        assert generate_starter.is_valid()
