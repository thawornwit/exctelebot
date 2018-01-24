# -*- coding: utf-8 -*-

import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402

exchange = ccxt.bxinth({
    'apiKey': '8cdf0f0a666c',
    'secret': 'b6b22e1e51eb',
})

orders = exchange.fetch_balance()
#print(orders)

#order = exchange.fetch_order(orders[0]['id'])
print(orders['THB']['total'])
print(orders['THB']['used'])
print(orders['THB']['free'])
