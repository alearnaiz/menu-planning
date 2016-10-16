from menu_planning.services.starter_service import StarterService


class GenerateStarter(object):

    def __init__(self, starter_service=StarterService()):
        self.starter_service = starter_service

        self.starter = self.starter_service.get_random()

    def is_valid(self):
        return True
