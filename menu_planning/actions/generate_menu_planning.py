from datetime import date, timedelta

from menu_planning.actions.generate_lunch import GenerateLunch
from menu_planning.actions.generate_dinner import GenerateDinner
from menu_planning.actions.generate_starter import GenerateStarter
from menu_planning.services.daily_menu_service import DailyMenuService
from menu_planning.services.lunch_service import LunchService
from menu_planning.services.dinner_service import DinnerService
from menu_planning.services.starter_service import StarterService
from menu_planning.services.menu_service import MenuService


class GenerateMenuPlanning(object):

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
        current_starter = None
        current_lunch = None
        current_dinner = None
        num_starter_days = 0
        num_lunch_days = 0
        num_dinner_days = 0
        sum_starter_days_by_lunch = 0

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
                current_dinner = self.generate_dinner(menu.id, lunch_days_left=lunch_days_left,
                                                      dinner_days_left=dinner_days_left)
                dinner_days_left -= 1
            else:
                if lunch_days_left > 0:
                    if current_lunch and current_lunch.days > num_lunch_days:
                        add_new_lunch = False
                    elif current_dinner and current_dinner.related_lunch and \
                            (not current_lunch or current_lunch.id != current_dinner.related_lunch.id):
                        num_lunch_days = 0
                        add_new_lunch = False
                        current_lunch = current_dinner.related_lunch
                    else:
                        add_new_lunch = True
                else:
                    current_lunch = None
                    current_starter = None
                    add_new_lunch = False

                if dinner_days_left > 0:
                    if current_dinner and current_dinner.days > num_dinner_days:
                        add_new_dinner = False
                        dinner_left = True
                    else:
                        add_new_dinner = True
                        dinner_left = False
                else:
                    current_dinner = None
                    add_new_dinner = False
                    dinner_left = False

                if add_new_lunch:
                    current_lunch = self.generate_lunch(menu.id, lunch_days_left=lunch_days_left,
                                                        dinner_days_left=dinner_days_left, dinner_left=dinner_left)
                    current_starter = None
                    num_starter_days = 0
                    sum_starter_days_by_lunch = 0
                    num_lunch_days = 1
                    if current_lunch.related_dinner_id:
                        num_dinner_days = 0
                        current_dinner = self.dinner_service.get_by_id(id=current_lunch.related_dinner_id)
                        add_new_dinner = False
                else:
                    num_lunch_days += 1

                if current_lunch and current_lunch.need_starter:
                    if current_starter:
                        if current_starter.days > num_starter_days:
                            num_starter_days += 1
                            sum_starter_days_by_lunch += 1
                        else:
                            current_starter = self.generate_starter(menu.id, starter_days_left=
                                                                    current_lunch.days - sum_starter_days_by_lunch)
                            num_starter_days = 1
                            sum_starter_days_by_lunch += 1
                    else:
                        current_starter = self.generate_starter(menu.id, starter_days_left=current_lunch.days)
                        num_starter_days = 1
                        sum_starter_days_by_lunch += 1
                else:
                    current_starter = None
                    sum_starter_days_by_lunch = 0
                    num_starter_days = 0

                lunch_days_left -= 1

                if add_new_dinner:

                    if current_lunch.days > num_lunch_days:
                        lunch_left = True
                    else:
                        lunch_left = False

                    current_dinner = self.generate_dinner(menu.id, lunch_days_left=lunch_days_left,
                                                          dinner_days_left=dinner_days_left, lunch_left=lunch_left)

                    num_dinner_days = 1
                else:
                    num_dinner_days += 1

                dinner_days_left -= 1

            dinner_id = current_dinner.id if current_dinner else None
            starter_id = current_starter.id if current_starter else None
            lunch_id = current_lunch.id if current_lunch else None

            self.daily_menu_service.create(current_date, menu.id, lunch_id=lunch_id, dinner_id=dinner_id,
                                           starter_id=starter_id)

            # Update variables
            current_date += timedelta(days=1)

        return menu

    @classmethod
    def generate_lunch(cls, menu_id, lunch_days_left, dinner_days_left, dinner_left=None):
        for i in range(cls.MAX_RETRIES):
            generate_lunch = GenerateLunch(menu_id=menu_id, lunch_days_left=lunch_days_left,
                                           dinner_days_left=dinner_days_left,
                                           dinner_left=dinner_left)
            if generate_lunch.is_valid():
                lunch = generate_lunch.lunch
                break
        if i == cls.MAX_RETRIES-1:
            raise Exception('We could not do a menu planning. Try again')
        return lunch

    @classmethod
    def generate_dinner(cls, menu_id, lunch_days_left, dinner_days_left, lunch_left=None):
        for i in range(cls.MAX_RETRIES):
            generate_dinner = GenerateDinner(menu_id=menu_id, lunch_days_left=lunch_days_left,
                                             dinner_days_left=dinner_days_left,
                                             lunch_left=lunch_left)
            if generate_dinner.is_valid():
                dinner = generate_dinner.dinner
                break
        if i == cls.MAX_RETRIES-1:
            raise Exception('We could not do a menu planning. Try again')
        return dinner

    @classmethod
    def generate_starter(cls, menu_id, starter_days_left):
        for i in range(cls.MAX_RETRIES):
            generate_starter = GenerateStarter(menu_id=menu_id, starter_days_left=starter_days_left)
            if generate_starter.is_valid():
                starter = generate_starter.starter
                break
        if i == cls.MAX_RETRIES-1:
            raise Exception('We could not do a menu planning. Try again')
        return starter

