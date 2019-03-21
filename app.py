import os
import datetime
from flask import Flask, request, jsonify, make_response, Blueprint
from models import db, Product, User

bp = Blueprint('api', __name__,)

def create_app():

    app = Flask(__name__)
    
    #   config to connect database
    POSTGRES = {
        'user': 'postgres',
        'pw': '2484',
        'db': 'kaidee_store',
        'host': 'localhost',
        'port': '5432',
    }

    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False  

    app.app_context().push()
    db.init_app(app)

    app.register_blueprint(bp)

    return app



#
#   API
#

@bp.route("/products", methods=['GET'] )
def getAllProduct():
    ''' Function to get all product
        Method : Get
    '''

    
    #   Get all product
    try:
        products = Product.query.order_by( Product.id ).all()

        return make_response( jsonify( [ e.serialize() for e in products ] ), 200 )

    except Exception as e:
	    return make_response( str(e), 500 )

@bp.route("/products/<int:product_id>", methods=['GET'] )
def getProductById( product_id ):
    ''' Function to get a product by product id
        Method : Get
    '''

    #   Get product
    try:
        product = Product.query.filter( Product.id == product_id ).first()

        if( product == None ):
            return make_response( "Product not found.", 404 )
        else:
            return make_response( jsonify( product.serialize() ), 200 )

    except Exception as e:
        return make_response( str(e), 500 )


@bp.route("/products", methods=['POST'] )
def createProduct():
    ''' Function to create a new product model
        Method : Post
    '''

    newProduct = Product()
    
    #   Get product info from request
    newProduct.product_name = request.form.get('productName')
    newProduct.seller_id = request.form.get('sellerId')
    newProduct.price = request.form.get('price')
    newProduct.place = request.form.get('place')
    newProduct.description = request.form.get('description')

    #   assign create and modify date to current date time
    newProduct.create_date = datetime.datetime.now()
    newProduct.modify_date = datetime.datetime.now()

    #   save to db
    try:
        db.session.add( newProduct )
        db.session.commit()

        return make_response( jsonify( newProduct.serialize() ), 200 )

    except Exception as e:
        return make_response( str(e), 500 )

@bp.route("/products/<int:product_id>", methods=['PUT'] )
def editProduct( product_id ):
    ''' Function to update product
        Method : Put
        NOTE: Product cannot be update seller_id
    '''

    #   Get product
    try:
        product = Product.query.filter( Product.id == product_id ).first()

        if( product == None ):
            return make_response( "Product not found.", 404 )

        #   Get product info from request
        product.product_name = request.form.get('productName')
        product.price = request.form.get('price')
        product.place = request.form.get('place')
        product.description = request.form.get('description')

        #   update modify date to current date time
        product.modify_date = datetime.datetime.now()

        #   Save to database
        db.session.commit()

        #   Return updated product
        return make_response( jsonify( product.serialize() ), 200 )

    except Exception as e:
        return make_response( str(e), 500 )


@bp.route("/products/<int:product_id>", methods=['DELETE'] )
def deleteProduct( product_id ):
    ''' Function to delete product
        Method : Delete
    '''

    #   Get product
    try:
        product = Product.query.filter( Product.id == product_id ).first()

        if( product == None ):
            return make_response( "Product not found.", 404 )

        db.session.delete( product )
        db.session.commit()

        return make_response( "Delete success", 200 )

    except Exception as e:
        return make_response( str(e), 500 )

@bp.route("/users", methods=['POST'] )
def createUser( ):
    ''' Functino to create user
        Method : Post
    '''

    #   construct new user
    newUser = User()

    #   get data from request
    newUser.firstname = request.form.get('firstname')
    newUser.lastname = request.form.get('lastname')
    newUser.username = request.form.get('username')
    newUser.password_hash = request.form.get('password')

    try:

        #   find user from username
        user = User.query.filter( User.username == newUser.username ).first()

        #   return if username is already exists
        if( user ):
            return make_response( "Username already exist !!", 500 )
        
        #   save to db
        db.session.add( newUser )
        db.session.commit()

        return make_response( jsonify( newUser.serialize() ), 200 )

    except Exception as e:
        return make_response( str(e), 500 )
        
if __name__ == '__main__':
    app = create_app()
    app.run()
