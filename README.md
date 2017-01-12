# Menu planning

## Overview
Menu planning is a random generator menu using your common starters, lunches and dinners, then if you want you could send the ingredients to [Any.do](http://es.any.do/) 

## Requirements
* Python 2.7
* MySQL >= 5.6.5

## Install
* pip install -r requirements.txt

## How to use
* Create a env.json file with the following structure in the root directory

```json
{
  "mysql": {
    "database": "xxxx",
    "host": "xxxx",
    "user": "xxxx",
    "password": "xxxx",
    "charset": "xxxx"
  },
  "anydo": {
    "email": "xxxx",
    "password": "xxxx",
    "category_name": "xxxx"
  }
}
```

* Create the initial database. Import the db object from an interactive Python shell in the root directory to create the tables and database

```python
from menu_planning import db
db.create_all()
```

* Insert rows in food, starter, lunch, dinner, food, ingredient tables

```sql
INSERT INTO `food` (id, type) VALUES (1,0);
INSERT INTO `starter` (id, name) VALUES (1,'Salmorejo');
INSERT INTO `ingredient` (id, name) VALUES (1,'Tomate');
INSERT INTO `ingredient` (id, name) VALUES (2,'Ajo');
INSERT INTO `food_ingredient` (food_id, ingredient_id, quantity) VALUES (1,1,5),(1,2,1);

```

* In the root directory run **python runserver.py**

* Open a browser with the URL http://127.0.0.1:5000/
