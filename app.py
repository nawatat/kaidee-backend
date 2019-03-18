import os
import datetime
from flask import Flask, request, jsonify
from models import db, Product, User



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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

#   init app to sqlAchemy
with app.app_context():
    db.init_app(app)

#
#   API
#

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/product/getall", methods=['GET'] )
def getAllProduct():


    try:
        products = Product.query.join( User, Product.seller_id == User.id ).add_columns( Product.seller_id.name ).all()
        print(products)
        return  jsonify([e.serialize() for e in products])
    except Exception as e:
	    return(str(e))

@app.route("/product/getById/<product_id>", methods=['GET'] )
def getAllProductById( product_id ):
    '''
    '''

    pass

@app.route("/product/create", methods=['POST'] )
def createProduct():
    ''' Function to create a new product model
        Method : Post
    '''

    #   Get product info from request
    product_name = request.form.get('name')
    seller_id = request.form.get('sellerId')
    price = request.form.get('price')
    place = request.form.get('place')
    description = request.form.get('description')

    #   assign create and modify date to current date time
    create_date = datetime.datetime.now()
    modify_date = datetime.datetime.now()


    try:
        product = Product(
            product_name = product_name,
            seller_id = seller_id,
            price = price,
            place = place,
            description = description,
            create_date = create_date,
            modify_date = modify_date
        )

        db.session.add(product)
        db.session.commit()

        return "Product added. product id={}".format( product.id )

    except Exception as e:
        return(str(e))

@app.route("/product/edit/<product_id>", methods=['PUT'] )
def editProduct(product_id):
    '''
    '''

    pass

@app.route("/product/delete/<product_id>", methods=['DELETE'] )
def deleteProduct():
    '''
    '''

    pass
    
if __name__ == '__main__':
    app.run()
