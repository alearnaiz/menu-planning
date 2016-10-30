from menu_planning.models import Ingredient
from menu_planning import db


class IngredientService(object):

    def get_by_id(self, id):
        return Ingredient.query.filter_by(id=id).first()

    def get_all(self):
        return Ingredient.query.all()

    def create(self, name):
        ingredient = Ingredient(name=name)
        db.session.add(ingredient)
        db.session.commit()
        return ingredient
