from menu_planning.models import Food


class FoodService(object):

    def get_by_id(self, id):
        return Food.query.filter_by(id=id).first()

    def get_all(self):
        return Food.query.all()
