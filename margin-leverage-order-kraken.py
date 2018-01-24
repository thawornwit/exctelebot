# -*- coding: utf-8 -*-

import os
import sys
import json

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402


exchange = ccxt.bxinth({
    'apiKey': '8cdf0f0a666c',
    'secret': 'b6b22e1e51eb',
})

exchange.load_markets()

# for symbol in kraken.symbols:
# print(
# symbol
#'Available leverage levels',
#'Buy:', kraken.markets[symbol]['info']['leverage_buy'],
#'Sell:', kraken.markets[symbol]['info']['leverage_sell']
#   )
#
# with create_order all params (including the price=None) are needed!
# the extra param should be "leverage", not "leverage_sell" nor "leverage-sell"
#kraken.create_order('BTC/THB', 'market', 'sell', 0.0006, 600000, {'leverage': 3})
orders = exchange.fetch_balance()
Trader = exchange.fetch_tickers('DASH/THB')
print(Trader)
#cancel = exchange.cancel_order('492218','DASH/THB')
#print(cancel)
#exchange.create_order()
Result = exchange.create_order('DASH/THB', 'THB', 'buy', 20, 2000,{'leverage': 3})
if Result['info']['success'] == True:
    print("Buy Dash ID:"+Result['info']['order_id'])



print(orders['THB']['total'])
print(orders['THB']['used'])
print(orders['THB']['free'])

    #  or use a shorthand create_market_sell_order (no "price" param)
#kraken.create_market_sell_order('BTC/THB', 0.01, {'leverage': 3})
