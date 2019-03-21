import pytest
import tempfile, os
from flask import jsonify, json

from app import create_app



@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app( )
    
    flask_app.config['TEST'] = True
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()
   

def test_getAllProduct(test_client):
    response = test_client.get("/products")
    assert response.status_code == 200

def test_createProduct( test_client ):

    response = test_client.get("/products")
    oldProductList = json.loads( response.data )

    #   construct request data
    mimetype = 'application/x-www-form-urlencoded'
    headers = {
        'Content-Type': mimetype,
    }
    data = {
        'productName': 'test',
        'sellerId': 1,
        'price': 500,
        'description' : 'test'
    }

    response = test_client.post( "/products", data=data, headers=headers )

    #   Assert create done
    assert response.status_code == 200

    #   Get all product again
    response = test_client.get("/products")
    newProductList = json.loads( response.data )

    assert len( newProductList ) - len( oldProductList ) == 1
