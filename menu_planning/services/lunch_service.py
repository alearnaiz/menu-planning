from menu_planning.models import Lunch, DailyMenu
from sqlalchemy.sql.expression import func, text


class LunchService(object):

    def get_by_id(self, id):
        return Lunch.query.filter_by(id=id).first()

    def get_by_id_and_menu_id(self, id, menu_id):
        return Lunch.query.join(DailyMenu, DailyMenu.lunch_id == Lunch.id).filter(DailyMenu.menu_id == menu_id, Lunch.id == id).first()

    def get_random(self):
        return Lunch.query.order_by(func.rand()).first()

    def get_all(self):
        return Lunch.query.all()
