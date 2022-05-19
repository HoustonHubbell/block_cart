from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime


from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import UserMixin, LoginManager




from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    coin = db.relationship('Coin', backref = 'owner', lazy = True)


    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify


    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database"
        


class Coin(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    rank = db.Column(db.Integer())
    price = db.Column(db.Numeric(precision=20, scale=2))
    volume = db.Column(db.Numeric(precision=20, scale=2), nullable = True)
    ticker = db.Column(db.String(100))
    market_cap = db.Column(db.Numeric(precision=20, scale=2))
    percent_change = db.Column(db.Numeric(precision=10, scale=2))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, rank, price, volume, ticker, market_cap, percent_change, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.rank = rank
        self.price = price
        self.volume = volume
        self.ticker = ticker
        self.market_cap = market_cap
        self.percent_change = percent_change
        self.user_token = user_token

    def __repr__(self):
        return f"The following Coin has been added: {self.name}"

    def set_id(self):
        return (secrets.token_urlsafe())



class CoinSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'rank', 'price', 'volume', 'ticker', 'market_cap', 'percent_change']

coin_schema = CoinSchema()
coins_schema = CoinSchema(many = True)