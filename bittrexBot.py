from bittrex_tokens import *  ## for accessing telegram api
import matplotlib  ## for ploting graph
import os
import sys
from pprint import pprint

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

from symbols import *
import ccxt

matplotlib.use("Agg")  # has to be before any other matplotlibs imports to set a "headless" backend
import matplotlib.pyplot as plt  ## create object plt for ploting graph
import psutil  ## for get utility system
from datetime import datetime  ## for datetime
# import datetime
from subprocess import Popen, PIPE, STDOUT  ## for
import operator
import collections  ## for put management collection
import sys
import os
import time
import threading  ## for management threading
import random
import telepot  ## for interact with telegram
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
#######Import Mail #######
import smtplib
import re
####Import Emoji###
import emoji
######Check Email #######
import pymysql
from bittrexBot_function import *
#### Table format ###
import time
import requests
import hashlib
import hmac
import pdb

# pdb.set_trace()
StopLoss_Point2 = 0
StopLoss_Point = 0
TICK_INTERVAL = 5  # seconds
# API_KEY = 'a7e650878ca94b428f2bb43547793aa7'
# API_SECRET_KEY = b'bcfd8047a5f94d108714fc2d38092780'
Enable = "OFF"


def cutloss(UUID, Exchange, coin_markets):
    BuyRate = Get_BittrexOrder_buy(UUID, Exchange, 'order_buy', 'Rate')
    StopLoss = Get_BittrexDB(UUID, Exchange, 'ckloss', 'Stoploss')
    CutLoss = Get_BittrexDB(UUID, Exchange, 'ckloss', 'Cutloss')
    print("--------------------------")
    print('1.Start Bot cutloss ..')
    print('2.BuyRate=>' + str(BuyRate))
    print('2.StopLoss=>' + str(StopLoss))
    print('3.CutLoss=>' + str(CutLoss))
    LastPrice = Get_Bittrex_Price('USDT-BCC', Exchange)  ## Sim for Tesss
    print('LastPrice=>' + str(LastPrice))
    CutLossPrice = (BuyRate - (BuyRate * (CutLoss / 100)))
    print('4.CutLossPrice=>' + str(CutLossPrice))
    MinProfit = (BuyRate + (BuyRate * (CutLoss / 100)))
    print("Minimum Profit=>" + str(MinProfit))
    print("Buy Cost =>" + str(BuyRate) + " Price Up =>" + str(LastPrice - BuyRate) + " (+/-) =>" + str(
        (100 * (LastPrice - BuyRate)) / BuyRate) + "%")
    print("--------------------------")
    # market_summaries = simple_request('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    # for summary in market_summaries['result']:
    # market = summary['MarketName']
    # day_close = summary['PrevDay']
    # last = summary['Last']
    # if day_close > 0:
    #       percent_chg = ((last / day_close) - 1) * 100
    #    else:
    #       print('day_close zero for ' + market)
    #
    #    if market == coin_markets:
    #       LastPrice=last

    #print('CutLoss:'+str(CutLoss))
    #print(market + ' changed ' + str(percent_chg))
    #print('### Balance ###')
    #print('Last price:'+str(last))

    # For test only ##
    ## Price UP ##
    if LastPrice > BuyRate:
        if StopLoss != "" or StopLoss != 0:
            StopLoss_Point2 = Get_BittrexDB(UUID, Exchange, 'ckloss', 'StoplossPoint')
            StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))
            print('StopLoss_Point1=' + str(StopLoss_Point))
            print('StopLoss_Point2=' + str(StopLoss_Point2))
            if LastPrice > StopLoss_Point2:  ## Price Up
                print('StopLoss_Point2.1=' + str(StopLoss_Point2))
                if StopLoss_Point <= BuyRate:
                    print("Update Stop Loss !! = 0")
                    Update_Stoppoint(UUID, Exchange, '0')

            if StopLoss_Point > BuyRate and StopLoss_Point > StopLoss_Point2:
                print('Update Stop Loss !! =' + str(StopLoss_Point))
                CK = Update_Stoppoint(UUID, Exchange, StopLoss_Point)
                if CK == "Ok":
                    print('Update_Stoppoint=' + str(StopLoss_Point))
            #if StopLoss_Point > BuyRate and LastPrice <= StopLoss_Point2:
            if LastPrice <= StopLoss_Point2:
                print("Sale Stop loss at " + str(LastPrice) + " !!!")
                print('Profit is ' + str(LastPrice - BuyRate))
                CK = Update_OrderBuy(UUID, Exchange, 'sell')
                print('Sale Status =>' + CK)
    elif LastPrice == BuyRate:
        Update_Stoppoint(UUID, Exchange, '0')
        StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))
    elif LastPrice < BuyRate:
        if BuyRate != "failed":
            CutLossPrice = (BuyRate - (BuyRate * (CutLoss / 100)))
            print('4.CutLossPrice=>' + str(CutLossPrice))
        if CutLossPrice >= LastPrice:
            print('Sale CutLoss at ' + str(CutLossPrice) + "!!!!")
            CK = Update_OrderBuy(UUID, Exchange, 'sell')
            print('Sell Status=' + CK)


def format_float(f):
    return "%.8f" % f


def symbols(id):
    exchange = getattr(ccxt, id)({
        # 'proxy':'https://cors-anywhere.herokuapp.com/',
    })

    # load all markets from the exchange
    markets = exchange.load_markets()

    # output a list of all market symbols
    dump(green(id), 'has', len(exchange.symbols), 'symbols:', exchange.symbols)
    tuples = list(ccxt.Exchange.keysort(markets).items())
    # output a table of all markets
    # dump(pink('{:<15} {:<15} {:<15} {:<15}'.format('id', 'symbol', 'base', 'quot')))
    #for (k, v) in tuples:
    # dump('{:<15} {:<15} {:<15} {:<15}'.format(v['id'], v['symbol'], v['base'], v['quote']))


def get_positive_accounts(balance):
    result = {}
    currencies = list(balance.keys())
    for currency in currencies:
        if balance[currency] and balance[currency] > 0:
            result[currency] = balance[currency]
    return result


def get_balance(id):
    ## GetBalance ##
    trading_balance = id.fetch_balance()
    account_balance = id.fetch_balance({'type': 'account'})
    pprint('Trading balance:')
    pprint(get_positive_accounts(trading_balance['total']))
    pprint('Account balance:')
    pprint(get_positive_accounts(account_balance['total']))


def main():
    try:
        print('Starting trader bot...')
        # bxin=ccxt.bxinth()
        bxin = ccxt.bxinth({
            'apiKey': '8cdf0f0a666c',
            'secret': 'b6b22e1e51eb',
            "enableRateLimit": True,
        })
        #print(ccxt.bxinth().fetch_ticker('DASH/THB'))
        #print(Get_OrderBuy(UUID, 'bxinth', 'buy'))
        #print(bxin.create_order('DASH/THB', 'THB', 'buy', 20, 2000,{'leverage': 3}))
        ST=bxin.fetch_order_book('BTC/THB')
        print(ST)

        
    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        raise
    # while True:
#    Exchange = 'Bittrex'
#    start = time.time()
#    for uuid in Get_BittrexOrder_UUID(Exchange):
#        print('UUID=>' + uuid[0])
#        cutloss(uuid[0], Exchange, 'USDT-BCC')
#        print('-----------------------')
#        end = time.time()
#        if end - start < TICK_INTERVAL:
#            time.sleep(TICK_INTERVAL - (end - start))

if __name__ == "__main__":
    main()

