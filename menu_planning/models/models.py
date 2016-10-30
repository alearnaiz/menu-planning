from menu_planning import db
from sqlalchemy.sql import func, expression


class FoodType(object):
    STARTER = 0
    LUNCH = 1
    DINNER = 2


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    daily_menus = db.relationship('DailyMenu', backref='menu', lazy='select')
    favourite = db.Column(db.Boolean, server_default=expression.false())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, name=None, favourite=False):
        self.name = name
        self.favourite = favourite

    def __repr__(self):
        return 'Menu {0}, name {1}, created at {2}'.format(self.id, self.name, self.created_at)


class DailyMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    lunch_id = db.Column(db.Integer, db.ForeignKey('lunch.id'), nullable=True)
    dinner_id = db.Column(db.Integer, db.ForeignKey('dinner.id'), nullable=True)
    starter_id = db.Column(db.Integer, db.ForeignKey('starter.id'), nullable=True)

    def __init__(self, day, menu_id, lunch_id=None, dinner_id=None, starter_id=None):
        self.day = day
        self.menu_id = menu_id
        self.lunch_id = lunch_id
        self.dinner_id = dinner_id
        self.starter_id = starter_id

    def __repr__(self):
        return 'Daily menu {0}, day {1}'.format(self.id, self.day)


class FoodIngredient(db.Model):
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    quantity = db.Column(db.Float, nullable=True)

    def __init__(self, food_id, ingredient_id, quantity=None):
        self.food_id = food_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity

    def __repr__(self):
        return 'FoodIngredient, food {0}, ingredient {1}, quantity {2}'.format(self.food_id, self.ingredient_id,
                                                                               self.quantity)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return 'Food {0}, type {1}'.format(self.id, self.type)


class Lunch(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    days = db.Column(db.Integer, default=1)
    need_starter = db.Column(db.Boolean, server_default=expression.false())
    related_dinner_id = db.Column(db.Integer, db.ForeignKey('dinner.id'), nullable=True)

    def __init__(self, name, days=1, need_starter=False, related_dinner_id=None):
        self.name = name
        self.days = days
        self.need_starter = need_starter
        self.related_dinner_id = related_dinner_id

    def __repr__(self):
        return 'Lunch {0}, name {1}'.format(self.id, self.name)


class Dinner(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    days = db.Column(db.Integer, default=1)
    related_lunch = db.relationship('Lunch', uselist=False, backref='dinner', lazy='select')

    def __init__(self, name, days=1):
        self.name = name
        self.days = days

    def __repr__(self):
        return 'Dinner {0}, name {1}'.format(self.id, self.name)


class Starter(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Starter {0}, name {1}'.format(self.id, self.name)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Ingredient {0}, name {1}'.format(self.id, self.name)
