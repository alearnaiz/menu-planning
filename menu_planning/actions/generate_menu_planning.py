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

    MAX_RETIRES = 30

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
                lunch_left = self.lunch_service.get_lunch_left(menu.id, current_date)
                dinner_left = self.dinner_service.get_dinner_left(menu.id, current_date)
                starter_left = self.starter_service.get_starter_left(menu.id, current_date)

                if lunch_days_left > 0:
                    if not lunch_left:
                        generate_lunch = True
                        if current_dinner and current_dinner.related_lunch and \
                                (not current_lunch or current_lunch.id != current_dinner.related_lunch.id):
                            current_lunch = current_dinner.related_lunch
                            generate_lunch = False

                        if generate_lunch:
                            current_lunch = self.generate_lunch(menu.id, lunch_days_left=lunch_days_left,
                                                                dinner_days_left=dinner_days_left,
                                                                dinner_left=dinner_left)
                        if current_lunch.need_starter:
                            current_starter = self.generate_starter(menu.id, starter_days_left=current_lunch.days)
                        else:
                            current_starter = None

                    elif lunch_left and lunch_left.need_starter and not starter_left:
                        current_lunch = None
                        daily_menu = self.daily_menu_service.get_last_by_menu_id_and_lunch_id(menu.id, lunch_left.id)
                        starter_days = self.starter_service.get_days(menu.id, daily_menu.day)
                        if starter_days < lunch_left.days:
                            current_starter = self.generate_starter(menu.id, lunch_left.days - starter_days)
                        else:
                            current_starter = None
                    else:
                        current_starter = None
                        current_lunch = None
                else:
                    current_starter = None
                    current_lunch = None

                lunch_days_left -= 1

                if dinner_days_left > 0:
                    if not dinner_left:
                        generate_dinner = True
                        if current_lunch and current_lunch.related_dinner_id and \
                                (not current_dinner or current_dinner.id != current_lunch.related_dinner_id):
                            current_dinner = self.dinner_service.get_by_id(id=current_lunch.related_dinner_id)
                            generate_dinner = False

                        if generate_dinner:

                            if current_lunch:
                                if current_lunch.days > 1:
                                    lunch = current_lunch
                                else:
                                    lunch = None
                            else:
                                lunch = lunch_left

                            current_dinner = self.generate_dinner(menu.id, lunch_days_left=lunch_days_left,
                                                                  dinner_days_left=dinner_days_left,
                                                                  lunch_left=lunch)
                    else:
                        current_dinner = None
                else:
                    current_dinner = None

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
        for i in range(cls.MAX_RETIRES):
            generate_lunch = GenerateLunch(menu_id=menu_id, lunch_days_left=lunch_days_left,
                                           dinner_days_left=dinner_days_left,
                                           dinner_left=dinner_left)
            if generate_lunch.is_valid():
                lunch = generate_lunch.lunch
                break
        if i == cls.MAX_RETIRES-1:
            raise Exception('We could not do a menu planning. Try again')
        return lunch

    @classmethod
    def generate_dinner(cls, menu_id, lunch_days_left, dinner_days_left, lunch_left=None):
        for i in range(cls.MAX_RETIRES):
            generate_dinner = GenerateDinner(menu_id=menu_id, lunch_days_left=lunch_days_left,
                                             dinner_days_left=dinner_days_left,
                                             lunch_left=lunch_left)
            if generate_dinner.is_valid():
                dinner = generate_dinner.dinner
                break
        if i == cls.MAX_RETIRES-1:
            raise Exception('We could not do a menu planning. Try again')
        return dinner

    @classmethod
    def generate_starter(cls, menu_id, starter_days_left):
        for i in range(cls.MAX_RETIRES):
            generate_starter = GenerateStarter(menu_id=menu_id, starter_days_left=starter_days_left)
            if generate_starter.is_valid():
                starter = generate_starter.starter
                break
        if i == cls.MAX_RETIRES-1:
            raise Exception('We could not do a menu planning. Try again')
        return starter

