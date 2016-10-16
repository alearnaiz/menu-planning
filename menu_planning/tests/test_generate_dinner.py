import unittest
from mock import MagicMock
from menu_planning.models import Lunch, Dinner
from menu_planning.services.dinner_service import DinnerService
from menu_planning.actions.generate_dinner import GenerateDinner


class TestGenerateDinner(unittest.TestCase):

    def setUp(self):
        self.dinner_service = DinnerService

    def test_valid(self):
        self.dinner_service.get_random = MagicMock(return_value=Dinner(name='Eggs', days=1))
        self.dinner_service.get_by_id_and_menu_id = MagicMock(return_value=None)

        generate_dinner = GenerateDinner(1, lunch_days_left=2, dinner_days_left=2, dinner_service=self.dinner_service)

        assert generate_dinner.is_valid()

    def test_invalid_has_enough_days(self):
        self.dinner_service.get_random = MagicMock(return_value=Dinner(name='Sandwich', days=3))
        self.dinner_service.get_by_id_and_menu_id = MagicMock(return_value=None)

        generate_dinner = GenerateDinner(1, lunch_days_left=2, dinner_days_left=2, dinner_service=self.dinner_service)

        assert not generate_dinner.is_valid()

    def test_invalid_is_already_add(self):
        dinner = Dinner(name='Soup', days=1)
        self.dinner_service.get_random = MagicMock(return_value=dinner)
        self.dinner_service.get_by_id_and_menu_id = MagicMock(return_value=dinner)

        generate_dinner = GenerateDinner(1, lunch_days_left=2, dinner_days_left=2, dinner_service=self.dinner_service)

        assert not generate_dinner.is_valid()

    def test_invalid_can_have_related_dinner(self):
        dinner = Dinner(name='Chicken')
        dinner.related_lunch = Lunch(name="Beef")
        self.dinner_service.get_random = MagicMock(return_value=dinner)
        self.dinner_service.get_by_id_and_menu_id = MagicMock(return_value=None)

        generate_dinner = GenerateDinner(1, lunch_days_left=2, dinner_days_left=2, is_lunch_left=True,
                                         dinner_service=self.dinner_service)

        assert not generate_dinner.is_valid()

    def test_invalid_has_related_dinner_enough_days(self):
        dinner = Dinner(name='Chicken', days=1)
        dinner.related_lunch = Lunch(name="Beef", days=3)
        self.dinner_service.get_random = MagicMock(return_value=dinner)
        self.dinner_service.get_by_id_and_menu_id = MagicMock(return_value=None)

        generate_dinner = GenerateDinner(1, lunch_days_left=2, dinner_days_left=2, dinner_service=self.dinner_service)

        assert not generate_dinner.is_valid()
