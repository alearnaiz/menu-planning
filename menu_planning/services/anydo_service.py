from anydo_api.client import Client
from anydo_api.task import Task
import os
import json


class AnydoService(object):

    def __init__(self):
        with open(os.getcwd() + '/credentials.json') as data_file:
            data = json.load(data_file)['anydo']
        self.email = data['email']
        self.password = data['password']
        self.category_name = data['category_name']

    def login(self):
        return Client(email=self.email, password=self.password).get_user()

    def get_category(self, user):
        for category in user.categories():
            if category.name == self.category_name:
                return category
        return None

    def create_task(self, user, category, title):
        category.add_task(Task.create(user=user, title=title))
