from menu_planning.models import DailyMenu
from menu_planning import db


class DailyMenuService(object):

    def create(self, day, menu_id, lunch_id, dinner_id, starter_id):
        daily_menu = DailyMenu(day, menu_id, lunch_id, dinner_id, starter_id)
        db.session.add(daily_menu)
        db.session.commit()
        return daily_menu

    def update(self, daily_menu):
        db.session.add(daily_menu)
        db.session.commit()
        return daily_menu
