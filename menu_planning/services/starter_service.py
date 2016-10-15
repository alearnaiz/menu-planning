from menu_planning.models import Starter, DailyMenu
from sqlalchemy.sql.expression import func, text


class StarterService(object):

    def get_by_id(self, id):
        return Starter.query.filter_by(id=id).first()

    def get_days(self, menu_id, day):
        return int(Starter.query.with_entities(func.sum(Starter.days)).
                   join(DailyMenu, DailyMenu.starter_id == Starter.id).
                   filter(DailyMenu.menu_id == menu_id, DailyMenu.day >= day).first()[0])

    def get_starter_left(self, menu_id, day):
        date_add = func.date_add(DailyMenu.day, text('Interval starter.days-1 day'))
        return Starter.query.join(DailyMenu, DailyMenu.starter_id == Starter.id).filter(DailyMenu.menu_id == menu_id,
                                                                                        date_add >= day).first()

    def get_by_id_and_menu_id(self, id, menu_id):
        return Starter.query.join(DailyMenu, DailyMenu.starter_id == Starter.id).filter(DailyMenu.menu_id == menu_id, Starter.id == id).first()

    def get_random(self):
        return Starter.query.order_by(func.rand()).first()