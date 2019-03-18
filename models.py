from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column( db.Integer, primary_key=True )
    username = db.Column( db.String(64), unique=True )
    password_hash = db.Column( db.String(128) )
    firstname = db.Column( db.String(120) )
    lastname = db.Column( db.String(120) )
    products = db.relationship('Product', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def serialize(self):
        return {
            'id': self.id, 
            'username': self.username,
            'firstname' : self.firstname,
            'lastname' : self.lastname
        }
    

class Product(db.Model):

    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    price = db.Column(db.Numeric())
    place = db.Column(db.String(100))
    description = db.Column(db.String(500))
    create_date = db.Column(db.DateTime())
    modify_date = db.Column(db.DateTime())

    def __repr__(self):
        return '<Product {} price = {} >'.format( self.product_name, self.price )

    def serialize(self):
        return {
            'id': self.id, 
            'product_name': self.product_name,
            'seller_id' : self.seller_id,
            'price' : self.price,
            'place' : self.place,
            'description' : self.description,
            'create_date' : self.create_date,
            'modify_date' : self.modify_date
        }
