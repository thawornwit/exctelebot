
from bittrex_tokens import * ## for accessing telegram api
import matplotlib  ## for ploting graph 
matplotlib.use("Agg") # has to be before any other matplotlibs imports to set a "headless" backend
import matplotlib.pyplot as plt ## create object plt for ploting graph 
import psutil ## for get utility system 
from datetime import datetime ## for datetime 
#import datetime
from subprocess import Popen, PIPE, STDOUT ## for 
import operator
import collections ## for put management collection 
import sys
import os
import time
import threading ## for management threading
import random
import telepot ## for interact with telegram 
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

#pdb.set_trace()
StopLoss_Point2=0
StopLoss_Point=0
TICK_INTERVAL = 30  # seconds
#API_KEY = 'a7e650878ca94b428f2bb43547793aa7'
#API_SECRET_KEY = b'bcfd8047a5f94d108714fc2d38092780'
Enable="OFF"

def main():
    print('Starting trader bot...')

    while True:
        start = time.time()
          #count=0 
        number = ''.join(random.sample("0123456789", 4))
        #print('Number of randome is '+number)
        Price = ''.join(random.sample("0123456789", 3))
        ## Insert Coin #### 
        UUID='a606d53c-8d70-'+str(number)+'-94b5-425861b8'+str(number)
        print(UUID)
        Insert_ckloss(UUID,5,5,0)
        Insert_OrderBuy(UUID,time.strftime('%Y-%m-%d %H:%M:%S'),'USDT-BCC',4,340.4,'buy')
        if end - start < TICK_INTERVAL:
           time.sleep(TICK_INTERVAL - (end - start))



def cutloss(UUID,coin_markets): 
    BuyRate=Get_BittrexOrder_buy(UUID,'order_buy','Rate')
    StopLoss=Get_BittrexDB(UUID,'ckloss','Stoploss')
    CutLoss=Get_BittrexDB(UUID,'ckloss','Cutloss')
    print("--------------------------")
    print('1.Start Bot cutloss ..')
    print('2.BuyRate=>'+str(BuyRate))
    print('2.StopLoss=>'+str(StopLoss))
    print('3.CutLoss=>'+str(CutLoss))
    LastPrice=Get_Bittrex_Price('USDT-BCC')
    print('LastPrice=>'+str(LastPrice))
    CutLossPrice=(BuyRate - (BuyRate * (CutLoss / 100)))
    print('4.CutLossPrice=>'+str(CutLossPrice))
    MinProfit=(BuyRate + (BuyRate * (CutLoss / 100)))
    print("Minimum Profit=>"+str(MinProfit))
    print("--------------------------")
       #market_summaries = simple_request('https://bittrex.com/api/v1.1/public/getmarketsummaries')
       #for summary in market_summaries['result']:
       #    market = summary['MarketName']
       #    day_close = summary['PrevDay']
       #    last = summary['Last']
       #    if day_close > 0:
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
          StopLoss_Point2=Get_BittrexDB(UUID,'ckloss','StoplossPoint')
          StopLoss_Point=LastPrice - (LastPrice * (StopLoss/100))
          print('StopLoss_Point1='+str(StopLoss_Point))
          print('StopLoss_Point2='+str(StopLoss_Point2))
          if LastPrice > StopLoss_Point2: ## Price Up
             print('StopLoss_Point2.1='+str(StopLoss_Point2))
             if StopLoss_Point <= BuyRate:
                print("Update Stop Loss !! = 0")
                Update_Stoppoint(UUID,'0')
                    
          if StopLoss_Point > BuyRate and StopLoss_Point > StopLoss_Point2:
             print('Update Stop Loss !! ='+str(StopLoss_Point))
             CK=Update_Stoppoint(UUID,StopLoss_Point) 
             if CK == "Ok":
                print('Update_Stoppoint='+str(StopLoss_Point))
          #if StopLoss_Point > BuyRate and LastPrice <= StopLoss_Point2:
          if LastPrice <= StopLoss_Point2:
             print("Sale Stop loss at "+str(LastPrice)+" !!!")
             print('Profit is '+str(LastPrice - BuyRate))
             CK=Update_OrderBuy(UUID,'sell')
             print('Sale Status =>'+CK)
    elif LastPrice == BuyRate: 
         Update_Stoppoint(UUID,'0')
         StopLoss_Point=LastPrice - (LastPrice * (StopLoss/100))
    elif LastPrice < BuyRate: 
         if BuyRate != "failed":
            CutLossPrice=(BuyRate - (BuyRate * (CutLoss / 100)))
            print('4.CutLossPrice=>'+str(CutLossPrice))
         if CutLossPrice >= LastPrice:
            print('Sale CutLoss at '+str(LastPrice)+"!!!!")
            CK=Update_OrderBuy(UUID,'sell')
            print('Sell Status='+CK)


