from menu_planning.models import Lunch, DailyMenu
from sqlalchemy.sql.expression import func, text


class LunchService(object):

    def get_by_id(self, id):
        return Lunch.query.filter_by(id=id).first()

    def get_lunch_left(self, menu_id, day):
        date_add = func.date_add(DailyMenu.day, text('Interval lunch.days-1 day'))
        return Lunch.query.join(DailyMenu, DailyMenu.lunch_id == Lunch.id).filter(DailyMenu.menu_id == menu_id, date_add >= day).first()

    def get_by_id_and_menu_id(self, id, menu_id):
        return Lunch.query.join(DailyMenu, DailyMenu.lunch_id == Lunch.id).filter(DailyMenu.menu_id == menu_id, Lunch.id == id).first()

    def get_random(self):
        return Lunch.query.order_by(func.rand()).first()
