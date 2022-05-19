from urllib import response
from flask import Blueprint, request, jsonify
from block_inventory.helpers import token_required
from block_inventory.models import db, User, Coin, coin_schema, coins_schema 

api = Blueprint('api', __name__, url_prefix ='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}

@api.route('/coins', methods = ['POST'])
@token_required
def create_coin(current_user_token):
    name = request.json['name']
    rank = request.json['rank']
    price = request.json['price']
    volume = request.json['volume']
    ticker = request.json['ticker']
    market_cap = request.json['market_cap']
    percent_change = request.json['percent_change']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    coin = Coin(name, rank, price, volume, ticker, market_cap, percent_change, user_token = user_token)


    db.session.add(coin)
    db.session.commit()

    response = coin_schema.dump(coin)
    return jsonify(response)

@api.route('/coins', methods = ['GET'])
@token_required
def get_coins(current_user_token):
    owner = current_user_token.token
    coins = Coin.query.filter_by(user_token = owner).all()
    response = coins_schema.dump(coins)
    return jsonify(response)

@api.route('/coins/<id>', methods = ['GET'])
@token_required
def get_coin(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        coin = Coin.query.get(id)
        response = coin_schema.dump(coin)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


@api.route('/coins/<id>', methods = ['POST', 'PUT'])
@token_required
def update_coin(current_user_token, id):
    coin = Coin.query.get(id)

    coin.name = request.json['name']
    coin.rank = request.json['rank']
    coin.price = request.json['price']
    coin.volume = request.json['volume']
    coin.ticker = request.json['ticker']
    coin.market_cap = request.json['market_cap']
    coin.percent_change = request.json['percent_change']
    coin.user_token = current_user_token.token

    db.session.commit()
    response = coin_schema.dump(coin)
    return jsonify(response)

@api.route('/coins/<id>', methods = ['DELETE'])
@token_required
def delete_coin(current_user_token, id):
    coin = Coin.query.get(id)
    db.session.delete(coin)
    db.session.commit()
    response = coin_schema.dump(coin)
    return jsonify(response)