import alpaca_trade_api as tradeapi
import time
import datetime
import random

api = tradeapi.REST('PKT89ZPCZGV1X6V8H7JX', 'FC0EOE4sP3cszqYftMMWyYvUOAXabuQNiPcHhkTO', base_url='https://paper-api.alpaca.markets')
account = api.get_account()
portfolio = api.list_positions()
sym = "ZOM"
barset = api.get_barset(sym, '1Min', limit=30)
asset = api.get_asset(sym)
quote = api.get_last_quote(sym)

for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))


class bot:
    def __init__(self, stock):
        self.STOCK = stock
        self.is_buy = True
        self.cycles = 0
        self.target = 2000
        self.BUY_QTY = self.share_amt(self.STOCK, self.target)
        self.PROFIT_THRESHOLD = 1.025
        self.STOP_LOSS_THRESHOLD = 0.01
        priceObj = api.get_last_trade(self.STOCK)
        self.open_price = getattr(priceObj, 'price')
        self.limit_ID = ''
        self.stop_ID = ''



    def trade(self, cycles):
        while(self.check_cycles(cycles)):
            if(self.is_buy):
                current_price = self.get_price(self.STOCK)
                deviation = 100*(current_price - self.open_price) / current_price
                print('Current price: $' + str(self.get_price(self.STOCK)) + '\n')
                print('Placing order ' + self.STOCK + '... (dev. ' + str(deviation) + '%)')
                self.buy_attempt(current_price)

            else:
                if(len(api.list_orders()) == 0):
                    print('You sold your stock for an average share price of $' + str(self.get_price(self.STOCK)) + '.')
                    self.is_buy = True
                    self.cycles += 1
                    return
                try:
                    root_order = api.list_orders(nested=True, status='all')[0]
                except IndexError:
                    self.is_buy = True
                    print(api.list_orders(nested=True))
                    print('try-catch block activated.')
                    return
                limit_id = self.get_limit_id(root_order)
                limit_price = getattr(api.get_order(limit_id), 'limit_price')
                stop_id = self.get_stop_id(root_order)
                stop_price = getattr(api.get_order(stop_id), 'stop_price')
                print(self.STOCK + ' current price: $' + str(self.get_price(self.STOCK)))
                print('Your profit target is $' + limit_price + ' and stop loss is set to $' + stop_price + '\n')

    def buy_attempt(self, deviation):
            print('Placing BUY order...')
            self.open_price = self.place_buy_order()

    def place_buy_order(self):
        self.is_buy = False

        price = self.get_price(self.STOCK)
        limit_price = price * self.PROFIT_THRESHOLD 
        stop_loss = price * self.STOP_LOSS_THRESHOLD
        order_obj = api.submit_order(self.STOCK, self.BUY_QTY, 'buy', 'limit', 'day',
                                     limit_price= price,
                                     order_class='bracket',
                                     take_profit={'limit_price' : limit_price },
                                     stop_loss={'stop_price' : stop_loss}
                                     )
        print('Buy order placed of ' + str(self.BUY_QTY) + ' shares at $' + str(self.get_price(self.STOCK)))
        return order_obj

    def get_price(self, ticker):
        priceObj = api.get_last_trade(ticker)
        return getattr(priceObj, 'price')

    def get_limit_id(self, root_order):
        for i in getattr(root_order, 'legs'):
            if getattr(i, 'order_type') == 'limit':
                return getattr(i, 'id')

    def get_stop_id(self, root_order):
        for i in getattr(root_order, 'legs'):
            if getattr(i, 'order_type') == 'stop':
                return getattr(i, 'id')

    def check_cycles(self, cycles):
        return self.cycles < cycles

    def share_amt(self, stock, target):
        price = self.get_price(stock)
        return int(target / price)

def run_bot():
    b = bot(sym)
    b.trade(1)

if __name__ == '__main__':
    for i in range (3000):
        run_bot()
    print('Finished at ' + str(time.ctime()))
    
