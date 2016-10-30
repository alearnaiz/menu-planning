from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os
app = Flask(__name__)
with open(os.getcwd() + '/credentials.json') as data_file:
    data = json.load(data_file)['mysql']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}?charset={4}'\
    .format(data['user'], data['password'], data['host'], data['database'], data['charset'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
import menu_planning.views