def tick():
    print('Running routine')

    market_summaries = simple_request('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    for summary in market_summaries['result']:
        market = summary['MarketName']
        day_close = summary['PrevDay']
        last = summary['Last']
        if day_close > 0:
            percent_chg = ((last / day_close) - 1) * 100
        else:
            print('day_close zero for ' + market)
        if market == 'USDT-BCC':
           print(market + ' changed ' + str(percent_chg))
           print('### Balance ###')
           print('Last price:'+str(last))


    print('######### Check Balance BCC #########')
    print(get_balance('BCC'))
    print('######### Check Balance USDT ########')
    print(get_balance('USDT'))
    print('######### Check Market Summary #########')
    print(getmarket_summary('USDT-BCC'))
    print('######### Check Buy book USDT-BCC #########')
    print(getorder_avg_buybook('USDT-BCC'))
    print('######### Check Sale book USDT-BCC #########')
    print(getorder_avg_salebook('USDT-BCC'))
    print('######### Check history USDT-BCC #########')
    print(gethistory('USDT-BCC'))
    print('######### Check Open Order #########')
    print(get_open_orders('USDT-BCC')) 
          # for bl in BL['result']:
           #    print(str(bl['Currency']))
               #Balance=bl[0]
               #Currency=bl[1]
               #Available=bl[2]
               #Pending=bl[3]
               #print('Balance:'+str(Balance)+' Available:'+str(Available)+' Pending:'+str(Pending))
           
           #Sell Example ##
           ##print(sell_limit('USDT-BCC',float(0.1),float(500)))
          #Buy Limit
          # print(buy_limit('USDT-BCC',float(0.0001),float(100)))
   # for op in open['result']:
    #    Open=op['Opened']
    #    Exchg=op['Exchange']
    #    QC=op['Quantity']
    #    Limit=op['Limit']
    #    print('Open:'+Open+' Exchange='+Exchg+' Quantity='+str(QC)+' Limit='+str(Limit))

        #if 40 < percent_chg < 60:
            # Fomo strikes! Let's buy some
        #    if has_open_order(market, 'LIMIT_BUY'):
        #        print('Order already opened to buy 5 ' + market)
        #    else:
        #        print('Purchasing 5 units of ' + market + ' for ' + str(format_float(last)))
        #        res = buy_limit(market, 5, last)
        #        print(res)

        #if percent_chg < -20:
            # Do we have any to sell?
        #    balance_res = get_balance_from_market(market)
        #    current_balance = balance_res['result']['Available']

         #   if current_balance > 5:
                # Ship is sinking, get out!
         #       if has_open_order(market, 'LIMIT_SELL'):
         #           print('Order already opened to sell 5 ' + market)
         #       else:
         #           print('Selling 5 units of ' + market + ' for ' + str(format_float(last)))
         #           res = sell_limit(market, 5, last)
         #           print(res)
         #  else:
         #       print('Not enough ' + market + ' to open a sell order')


def buy_limit(market, quantity, rate):
    url = 'https://bittrex.com/api/v1.1/market/buylimit?apikey=' + API_KEY + '&market=' + market + '&quantity=' + str(quantity) + '&rate=' + format_float(rate)
    return signed_request(url)


def sell_limit(market, quantity, rate):
    url = 'https://bittrex.com/api/v1.1/market/selllimit?apikey=' + API_KEY + '&market=' + market + '&quantity=' + str(quantity) + '&rate=' + format_float(rate)
    return signed_request(url)


def get_balance_from_market(market_type):
    markets_res = simple_request('https://bittrex.com/api/v1.1/public/getmarkets')
    markets = markets_res['result']
    for market in markets:
        if market['MarketName'] == market_type:
            return get_balance(market['MarketCurrency'])

    # Return a fake response of 0 if not found
    return {'result': {'Available': 0}}


def getorder_avg_buybook(market):
    result=0
    count=0
    orderbuy_res=simple_request('https://bittrex.com/api/v1.1/public/getorderbook?market='+market+'&type=buy')
    orderbuy=orderbuy_res['result'] 
    for order in orderbuy:
        result+=order['Rate']
        count+=1
        if count == 10: 
           break 
    return(result/10)

def getorder_avg_salebook(market):
    result=0
    count=0
    ordersale_res=simple_request('https://bittrex.com/api/v1.1/public/getorderbook?market='+market+'&type=sell')
    ordersale=ordersale_res['result']
    for order in ordersale:
        result+=order['Rate']
        count+=1
        if count == 10:
           break
    return(result/10)


def gethistory(market): 
    orderhistory_res=simple_request('https://bittrex.com/api/v1.1/public/getmarkethistory?market='+market)
    orderhis=orderhistory_res['result']
    for history in orderhis: 
        print(str(history['Id'])+'|'+str(history['TimeStamp'])+'|'+str(history['Quantity'])+'|'+str(history['Price'])+'|'+str(history['Total'])+'|'+str(history['OrderType']))


def getmarket_summary(market):
     markets_res = simple_request('https://bittrex.com/api/v1.1/public/getmarketsummary?market='+market)
     markets = markets_res['result']
     return(markets)
     #for market_res in markets:
     #     return('TimeStamp:'+market_res['TimeStamp'])
     #     return('Hight:'+str(market_res['High']))
     #     return('Low:'+str(market_res['Low']))
     #     return('Volume:'+str(market_res['Volume']))
     #     return('Last:'+str(market_res['Last']))
     #     return('BaseVolume:'+str(market_res['BaseVolume']))
     #     return('Bid:'+str(market_res['Bid']))
     #     return('Ask:'+str(market_res['Ask']))
     #     return('OpenBuyOrders:'+str(market_res['OpenBuyOrders']))
     #     return('OpenSellOrders:'+str(market_res['OpenSellOrders']))

def get_balance(currency):
    url = 'https://bittrex.com/api/v1.1/account/getbalance?apikey=' + API_KEY + '&currency=' + currency
    res = signed_request(url)

    if res['result'] is not None and len(res['result']) > 0:
        return res

    # If there are no results, than your balance is 0
    return {'result': {'Available': 0}}


def get_open_orders(market):
    url = 'https://bittrex.com/api/v1.1/market/getopenorders?apikey=' + API_KEY + '&market=' + market
    res = signed_request(url)
    if res['result'] is not None and len(res['result']) > 0:
       return res


def has_open_order(market, order_type):
    orders_res = get_open_orders(market)
    orders = orders_res['result']

    if orders is None or len(orders) == 0:
        return False

    # Check all orders for a LIMIT_BUY
    for order in orders:
        if order['OrderType'] == order_type:
            return True

    return False


def signed_request(url):
    now = time.time()
    url += '&nonce=' + str(now)
    signed = hmac.new(API_SECRET_KEY, url.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'apisign': signed}
    r = requests.get(url, headers=headers)
    return r.json()


def simple_request(url):
    r = requests.get(url)
    return r.json()


def format_float(f):
    return "%.8f" % f


if __name__ == "__main__":
    main()

