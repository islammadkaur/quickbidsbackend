from flask import Flask
from flask_cors import CORS
import alpaca_trade_api as tradeapi
import time
import random
from bot import *

app = Flask(__name__)
CORS(app)
@app.route('/')


def api():
    # run_bot()
    return {
        "account_status": account.status,
        'equity': account.equity,
        'buying_power': account.buying_power,
        'current_stock': asset.symbol,
        'last_price': quote.bidprice
    }
    

if __name__ == '__main__':

    app.run()
    
    #start flask server
    
    # app.run()