from menu_planning import db
from sqlalchemy.sql import func, expression


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    daily_menus = db.relationship('DailyMenu', backref='menu', lazy='select')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return 'Menu {0}, created at {1}'.format(self.id, self.created_at)


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


class Lunch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    days = db.Column(db.Integer, default=1)
    related_lunch = db.relationship('Lunch', uselist=False, backref='dinner', lazy='select')

    def __init__(self, name, days=1):
        self.name = name
        self.days = days

    def __repr__(self):
        return 'Dinner {0}, name {1}'.format(self.id, self.name)


class Starter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Starter {0}, name {1}'.format(self.id, self.name)
