from menu_planning.models import Starter, DailyMenu
from sqlalchemy.sql.expression import func, text


class StarterService(object):

    def get_by_id(self, id):
        return Starter.query.filter_by(id=id).first()

    def get_random(self):
        return Starter.query.order_by(func.rand()).first()
