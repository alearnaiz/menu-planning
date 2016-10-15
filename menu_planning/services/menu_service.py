from menu_planning.models import Menu
from menu_planning import db


class MenuService(object):

    def create(self):
        menu = Menu()
        db.session.add(menu)
        db.session.commit()
        return menu

    def get_by_id(self, id):
        return Menu.query.filter(Menu.id == id).first()
