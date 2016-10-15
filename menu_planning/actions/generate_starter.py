from menu_planning.services.starter_service import StarterService


class GenerateStarter(object):

    def __init__(self, menu_id, starter_days_left, starter_service=StarterService()):
        self.menu_id = menu_id
        self.starter_days_left = starter_days_left
        self.starter_service = starter_service

        self.starter = self.starter_service.get_random()

    def has_enough_days(self):
        return self.starter.days <= self.starter_days_left

    def is_already_added(self):
        return self.starter_service.get_by_id_and_menu_id(self.starter.id, self.menu_id)

    def is_valid(self):
        if not self.has_enough_days():
            return False
        if self.is_already_added():
            return False
        return True
