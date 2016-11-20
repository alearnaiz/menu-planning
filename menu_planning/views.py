from menu_planning import app
from menu_planning.actions.menu_generator import MenuGenerator
from menu_planning.actions.anydo_action import AnydoAction
from menu_planning.models import FoodType
from menu_planning.services.daily_menu_service import DailyMenuService
from menu_planning.services.food_ingredient_service import FoodIngredientService
from menu_planning.services.food_service import FoodService
from menu_planning.services.ingredient_service import IngredientService
from menu_planning.services.menu_service import MenuService
from menu_planning.services.lunch_service import LunchService
from menu_planning.services.dinner_service import DinnerService
from menu_planning.services.starter_service import StarterService
from flask import render_template, request, redirect, url_for
from datetime import datetime


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', error=request.args.get('error'))


@app.route('/menu', methods=['POST'])
def create_menu():
    start_lunch = request.form.get('start_lunch')
    end_dinner = request.form.get('end_dinner')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if not start_lunch or not end_dinner or not start_date or not end_date:
        return redirect(url_for('index', error='Wrong parameters'))

    try:
        start_date = get_date(start_date)
        end_date = get_date(end_date)
        days = (end_date - start_date).days + 1

        menu_generator = MenuGenerator()
        menu = menu_generator.generate(days=days, start_date=start_date, start_lunch=get_boolean(start_lunch),
                                       end_dinner=get_boolean(end_dinner))
    except Exception as exception:
        return redirect(url_for('index', error=exception))

    return redirect(url_for('show_menu', menu_id=menu.id))


@app.route('/menu/<menu_id>', methods=['GET'])
def show_menu(menu_id):
    return render_template('show-menu.html', menu=get_menu(menu_id), success=request.args.get('success'))


@app.route('/menu/<menu_id>/edit', methods=['GET'])
def show_editable_menu(menu_id):
    return render_template('edit-menu.html', menu=get_editable_menu(menu_id))


@app.route('/menu/<menu_id>/edit', methods=['POST'])
def edit_menu(menu_id):
    menu_service = MenuService()
    menu = menu_service.get_by_id(menu_id)

    daily_menu_service = DailyMenuService()

    if not menu:
        return redirect(url_for('page_not_found'))

    for daily_menu in menu.daily_menus:
        starter_id = get_int(request.form.get('starter[' + str(daily_menu.day) + ']'))
        lunch_id = get_int(request.form.get('lunch[' + str(daily_menu.day) + ']'))
        dinner_id = get_int(request.form.get('dinner[' + str(daily_menu.day) + ']'))

        daily_menu.starter_id = starter_id
        daily_menu.lunch_id = lunch_id
        daily_menu.dinner_id = dinner_id

        daily_menu_service.update(daily_menu)

    return redirect(url_for('show_menu', menu_id=menu.id))


@app.route('/menu/<menu_id>/favourite', methods=['POST'])
def favourite_menu(menu_id):
    name = request.form.get('name')
    favourite = request.form.get('favourite')

    menu_service = MenuService()
    menu_service.favourite(menu_id, name=name, favourite=get_checkbox(favourite))
    return redirect(url_for('show_menu', menu_id=menu_id, success='Changes updated'))


@app.route('/menu/favourites', methods=['GET'])
def show_favourite_menus():
    menu_service = MenuService()
    menus = menu_service.get_all_by_favourites()
    return render_template('show-favourites.html', menus=menus)


@app.route('/menu/<menu_id>/anydo', methods=['POST'])
def send_ingredients_to_anydo(menu_id):
    anydo_action = AnydoAction()
    anydo_action.add_ingredients(menu_id=menu_id)
    return redirect(url_for('show_menu', menu_id=menu_id, success='Ingredients sent to any.do'))


