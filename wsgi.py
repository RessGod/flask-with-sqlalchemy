# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, request
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

from schemas import many_product_schema, one_product_schema

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products/<id>', methods=['GET'])
def get_one_product(id):
    products = db.session.query(Product).get(id) # SQLAlchemy request => 'SELECT * FROM products WHERE id = id'
    return one_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products', methods=['POST'])
def add_product():
    product = Product() # SQLAlchemy request => 'INSERT INTO products (name) VALUES ('Skello')'
    product = request.get_json()
    db.session.add(product)
    db.session.commit()
    return one_product_schema.jsonify(product), 200