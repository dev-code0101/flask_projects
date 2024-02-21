from flask_restful import Resource, reqparse
from database import db
from models import Product, CartItem

# Request parser for product operations
product_parser = reqparse.RequestParser()
product_parser.add_argument('name', type=str, required=True, help='Name is required')
product_parser.add_argument('description', type=str, required=True, help='Description is required')
product_parser.add_argument('price', type=float, required=True, help='Price is required')
product_parser.add_argument('image_url', type=str, required=True, help='Image URL is required')

# Request parser for cart operations
cart_parser = reqparse.RequestParser()
cart_parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
cart_parser.add_argument('quantity', type=int, required=True, help='Quantity is required')

class ProductResource(Resource):
    """Resource class for handling product-related operations."""
    def get(self, product_id=None):
        """Get method to fetch all products or a specific product."""
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return {'id': product.id, 'name': product.name, 'description': product.description,
                        'price': product.price, 'image_url': product.image_url}
            else:
                return {'message': 'Product not found'}, 404
        else:
            products = Product.query.all()
            return [{'id': product.id, 'name': product.name, 'description': product.description,
                     'price': product.price, 'image_url': product.image_url} for product in products]

    def post(self):
        """Post method to create a new product."""
        args = product_parser.parse_args()
        product = Product(name=args['name'], description=args['description'], 
                          price=args['price'], image_url=args['image_url'])
        db.session.add(product)
        db.session.commit()
        return {'message': 'Product created', 'data': {'id': product.id}}, 201

    def put(self, product_id):
        """Put method to update a specific product."""
        args = product_parser.parse_args()
        product = Product.query.get(product_id)
        if product:
            product.name = args['name']
            product.description = args['description']
            product.price = args['price']
            product.image_url = args['image_url']
            db.session.commit()
            return {'message': 'Product updated', 'data': {'id': product.id}}, 200
        else:
            return {'message': 'Product not found'}, 404

    def delete(self, product_id):
        """Delete method to delete a specific product."""
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return {'message': 'Product deleted'}, 200
        else:
            return {'message': 'Product not found'}, 404

class CartResource(Resource):
    """Resource class for handling cart-related operations."""
    def post(self):
        """Post method to add a product to the cart."""
        args = cart_parser.parse_args()
        product_id = args['product_id']
        quantity = args['quantity']
        cart_item = CartItem(product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
        return {'message': 'Product added to cart', 'data': {'id': cart_item.id}}, 201

    def get(self):
        """Get method to retrieve cart items."""
        cart_items = CartItem.query.all()
        return [{'id': item.id, 'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items]

    def delete(self, item_id):
        """Delete method to remove a specific item from the cart."""
        cart_item = CartItem.query.get(item_id)
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return {'message': 'Item removed from cart'}, 200
        else:
            return {'message': 'Item not found'}, 404
        

