from menu_planning.services.dinner_service import DinnerService


class GenerateDinner(object):

    def __init__(self, menu_id, lunch_days_left, dinner_days_left, is_lunch_left=False,
                 dinner_service=DinnerService()):

        self.menu_id = menu_id
        self.lunch_days_left = lunch_days_left
        self.dinner_days_left = dinner_days_left
        self.is_lunch_left = is_lunch_left
        self.dinner_service = dinner_service

        self.dinner = self.dinner_service.get_random()

    def has_enough_days(self):
        return self.dinner.days <= self.dinner_days_left

    def is_already_added(self):
        return self.dinner_service.get_by_id_and_menu_id(self.dinner.id, self.menu_id)

    def can_have_related_lunch(self):
        return not self.is_lunch_left

    def has_related_lunch_enough_days(self):
        return self.dinner.related_lunch.days <= self.lunch_days_left

    def is_valid(self):
        if not self.has_enough_days():
            return False
        if self.is_already_added():
            return False
        if self.dinner.related_lunch and not self.can_have_related_lunch():
            return False
        if self.dinner.related_lunch and not self.has_related_lunch_enough_days():
            return False
        return True
