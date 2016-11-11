from menu_planning.models import Food, FoodIngredient, DailyMenu
from sqlalchemy import or_
from menu_planning import db


class FoodIngredientService(object):

    def get_all_by_menu_id(self, menu_id):
        return FoodIngredient.query.\
            join(Food, Food.id == FoodIngredient.food_id). \
            join(DailyMenu, or_(DailyMenu.lunch_id == Food.id,
                                DailyMenu.starter_id == Food.id,
                                DailyMenu.dinner_id == Food.id)
                 ). \
            filter(DailyMenu.menu_id == menu_id).all()

    def get_all_by_food_id(self, food_id):
        return FoodIngredient.query.filter_by(food_id=food_id).all()

    def delete_all_by_food_id(self, food_id):
        FoodIngredient.query.filter_by(food_id=food_id).delete()
        db.session.commit()

    def create(self, food_id, ingredient_id, quantity=None):
        food_ingredient = FoodIngredient(food_id=food_id, ingredient_id=ingredient_id, quantity=quantity)
        db.session.add(food_ingredient)
        db.session.commit()
        return food_ingredient