@app.route('/food', methods=['GET'])
def show_foods():
    food_service = FoodService()
    starter_service = StarterService()
    lunch_service = LunchService()
    dinner_service = DinnerService()

    foods = food_service.get_all()

    starters = []
    lunches = []
    dinners = []

    for food in foods:
        if food.type == FoodType.STARTER:
            starters.append(starter_service.get_by_id(food.id))
        elif food.type == FoodType.LUNCH:
            lunches.append(lunch_service.get_by_id(food.id))
        elif food.type == FoodType.DINNER:
            dinners.append(dinner_service.get_by_id(food.id))
    return render_template('show-foods.html', starters=starters, lunches=lunches, dinners=dinners)


@app.route('/food/<food_id>', methods=['GET'])
def show_food(food_id):
    food_service = FoodService()

    food = food_service.get_by_id(id=food_id)
    if not food:
        return render_template('show-food.html')

    starter_service = StarterService()
    lunch_service = LunchService()
    dinner_service = DinnerService()
    ingredient_service = IngredientService()
    food_ingredient_service = FoodIngredientService()

    if food.type == FoodType.STARTER:
        food.starter = starter_service.get_by_id(food.id)
    elif food.type == FoodType.LUNCH:
        food.lunch = lunch_service.get_by_id(food.id)
    elif food.type == FoodType.DINNER:
        food.dinner = dinner_service.get_by_id(food.id)

    ingredients = ingredient_service.get_all()
    food_ingredients = food_ingredient_service.get_all_by_food_id(food.id)

    return render_template('show-food.html', food=food, ingredients=ingredients, food_ingredients=food_ingredients,
                           success=request.args.get('success'))


@app.route('/food/<food_id>', methods=['POST'])
def edit_food(food_id):
    food_ingredient_service = FoodIngredientService()
    food_ingredient_service.delete_all_by_food_id(food_id)

    ingredients = request.form.getlist('ingredients[]')

    for ingredient_id in ingredients:
        quantity = get_float(request.form.get('quantity_{0}'.format(ingredient_id)))
        if quantity <= 0:
            quantity = None
        food_ingredient_service.create(food_id=food_id, ingredient_id=ingredient_id, quantity=quantity)

    return redirect(url_for('show_food', food_id=food_id, success='Food edited successfully'))


@app.route('/ingredient', methods=['POST'])
def create_ingredient():
    name = request.form.get('name')
    if name:
        ingredient_service = IngredientService()
        ingredient = ingredient_service.create(name)
        return render_template('partials/create-ingredient.html', ingredient=ingredient)
    return ""


@app.errorhandler(404)
def page_not_found(error):
    return "Page Not Found", 404


def get_menu(menu_id):
    menu_service = MenuService()
    menu = menu_service.get_by_id(menu_id)

    if not menu:
        return None

    starter_service = StarterService()
    lunch_service = LunchService()
    dinner_service = DinnerService()

    for daily_menu in menu.daily_menus:

        if daily_menu.lunch_id:
            lunch = lunch_service.get_by_id(daily_menu.lunch_id)
        else:
            lunch = None

        if daily_menu.starter_id:
            starter = starter_service.get_by_id(daily_menu.starter_id)
        else:
            starter = None

        if daily_menu.dinner_id:
            dinner = dinner_service.get_by_id(daily_menu.dinner_id)
        else:
            dinner = None

        daily_menu.starter = starter
        daily_menu.lunch = lunch
        daily_menu.dinner = dinner

    return menu


def get_editable_menu(menu_id):
    menu = get_menu(menu_id)
    if not menu:
        return None

    starter_service = StarterService()
    lunch_service = LunchService()
    dinner_service = DinnerService()

    menu.starters = starter_service.get_all()
    menu.lunches = lunch_service.get_all()
    menu.dinners = dinner_service.get_all()

    return menu


def get_date(date):
    try:
        day, month, year = date.split('-')
        return datetime(int(year), int(month), int(day))
    except Exception:
        raise Exception('Wrong parameters')


def get_boolean(argument):
    if argument == 'True':
        argument = True
    elif argument == 'False':
        argument = False
    else:
        raise Exception('Wrong parameters')

    return argument


def get_int(argument):
    try:
        return int(argument)
    except ValueError:
        return None


def get_float(argument):
    try:
        return float(argument)
    except ValueError:
        return None


def get_checkbox(argument):
    if argument == 'on':
        return True
    else:
        return False
