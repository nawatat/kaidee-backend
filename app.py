import os
from flask import Flask, request, jsonify
from models import db, Product



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

#   init app to sqlAchemy
db.init_app(app)

#
#   API
#

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/product/getall")
def getAllProduct():
    try:
        products = Product.query.all()
        return  jsonify([e.serialize() for e in products])
    except Exception as e:
	    return(str(e))

@app.route("/product/getById/<product_id>")
def getAllProductById( product_id ):
    '''
    '''

    pass

def createProduct():
    '''
    '''

    pass

def editProduct():
    '''
    '''

    pass

def deleteProduct():
    '''
    '''

    pass
    
if __name__ == '__main__':
    app.run()
