from sqlalchemy.sql.expression import func, text
from menu_planning.models import Dinner, DailyMenu


class DinnerService(object):

    def get_by_id(self, id):
        return Dinner.query.filter_by(id=id).first()

    def get_by_id_and_menu_id(self, id, menu_id):
        return Dinner.query.join(DailyMenu, DailyMenu.dinner_id == Dinner.id).filter(DailyMenu.menu_id == menu_id,
                                                                                     Dinner.id == id).first()

    def get_random(self):
        return Dinner.query.order_by(func.rand()).first()

    def get_all(self):
        return Dinner.query.all()
