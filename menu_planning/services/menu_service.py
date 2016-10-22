from menu_planning.models import Menu
from menu_planning import db


class MenuService(object):

    def create(self, name=None, favourite=False):
        menu = Menu(name=name, favourite=favourite)
        db.session.add(menu)
        db.session.commit()
        return menu

    def get_by_id(self, id):
        return Menu.query.filter(Menu.id == id).first()

    def get_all_by_favourites(self):
        return Menu.query.filter(Menu.favourite.is_(True)).all()

    def favourite(self, menu_id, name=None, favourite=False):
        menu = self.get_by_id(menu_id)
        menu.name = name
        menu.favourite = favourite
        db.session.commit()
