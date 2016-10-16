from menu_planning.services.dinner_service import DinnerService
from menu_planning.services.lunch_service import LunchService


class GenerateLunch(object):

    def __init__(self, menu_id, lunch_days_left, dinner_days_left, dinner_left=False,
                 lunch_service=LunchService(), dinner_service=DinnerService()):
        self.menu_id = menu_id
        self.lunch_days_left = lunch_days_left
        self.dinner_days_left = dinner_days_left
        self.dinner_left = dinner_left
        self.lunch_service = lunch_service
        self.dinner_service = dinner_service

        self.lunch = self.lunch_service.get_random()

    def has_enough_days(self):
        return self.lunch.days <= self.lunch_days_left

    def is_already_added(self):
        return self.lunch_service.get_by_id_and_menu_id(self.lunch.id, self.menu_id)

    def can_have_related_dinner(self):
        return not self.dinner_left

    def has_related_dinner_enough_days(self):
        dinner = self.dinner_service.get_by_id(id=self.lunch.related_dinner_id)
        return dinner.days <= self.dinner_days_left

    def is_valid(self):
        if not self.has_enough_days():
            return False
        if self.is_already_added():
            return False
        if self.lunch.related_dinner_id and not self.can_have_related_dinner():
            return False
        if self.lunch.related_dinner_id and not self.has_related_dinner_enough_days():
            return False
        return True
