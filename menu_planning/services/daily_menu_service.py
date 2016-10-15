from menu_planning.models import DailyMenu
from menu_planning import db
from sqlalchemy import desc


class DailyMenuService(object):

    def create(self, day, menu_id, lunch_id, dinner_id, starter_id):
        daily_menu = DailyMenu(day, menu_id, lunch_id, dinner_id, starter_id)
        db.session.add(daily_menu)
        db.session.commit()
        return daily_menu

    def get_last_by_menu_id_and_lunch_id(self, menu_id, lunch_id):
        return DailyMenu.query.filter(DailyMenu.menu_id == menu_id, DailyMenu.lunch_id == lunch_id).order_by(desc(DailyMenu.day)).first()
