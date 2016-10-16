from menu_planning import app
from menu_planning.actions.generate_menu_planning import GenerateMenuPlanning
from menu_planning.services.menu_service import MenuService
from menu_planning.services.lunch_service import LunchService
from menu_planning.services.dinner_service import DinnerService
from menu_planning.services.starter_service import StarterService
from flask import render_template, request, redirect, url_for
from datetime import datetime


@app.route('/', methods=['GET'])
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)


@app.route('/generate_menu', methods=['POST'])
def generate_menu():
    start_lunch = request.form.get('start_lunch')
    end_dinner = request.form.get('end_dinner')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if not start_lunch or not end_dinner or not start_date or not end_date:
        return redirect(url_for('index', error='Wrong parameters'))

    start_date = get_date(start_date)
    end_date = get_date(end_date)
    days = (end_date - start_date).days + 1

    generate_menu_planning = GenerateMenuPlanning()
    try:
       menu = generate_menu_planning.generate(days=days, start_date=start_date, start_lunch=get_boolean(start_lunch),
                                              end_dinner=get_boolean(end_dinner))
    except Exception as exception:
        return redirect(url_for('index', error=exception))

    return redirect(url_for('menu', menu_id=menu.id))


@app.route('/menu/<menu_id>', methods=['GET'])
def menu(menu_id):
    return render_template('menu.html', menu=get_menu(menu_id))


@app.errorhandler(404)
def page_not_found():
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


def get_date(date):
    month, day, year = date.split('/')
    return datetime(int(year), int(month), int(day))


def get_boolean(argument):
    if argument == 'True':
        argument = True
    elif argument == 'False':
        argument = False
    else:
        raise Exception('Wrong parameters')

    return argument




