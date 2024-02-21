from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os
from database import db

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy()
db.init_app(app)
api = Api(app)



if __name__ == '__main__':
    from resources import ProductResource, CartResource
    api.add_resource(ProductResource, '/products', endpoint='products')
    api.add_resource(ProductResource, '/products/<int:product_id>', endpoint='product')
    api.add_resource(CartResource, '/cart', endpoint='cart')
    api.add_resource(CartResource, '/cart/<int:item_id>', endpoint='cart_item')
    with app.app_context():
	    db.create_all()
    app.run(debug=True)
