from datetime import date, timedelta

from menu_planning.actions.lunch_generator import LunchGenerator
from menu_planning.actions.dinner_generator import DinnerGenerator
from menu_planning.actions.starter_generator import StarterGenerator
from menu_planning.services.daily_menu_service import DailyMenuService
from menu_planning.services.lunch_service import LunchService
from menu_planning.services.dinner_service import DinnerService
from menu_planning.services.starter_service import StarterService
from menu_planning.services.menu_service import MenuService


class MenuGenerator(object):

    MAX_RETRIES = 30

    def __init__(self, starter_service=StarterService(), lunch_service=LunchService(), dinner_service=DinnerService(),
                 daily_menu_service=DailyMenuService(), menu_service=MenuService()):
        self.starter_service = starter_service
        self.lunch_service = lunch_service
        self.dinner_service = dinner_service
        self.daily_menu_service = daily_menu_service
        self.menu_service = menu_service

    def generate(self, days, start_date=date.today(), start_lunch=True, end_dinner=True):

        if days < 1 or (days == 1 and not start_lunch and not end_dinner):
            raise Exception('Wrong parameters')

        # Set variables
        current_lunch = None
        current_dinner = None
        num_lunch_days = 0
        num_dinner_days = 0

        if start_lunch:
            lunch_days_left = days
        else:
            lunch_days_left = days - 1
        if end_dinner:
            dinner_days_left = days
        else:
            dinner_days_left = days - 1
        current_date = start_date

        menu = self.menu_service.create()

        for day in range(days):

            if day == 0 and not start_lunch:
                current_starter = None
                current_lunch = None
                current_dinner = self.dinner_generator(menu.id, lunch_days_left, dinner_days_left)
                num_dinner_days = 1
                dinner_days_left -= 1
            else:
                if lunch_days_left > 0:

                    # Lunch
                    if self.is_lunch_left(current_lunch, num_lunch_days):
                        num_lunch_days += 1
                    elif self.is_mandatory_lunch(current_dinner, menu.id):
                        current_lunch = current_dinner.related_lunch
                        num_lunch_days = 1
                    else:
                        current_lunch = self.lunch_generator(menu.id, lunch_days_left, dinner_days_left,
                                                             is_dinner_left=
                                                             self.is_dinner_left(current_dinner, num_dinner_days))
                        num_lunch_days = 1

                    lunch_days_left -= 1

                    # Starter
                    if current_lunch and current_lunch.need_starter:
                        current_starter = self.starter_generator()
                    else:
                        current_starter = None
                else:
                    current_starter = None
                    current_lunch = None

                if dinner_days_left > 0:

                    # Dinner
                    if self.is_dinner_left(current_dinner, num_dinner_days):
                            num_dinner_days += 1
                    elif self.is_mandatory_dinner(current_lunch, menu.id):
                        current_dinner = self.dinner_service.get_by_id(id=current_lunch.related_dinner_id)
                        num_dinner_days = 1
                    else:
                        current_dinner = self.dinner_generator(menu.id, lunch_days_left, dinner_days_left,
                                                               is_lunch_left=
                                                               self.is_lunch_left(current_lunch, num_lunch_days))
                        num_dinner_days = 1

                    dinner_days_left -= 1
                else:
                    current_dinner = None

            dinner_id = current_dinner.id if current_dinner else None
            starter_id = current_starter.id if current_starter else None
            lunch_id = current_lunch.id if current_lunch else None

            self.daily_menu_service.create(current_date, menu.id, lunch_id=lunch_id, dinner_id=dinner_id,
                                           starter_id=starter_id)

            # Update variable
            current_date += timedelta(days=1)

        return menu

    @classmethod
    def lunch_generator(cls, menu_id, lunch_days_left, dinner_days_left, is_dinner_left=False):
        is_found = False
        for i in range(cls.MAX_RETRIES):
            lunch_generator = LunchGenerator(menu_id=menu_id, lunch_days_left=lunch_days_left,
                                             dinner_days_left=dinner_days_left,
                                             is_dinner_left=is_dinner_left)
            if lunch_generator.is_valid():
                lunch = lunch_generator.lunch
                is_found = True
                break
        if not is_found:
            raise Exception('We could not do a menu planning. Try again')
        return lunch

    @classmethod
    def dinner_generator(cls, menu_id, lunch_days_left, dinner_days_left, is_lunch_left=False):
        is_found = False
        for i in range(cls.MAX_RETRIES):
            dinner_generator = DinnerGenerator(menu_id=menu_id, lunch_days_left=lunch_days_left,
                                               dinner_days_left=dinner_days_left,
                                               is_lunch_left=is_lunch_left)
            if dinner_generator.is_valid():
                dinner = dinner_generator.dinner
                is_found = True
                break
        if not is_found:
            raise Exception('We could not do a menu planning. Try again')
        return dinner

    @classmethod
    def starter_generator(cls):
        is_found = False
        for i in range(cls.MAX_RETRIES):
            starter_generator = StarterGenerator()
            if starter_generator.is_valid():
                starter = starter_generator.starter
                is_found = True
                break
        if not is_found:
            raise Exception('We could not do a menu planning. Try again')
        return starter

    @classmethod
    def is_lunch_left(cls, lunch, num_lunch_days):
        return lunch and (lunch.days > num_lunch_days)

    @classmethod
    def is_dinner_left(cls, dinner, num_dinner_days):
        return dinner and (dinner.days > num_dinner_days)

    def is_mandatory_lunch(self, dinner, menu_id):
        return dinner and dinner.related_lunch and not \
            self.lunch_service.get_by_id_and_menu_id(id=dinner.related_lunch.id, menu_id=menu_id)

    def is_mandatory_dinner(self, lunch, menu_id):
        return lunch and lunch.related_dinner_id and not \
            self.dinner_service.get_by_id_and_menu_id(id=lunch.related_dinner_id, menu_id=menu_id)
