import unittest
from mock import MagicMock
from menu_planning.models import Starter
from menu_planning.services.starter_service import StarterService
from menu_planning.actions.generate_starter import GenerateStarter


class TestGenerateStarter(unittest.TestCase):

    def setUp(self):
        self.starter_service = StarterService

    def test_valid(self):
        self.starter_service.get_random = MagicMock(return_value=Starter('Gazpacho', days=1))
        self.starter_service.get_by_id_and_menu_id = MagicMock(return_value=None)

        generate_starter = GenerateStarter(1, starter_days_left=1, starter_service=self.starter_service)

        assert generate_starter.is_valid()

    def test_invalid_has_enough_days(self):
        self.starter_service.get_random = MagicMock(return_value=Starter('Gazpacho', days=2))
        self.starter_service.get_by_id_and_menu_id = MagicMock(return_value=None)

        generate_starter = GenerateStarter(1, starter_days_left=1, starter_service=self.starter_service)

        assert not generate_starter.is_valid()

    def test_invalid_is_already_add(self):
        starter = Starter('Salmorejo', days=1)
        self.starter_service.get_random = MagicMock(return_value=starter)
        self.starter_service.get_by_id_and_menu_id = MagicMock(return_value=starter)

        generate_starter = GenerateStarter(1, starter_days_left=1, starter_service=self.starter_service)

        assert not generate_starter.is_valid()
