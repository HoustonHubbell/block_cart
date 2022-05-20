from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login.utils import login_required
from block_inventory.helpers import token_required
from block_inventory.api.api import get_top_10, get_ticker
from block_inventory.forms import TickerSearch
from block_inventory.models import Coin, db, User
from flask_login import current_user
import math






site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@site.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    #logged_user = User.query.filter(User.email == email).first()
    form = TickerSearch()
    ticker_data = get_ticker()
    data = get_top_10()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            ticker_search = form.ticker_search.data.upper()
            print(ticker_search)
            for coin in ticker_data:
                if ticker_search in coin.values():
                    name = coin['name']
                    rank = coin['cmc_rank']
                    price = coin['quote']['USD']['price']
                    volume = coin['quote']['USD']['volume_24h']
                    volume = round(volume,2)
                    ticker = coin['symbol']
                    market_cap = coin['quote']['USD']['market_cap']
                    market_cap = round(market_cap,2)
                    percent_change = coin['quote']['USD']['percent_change_24h']
                    percent_change = round(percent_change,2)
                    user_token = current_user.token




                    coin = Coin(name, rank, price, volume, ticker, market_cap, percent_change, user_token = user_token)
                    print(coin)
                    db.session.add(coin)
                    db.session.commit()
                    flash(f"Succesfully added ${coin.name}")
                    return redirect(url_for('site.dashboard'))
                else:
                    flash(f"${ticker_search} not found in top 200")
            return redirect(url_for('site.dashboard'))
    except:
        raise Exception("Please enter a valid Ticker")


    coins = Coin.query.all()


    return render_template('dashboard.html', form=form, ticker_data=ticker_data, coins=coins, data=data)

# @site.route('/cointable')
# @login_required
# def coin_list():
#     coins = Coin.query.all()
#     print(coins)
#     return render_template('dashboard.html', coins=coins)

