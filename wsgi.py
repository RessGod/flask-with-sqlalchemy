# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask
from flask_migrate import Migrate
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

BASE_URL = '/api/v1'

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
migrate = Migrate(app,db)

from schemas import many_product_schema

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200