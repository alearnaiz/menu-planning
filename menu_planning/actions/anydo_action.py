from menu_planning.services.anydo_service import AnydoService
from menu_planning.services.food_ingredient_service import FoodIngredientService
from menu_planning.services.ingredient_service import IngredientService


class AnydoAction(object):

    def __init__(self, ingredient_service=IngredientService(), food_ingredient_service=FoodIngredientService(),
                 anydo_service=AnydoService()):
        self.ingredient_service = ingredient_service
        self.food_ingredient_service = food_ingredient_service
        self.anydo_service = anydo_service

    def add_ingredients(self, menu_id):
        food_ingredients = self.food_ingredient_service.get_all_by_menu_id(menu_id=menu_id)
        food_used = []
        ingredients = {}
        for food_ingredient in food_ingredients:
            quantity = food_ingredient.quantity if food_ingredient.quantity else 0
            if food_ingredient.ingredient_id not in ingredients.keys():
                ingredients[food_ingredient.ingredient_id] = quantity
                food_used.append(food_ingredient.food_id)
            else:
                if food_ingredient.food_id not in food_used:
                    ingredients[food_ingredient.ingredient_id] += quantity

        if ingredients:
            user = self.anydo_service.login()
            category = self.anydo_service.get_category(user)
            for ingredient_id, quantity in ingredients.iteritems():
                ingredient = self.ingredient_service.get_by_id(ingredient_id)
                if quantity > 0:
                    title = '{0}, quantity {1}'.format(ingredient.name, quantity)
                else:
                    title = '{0}'.format(ingredient.name)
                self.anydo_service.create_task(category=category, user=user, title=title)
