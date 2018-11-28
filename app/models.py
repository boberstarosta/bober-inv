import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User({})>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    address = db.Column(db.String(600), index=True)
    vat_number = db.Column(db.String(20), index=True)
    time_created = db.Column(db.DateTime, index=True,
                             default=datetime.datetime.utcnow)
    time_expired = db.Column(db.DateTime, index=True, nullable=True)

    invoices = db.relationship('Invoice', backref='buyer', lazy='dynamic')

    def __repr__(self):
        return '<Buyer({})>'.format(self.name)


class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    value = db.Column(db.Integer)
    
    items = db.relationship('Item', backref='rate', lazy='dynamic')

    def __repr__(self):
        return '<Rate({})>'.format(self.name)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, index=True)
    name = db.Column(db.String(240), index=True)
    unit = db.Column(db.String(20), default='szt.')
    quantity = db.Column(db.Integer, default=1)
    net_price = db.Column(db.Integer)
    rate_id = db.Column(db.Integer, db.ForeignKey('rate.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))

    def __repr__(self):
        return '<Item({})>'.format(self.name)


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), index=True)
    date = db.Column(db.Date, index=True,
                     default=lambda: datetime.datetime.utcnow().today())
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'))

    def __repr__(self):
        return '<Invoice({})>'.format(self.number)

