__author__ = 'thawornwit'
from bittrex_tokens import *  ## for accessing telegram api
import matplotlib  ## for ploting graph
import os
import sys
import time
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
global number_point
number_point = 0
# pdb.set_trace()
StopLoss_Point2 = 0
StopLoss_Point = 0
TICK_INTERVAL = 5  # seconds
# API_KEY = 'a7e650878ca94b428f2bb43547793aa7'
# API_SECRET_KEY = b'bcfd8047a5f94d108714fc2d38092780'
Enable = "OFF"

def cal_stop_point(buy,p_point):
     StopPoint=[]
     num=0
     for point in p_point:
        Last_Stop=(buy + (buy * (point / 100)))
        buy=Last_Stop
        StopPoint.append(buy)

     return StopPoint
     #for price in StopPoint:
      #   num+=1
      #   print("P "+str(num)+" : "+str(format_float(price)))

## Order Sell ## Fine good price and sale for coin not buy such mining etc ..
def sell_trailling_stop_shadow(UUID, Exchange, LastPrice,BuyRate):
    #global number_point
    #BuyRate = Get_BittrexOrder_buy(UUID, Exchange, 'order_buy', 'Rate')
    StopLoss = Get_BittrexDB(UUID, Exchange, 'ckloss', 'Stoploss')
    CutLoss = Get_BittrexDB(UUID, Exchange, 'ckloss', 'Cutloss')
    print("--------------------------")
    print('Start Bot Cutloss CTS..')
    print('1.StartRate=>' + str(BuyRate))
    print('2.StopLoss=>' + str(StopLoss))
    print('3.CutLoss=>' + str(CutLoss))
    # LastPrice = Get_Bittrex_Price(Coin, Exchange)  ## Sim for Tesss
    # LastPrice = get_lastprice(Exchange)
    print('LastPrice=>' + str(LastPrice))
    CutLossPrice = (BuyRate - (BuyRate * (CutLoss / 100)))
    print('4.CutLossPrice=>' + str(CutLossPrice))
    MinProfit = (BuyRate + (BuyRate * (StopLoss / 100)))
    print("Minimum Profit=>" + str(MinProfit))
    print("Start Cost =>" + str(BuyRate) + " Price Up =>" + str(LastPrice - BuyRate) + " (+/-) =>" + str(
        (100 * (LastPrice - BuyRate)) / BuyRate) + "%")
    print("--------------------------")
    ## Price UP ##
    if LastPrice > BuyRate:
        if StopLoss != "" or StopLoss != 0:
            StopLoss_Point_bf = Get_BittrexDB(UUID, Exchange, 'ckloss', 'StoplossPoint') ## Stop loss before
            StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))  ## current stop loss
            print('StopLoss_Point=' + str(StopLoss_Point))
            print('StopLoss_Point_Action=' + str(StopLoss_Point_bf))
            if LastPrice > StopLoss_Point_bf:  ## Price Up
                #print('StopLoss_Point2=' + str(StopLoss_Point_bf))
                if StopLoss_Point <= BuyRate:
                    print("Stop loss less than buyer update Stop Loss = 0")
                    Update_Stoppoint(UUID, Exchange, '0')
                    #return ('StopLossUpdate',0)

                if StopLoss_Point > BuyRate and StopLoss_Point > StopLoss_Point_bf:
                    print('Update Stop Loss !! =' + str(StopLoss_Point) +" to new value")
                    CK = Update_Stoppoint(UUID, Exchange, StopLoss_Point)
                    if CK == "OK":
                        print('Update_Stoppoint=' + str(StopLoss_Point) +" => Completed")
                        StopLoss_Point_bf = StopLoss_Point
                        #number_point+=1
                        return ('StopLossUpdate',StopLoss_Point_bf,StopLoss)
                elif StopLoss_Point > BuyRate and StopLoss_Point <= StopLoss_Point_bf:
                    print("Wait Price less than Last Stop Point Action")
                    print("Stop Point Action is "+str(StopLoss_Point_bf))
                    #return ('StopLoss Action Update', StopLoss_Point_bf)
            # if StopLoss_Point > BuyRate and LastPrice <= StopLoss_Point2:
            if LastPrice <= StopLoss_Point_bf:
                print("Sale coin because last price less than stop point => "+str(StopLoss_Point_bf)+"")
                return ('StopLoss', LastPrice,StopLoss)
    elif LastPrice == BuyRate:
        Update_Stoppoint(UUID, Exchange, '0')
        StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))
    elif LastPrice < BuyRate:
        if BuyRate != "failed":
            CutLossPrice = (BuyRate - (BuyRate * (CutLoss / 100)))
            print('CutLossPrice to Price =>' + str(CutLossPrice))
        if CutLossPrice >= LastPrice:
            return ('CutLoss', CutLossPrice,CutLoss)  ## Order  ##

## Order Buy ## Find good price and sale ,buy and find price up
def buy_trailling_stop_shadow(UUID, Exchange, LastPrice,BuyRate):
    #global number_point
    #BuyRate = Get_BittrexOrder_buy(UUID, Exchange, 'order_buy', 'Rate')
    StopLoss = Get_BittrexDB(UUID, Exchange, 'ckloss', 'Stoploss')
    CutLoss = Get_BittrexDB(UUID, Exchange, 'ckloss', 'Cutloss')
    print("--------------------------")
    print('1.Start Bot cutloss BTS ..')
    print('2.BuyRate=>' + str(BuyRate))
    print('2.StopLoss=>' + str(StopLoss))
    print('3.CutLoss=>' + str(CutLoss))
    # LastPrice = Get_Bittrex_Price(Coin, Exchange)  ## Sim for Tesss
    # LastPrice = get_lastprice(Exchange)
    print('LastPrice=>' + str(LastPrice))
    CutLossPrice = (BuyRate - (BuyRate * (CutLoss / 100)))
    print('4.CutLossPrice=>' + str(CutLossPrice))
    MinProfit = (BuyRate + (BuyRate * (StopLoss / 100)))
    print("Minimum Profit=>" + str(MinProfit))
    print("Buy Cost =>" + str(BuyRate) + " Price Up =>" + str(LastPrice - BuyRate) + " (+/-) =>" + str(
        (100 * (LastPrice - BuyRate)) / BuyRate) + "%")
    print("--------------------------")
    ## Price UP ##
    if LastPrice > BuyRate:
        if StopLoss != "" or StopLoss != 0:
            StopLoss_Point_bf = Get_BittrexDB(UUID, Exchange, 'ckloss', 'StoplossPoint') ## Stop loss before
            StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))  ## current stop loss
            print('StopLoss_Point=' + str(StopLoss_Point))
            print('StopLoss_Point_Action=' + str(StopLoss_Point_bf))
            if LastPrice > StopLoss_Point_bf:  ## Price Up
                #print('StopLoss_Point2=' + str(StopLoss_Point_bf))
                if StopLoss_Point <= BuyRate:
                    print("Stop loss less than buyer update Stop Loss = 0")
                    Update_Stoppoint(UUID, Exchange, '0')
                    #return ('StopLossUpdate',0)

                if StopLoss_Point > BuyRate and StopLoss_Point > StopLoss_Point_bf:
                    print('Update Stop Loss !! =' + str(StopLoss_Point) +" to new value")
                    CK = Update_Stoppoint(UUID, Exchange, StopLoss_Point)
                    if CK == "OK":
                        print('Update_Stoppoint=' + str(StopLoss_Point) +" => Completed")
                        StopLoss_Point_bf = StopLoss_Point
                        #number_point+=1
                        return ('StopLossUpdate',StopLoss_Point_bf,StopLoss)
                elif StopLoss_Point > BuyRate and StopLoss_Point <= StopLoss_Point_bf:
                    print("Wait Price less than Last Stop Point Action")
                    print("Stop Point Action is "+str(StopLoss_Point_bf))
                    #return ('StopLoss Action Update', StopLoss_Point_bf)
            # if StopLoss_Point > BuyRate and LastPrice <= StopLoss_Point2:
            if LastPrice <= StopLoss_Point_bf:
                print("Sale coin because last price less than stop point => "+str(StopLoss_Point_bf)+"")
                return ('StopLoss', LastPrice,StopLoss)
    elif LastPrice == BuyRate:
        Update_Stoppoint(UUID, Exchange, '0')
        StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))
    elif LastPrice < BuyRate:
        if BuyRate != "failed":
            CutLossPrice = (BuyRate - (BuyRate * (CutLoss / 100)))
            print('CutLossPrice to Price =>' + str(CutLossPrice))
        if CutLossPrice >= LastPrice:
            return ('CutLoss', CutLossPrice,CutLoss)

## Find price deep dows ## Find proce low and Buy
def buy_StopBuy_shadow(UUID, Exchange, LastPrice,StartRate):
    StopRisk = Get_BittrexDB(UUID, Exchange, 'ckstopbuy', 'StopRisk')
    StopBuy = Get_BittrexDB(UUID, Exchange, 'ckstopbuy', 'StopBuy')
    print("--------------------------")
    print('Start Bot StopBuy STB ..')
    print('1.StartRate=>' + str(StartRate))
    print('2.StopRisk(UP)=>' + str(StopRisk))
    print('3.StopBuy(DOWN)=>' + str(StopBuy))
    print('4.LastPrice=>' + str(LastPrice))
    StopRiskPrice = (StartRate + (StartRate * (StopRisk / 100)))
    print('5.StopRisk=>' + str(StopRiskPrice))
    print("StartRate =>" + str(StartRate) + " Price Down =>" + str(LastPrice - StartRate) + " (+/-) =>" + str((100 * (LastPrice - StartRate)) / StartRate) + "%")
    print("--------------------------")
    ## Price DOWN ##
    if LastPrice < StartRate:
        if StopBuy != "" or StopBuy != 0:
            StopBuy_Point_bf = Get_BittrexDB(UUID, Exchange, 'ckstopbuy', 'StopBuyPoint') ## Stop loss before
            if StopBuy_Point_bf == 0:
               StopBuy_Point_bf = 1000000

            StopBuy_Point = LastPrice + (LastPrice * (StopBuy / 100))  ## current cutloss
            print('StopBuy_Point=' + str(StopBuy_Point))
            print('StopBuy_Point_Action=' + str(StopBuy_Point_bf))
            if LastPrice < StopBuy_Point_bf:  ## Price is Down
                #print('StopLoss_Point2=' + str(StopLoss_Point_bf))
                if StopBuy_Point >= StartRate:
                    print("StopBuy Up than buyer update StopBuy = 0")
                    Update_StopBuyPoint(UUID, Exchange, '0')
                    #return ('StopLossUpdate',0)

                if StopBuy_Point < StartRate and StopBuy_Point < StopBuy_Point_bf:
                    print('Update StopBuy !! =' + str(StopBuy_Point) +" to new value")
                    CK = Update_StopBuyPoint(UUID, Exchange, StopBuy_Point)
                    if CK == "OK":
                        print('Update Price Down to new point=' + str(StopBuy_Point) +" => Completed")
                        StopBuy_Point_bf = StopBuy_Point
                        #number_point+=1
                        return ('StopBuyUpdate',StopBuy_Point_bf,StopBuy)
                elif StopBuy_Point < StartRate and StopBuy_Point >= StopBuy_Point_bf:
                    print("Wait Price Up than Last StopBuy Point Action")
                    print("StopBuy Point Action is "+str(StopBuy_Point_bf))
                    #return ('StopLoss Action Update', StopLoss_Point_bf)
            # if StopLoss_Point > BuyRate and LastPrice <= StopLoss_Point2:
            if LastPrice >= StopBuy_Point_bf:
                print("Buy coin because last price up than Stop Buy Point => "+str(StopBuy_Point_bf)+"")
                return ('StopBuy', LastPrice,StopBuy)  ### Stop and Buy coin Now !!!
    elif LastPrice == StartRate:
        Update_StopBuyPoint(UUID, Exchange, '0')
        CutLoss_Point = LastPrice - (LastPrice * (StopBuy / 100))
    elif LastPrice > StartRate:
        if StartRate != "failed":
            StopLossPrice = (StartRate + (StartRate * (StopRisk / 100)))
            print('StopRisk Price =>' + str(StopLossPrice))
        if StopLossPrice <= LastPrice:
            return ('StopRisk', StopLossPrice,StopRisk)   ### StopRisk becuase price is up



def buy_trailling_stop_custom_sim(UUID, Exchange, LastPrice,StopPoint):
    BuyRate = Get_BittrexOrder_buy(UUID, Exchange, 'order_buy', 'Rate')
    StopLoss = Get_BittrexDB(UUID, Exchange, 'ckloss', 'Stoploss')
    CutLoss = Get_BittrexDB(UUID, Exchange, 'ckloss', 'Cutloss')
    print("--------------------------")
    print('1.Start Bot cutloss ..')
    print('2.BuyRate=>' + str(BuyRate))
    print('2.StopLoss=>' + str(StopLoss))
    print('3.CutLoss=>' + str(CutLoss))
    # LastPrice = Get_Bittrex_Price(Coin, Exchange)  ## Sim for Tesss
    # LastPrice = get_lastprice(Exchange)
    print('LastPrice=>' + str(LastPrice))
    CutLossPrice = (BuyRate - (BuyRate * (CutLoss / 100)))
    print('4.CutLossPrice=>' + str(CutLossPrice))
    MinProfit = (BuyRate + (BuyRate * (StopLoss / 100)))
    print("Minimum Profit=>" + str(MinProfit))
    print("Buy Cost =>" + str(BuyRate) + " Price Up =>" + str(LastPrice - BuyRate) + " (+/-) =>" + str(
        (100 * (LastPrice - BuyRate)) / BuyRate) + "%")
    print("--------------------------")
    ## Price UP ##
    if LastPrice > BuyRate:
        if StopLoss != "" or StopLoss != 0:
            StopLoss_Point_bf = Get_BittrexDB(UUID, Exchange, 'ckloss', 'StoplossPoint') ## Stop loss before
            StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))  ## current stop loss
            print('StopLoss_Point=' + str(StopLoss_Point))
            print('StopLoss_Point_Action=' + str(StopLoss_Point_bf))
            if LastPrice > StopLoss_Point_bf:  ## Price Up
                #print('StopLoss_Point2=' + str(StopLoss_Point_bf))
                if StopLoss_Point <= BuyRate:
                    print("Stop loss less than buyer update Stop Loss = 0")
                    Update_Stoppoint(UUID, Exchange, '0')

                if StopLoss_Point > BuyRate and StopLoss_Point > StopLoss_Point_bf:
                    print('Update Stop Loss !! =' + str(StopLoss_Point) +" to new value")
                    CK = Update_Stoppoint(UUID, Exchange, StopLoss_Point)
                    if CK == "OK":
                        print('Update_Stoppoint=' + str(StopLoss_Point) +" => Completed")
                        StopLoss_Point_bf = StopLoss_Point
                elif StopLoss_Point > BuyRate and StopLoss_Point <= StopLoss_Point_bf:
                    print("Wait Price less than Last Stop Point Action")
                    print("Stop Point Action is"+str(StopLoss_Point_bf))
            # if StopLoss_Point > BuyRate and LastPrice <= StopLoss_Point2:
            if LastPrice <= StopLoss_Point_bf:
                print("Sale coin because last price less than stop point => "+str(StopLoss_Point_bf)+"")
                return ('StopLoss', LastPrice)
    elif LastPrice == BuyRate:
        Update_Stoppoint(UUID, Exchange, '0')
        StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))
    elif LastPrice < BuyRate:
        if BuyRate != "failed":
            CutLossPrice = (BuyRate - (BuyRate * (CutLoss / 100)))
            print('CutLossPrice to Price =>' + str(CutLossPrice))
        if CutLossPrice >= LastPrice:
            return ('CutLoss', CutLossPrice)



def format_float(f):
    return "%.5f" % f

def format_floatc(f,num):
    format="%."+str(num)+"f"
    return format % f
                     #% f


def symbols(id):
    exchange = getattr(ccxt, id)({
        # 'proxy':'https://cors-anywhere.herokuapp.com/',
    })

    # load all markets from the exchange
    markets = exchange.load_markets()

    # output a list of all market symbols
    for symbol in exchange.symbols:
        print(symbol)
        # tuples = list(ccxt.Exchange.keysort(markets).items())
        # print(tuples)
        # output a table of all markets
        # dump(pink('{:<15} {:<15} {:<15} {:<15}'.format('id', 'symbol', 'base', 'quot')))
        # for (k, v) in tuples:
        # dump('{:<15} {:<15} {:<15} {:<15}'.format(v['id'], v['symbol'], v['base'], v['quote']))


def get_positive_accounts(balance):
    result = {}
    currencies = list(balance.keys())
    for currency in currencies:
        if balance[currency] and balance[currency] > 0:
            result[currency] = balance[currency]
    return result

def Update_Balance_Exc(Exchange,Coin,Market,Qty,Type,SB,ChatID):
        INFO = ""
        total = 0
        Coin = check_sys("data=" + Coin + ";echo ${data%/*}")
        CK = Get_CoinBlance(Exchange, Coin, str(ChatID))
        if CK != "Failed":
            for bl in list(CK):
                coin = str(bl[2])
                total = format_floatc(bl[3], 5)
                used = format_floatc(bl[4], 5)
                free = format_floatc(bl[5], 5)
                INFO += ("\n|-- Coin Balance " + coin + "--|\
                        \nTotal:" +str(total) + "\
                        \nUsed:" +str(used) + "\
                        \nFree:" +str(free) + "\
                        \n----------------")
                if Type == "buy" and SB == "O":
                    print("Action to Buy !!!+>"+coin)
                    if coin == Market and float(Qty) > 0.0: ## Check market
                        Total=format_floatc((float(total) - float(Qty)),4)
                        Free=format_floatc((float(free) - float(Qty)),4)
                        Used=format_floatc((float(used) + float(Qty)),4)
                        #if float(Total) < 0 :
                        #    return (False,"Minimum balance less than 10 Bath !!")
                        #else:
                        CK=Update_CoinBlance(Exchange,Coin,Total,Used,Free,str(ChatID))
                        print("Update Data Buy => "+CK)
                    else:
                        continue
                elif Type == "buy" and SB == "C":
                    print("Action to Buy !!!+>" + coin)
                    if coin == Market and float(Qty) > 0.0:  ## Check market
                        Total = format_floatc((float(total) + float(Qty)), 4)
                        Free = format_floatc((float(free) + float(Qty)), 4)
                        Used = format_floatc((float(used) - float(Qty)), 4)
                        ### Restore Update  coin
                        CK = Update_CoinBlance(Exchange, Coin, Total, Used, Free, str(ChatID))
                        if CK == "OK":
                            print("Update  Close Balance  !! => " + CK)
                        else:
                            print("Update  Close Balance !! => " + CK)
                    else:
                        continue

                        ################
                if Type == "sell" and SB == "O":
                    print("Action to Sell !!!")
                    if coin == Coin and float(Qty) > 0.0:  ## Check market
                        Total = format_floatc((float(total) - float(Qty)), 4)
                        Free = format_floatc((float(free) - float(Qty)), 4)
                        Used = format_floatc((float(used) + float(Qty)), 4)
                        #if float(Total) < 0.0010:
                        #    return (False,"Minimum coin balance is not available,please verify  !!")
                        #else:
                        CK = Update_CoinBlance(Exchange, Coin, Total, Used, Free,str(ChatID))
                    else:
                        continue
                if Type == "sell" and SB == "C":
                    print("Action to Sell !!!")
                    if coin == Coin and float(Qty) > 0.0:  ## Check market
                        Total = format_floatc((float(total) + float(Qty)), 4)
                        Free = format_floatc((float(free) + float(Qty)), 4)
                        Used = format_floatc((float(used) - float(Qty)), 4)
                        ## Restore Update coin ##
                        CK = Update_CoinBlance(Exchange, Coin, Total, Used, Free, str(ChatID))
                        if CK == "OK":
                            print("Update  Close Balance !! => " + CK)
                        else:
                            print("Update  Close Balance !! => " + CK)
                    else:
                        continue

            if  str(CK) == "OK":
                INFO+="\n-------------\
                \n|= Update Balance =|\
                \nCoin: "+Coin+"\
                \nTotal:"+str(Total)+"\
                \nFree:"+str(Free)+"\
                \nUsed:"+str(Used)+""
                print(INFO)
                return (True,INFO)
        else:
            return (False,"Can't Get database for update balance !!")

def get_balance(Exchange,Coin,ChatID):
    INFO=""
    total=0
    Coin = check_sys("data=" + Coin + ";echo ${data%/*}")
    CK = Get_CoinBlance(Exchange,Coin, str(ChatID))
    if CK != "Failed":
        for bl in list(CK):
            coin = str(bl[2])
            total = format_floatc(bl[3], 5)
            used = format_floatc(bl[4], 5)
            free = format_floatc(bl[5], 5)
            INFO=("\n|-- Blance " + coin +"--|\
                    \n  Total:" + total + "\
                    \n  Used:" + used + "\
                    \n  Free:" + free + "\
                    \n----------------")
        if float(total) > 0:
            return INFO
        elif float(total) <= 0:
            return False
    else:
        return False

def get_balance_bx(id, coin):
    ## GetBalance ##
    try:
        CK = 1
        Bal = ""
        coin = check_sys("data=" + coin + ";echo ${data%/*}")
    # trading_balance = id.fetch_balance()
        account_balance = id.fetch_balance({'type': 'account'})
        for bal in (get_positive_accounts(account_balance['total'])):
            if bal == coin:
                Bal += (bal + ":" + str(format_floatc(account_balance['total'][bal],6)) + "\n")
                Bal += ("Used:" + str(format_floatc(account_balance['used'][bal],6)) + "\n")
                Bal += ("Free:" + str(format_floatc(account_balance['free'][bal],6)) + "\n")
                Bal+="----------------\n"
                CK = 0
        if CK == 0:
            return str(Bal)
        else:
            return 201
    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')

##############################
def sale_coin_sim(symbol, volumn, price):
        number = ''.join(random.sample("0123456789", 8))
        print('Number of randome is ' + number)
    ## Insert Coin ####
        UUID =str(number)
        print(UUID)
        Result = {'info': {'order_id':UUID, 'error': None, 'success': True}, 'id':UUID}
        print(Result)
        if Result['info']['success'] == True:
            print("Sale " + symbol + " ID:" + str(Result['info']['order_id']) + " Price:" + str( \
                price) + "Bath  Qty:" + str( \
                volumn) + " Total:" + str(format_float(volumn * price)) + " Bath")
            Oid = Result['info']['order_id']
            if Oid == 0:
                number = ''.join(random.sample("0123456789", 7))
                Oid = number
            if Oid != 0 and Oid != None:
                #Total = volumn * price
                #ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), str(symbol), 'sell', price,volumn, Total,
                #                      'open', exchange)
                #if ST == "OK":
                return Oid
                #else:
                #    return "Error,Insert Database open order failed"
            else:
                return Result['info']['error']
        else:
            return (str("Sale " + symbol + " Failed error is" + Result['info']['error']))

def sale_coin_res(symbol, volumn, price, exchange):
    number = ''.join(random.sample("0123456789", 8))
    print('Number of randome is ' + number)
    ## Insert Coin ####
    UUID = str(number)
    print(UUID)
    Result = {'info': {'order_id': UUID, 'error': None, 'success': True}, 'id': UUID}
    print(Result)
    print("Start Reserve Order Sell")
    if Result['info']['success'] == True:
        print("Sale " + symbol + " ID:" + str(Result['info']['order_id']) + " Price:" + str( \
            price) + "Bath  Qty:" + str( \
            volumn) + " Total:" + str(format_float(volumn * price)) + " Bath")
        Oid = Result['info']['order_id']
        if Oid == 0:
            number = ''.join(random.sample("0123456789", 7))
            Oid = number
        if Oid != 0 and Oid != None:
            Total = volumn * price
            ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), str(symbol), 'sell', price, volumn, Total,
                                  'open', exchange,'sts')
            if ST == "OK":
                return Oid
            else:
                return "Error,Insert Database open order failed"
        else:
            return Result['info']['error']
    else:
        return (str("Sale " + symbol + " Failed error is" + Result['info']['error']))
##############################
def sale_coin(id, symbol,volumn, price):
    try:
        ## Fortest ##
        #Result=True
        Result = id.create_order(symbol, 'market', 'sell', volumn, price, {'leverage': 3})
        print(Result)
        if Result['info']['success'] == True:
            print("Sale " + symbol + " ID:" + str(Result['info']['order_id']) + " Price:" + str( \
                price) + "Bath  Qty:" + str( \
                volumn) + " Total:" + str(format_float(volumn * price)) + " Bath")
            Oid = Result['info']['order_id']
            if Oid == 0:
                number = ''.join(random.sample("0123456789", 7))
                Oid = number
            if Oid != 0 and Oid != None:
                #Total = volumn
                #Qty = volumn * price
                #ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), str(symbol), 'sell', price, volumn, Total,
                #                      'open', exchange)
                #if ST == "OK":
                return Oid
                #else:
                #    return "Error,Insert Database open order failed"
            else:
                return Result['info']['error']
        else:
            return (str("Sale " + symbol + " Failed error is" + Result['info']['error']))
            # return 1

    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')

####### BSS Only
def buy_coin_bss_sim(symbol, volumn, price):
        number = ''.join(random.sample("0123456789", 8))
        print('Number of randome is ' + number)
        ## Insert Coin ####
        UUID = str(number)
        print(UUID)
        Result = {'info': {'order_id': UUID, 'error': None, 'success': True}, 'id': UUID}
        print(Result)
        if Result['info']['success'] == True:
            print("Buy " + symbol + " ID:" + str(Result['info']['order_id']) + "Price:" + str(\
            price) + " Volumn:" + str(volumn) + " Quality:" + str(volumn / price))
            Oid = Result['info']['order_id']
            if Oid == 0:
                number = ''.join(random.sample("0123456789", 7))
                Oid = number
            if Oid != 0 and Oid != None:
               return Oid
        else:
            return (str("Buy " + symbol + " Failed error is" + Result['info']['error']))
                # return 1

def buy_coin_bss(id, symbol, volumn, price):
    try:
        Result = id.create_order(symbol, 'market', 'buy', volumn, price, {'leverage': 3})
        print(Result)
        if Result['info']['success'] == True:
            print("Buy " + symbol + " ID:" + str(Result['info']['order_id']) + "Price:" + str(price) + " Volumn:" + str(
                volumn) + " Quality:" + str(volumn / price))
            Oid = Result['info']['order_id']
            if Oid == 0:
                number = ''.join(random.sample("0123456789", 7))
                Oid = number
            if Oid != 0 and Oid != None:
                return Oid
            else:
                return Result['info']['error']

        else:
            return (str("Buy " + symbol + " Failed error is" + Result['info']['error']))
            # return 1


    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')

def buy_coin_res(symbol, volumn, price, exchange):
    number = ''.join(random.sample("0123456789", 8))
    print('Number of randome is ' + number)
    ## Insert Coin ####
    UUID = str(number)
    print(UUID)
    Result = {'info': {'order_id': UUID, 'error': None, 'success': True}, 'id': UUID}
    print(Result)
    if Result['info']['success'] == True:
        print("Buy " + symbol + " ID:" + str(Result['info']['order_id']) + "Price:" + str(price) + " Volumn:" + str(
            volumn) + " Quality:" + str(volumn / price))
        Oid = Result['info']['order_id']
        if Oid == 0:
            number = ''.join(random.sample("0123456789", 7))
            Oid = number
        if Oid != 0 and Oid != None:
            Total = volumn
            Qty = volumn / price
            ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), symbol, 'buy', price, Qty, Total, 'open',
                                  exchange,'bss')
            if ST == "OK":
                return Oid
            else:
                return "Error,Insert Database open order failed"
        else:
            return Result['info']['error']

    else:
        return (str("Buy " + symbol + " Failed error is" + Result['info']['error']))
        # return 1


### BTS Only ###
def buy_coin_sim(symbol, volumn, price, exchange):
    number = ''.join(random.sample("0123456789", 8))
    print('Number of randome is ' + number)
    ## Insert Coin ####
    UUID = str(number)
    print(UUID)
    Result = {'info': {'order_id': UUID, 'error': None, 'success': True}, 'id': UUID}
    print(Result)
    if Result['info']['success'] == True:
        print("Buy " + symbol + " ID:" + str(Result['info']['order_id']) + "Price:" + str(price) + " Volumn:" + str(
            volumn) + " Quality:" + str(volumn / price))
        Oid = Result['info']['order_id']
        if Oid == 0:
            number = ''.join(random.sample("0123456789", 7))
            Oid = number
        if Oid != 0 and Oid != None:
            Total = volumn
            Qty = volumn / price
            ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), symbol, 'buy', price, Qty, Total, 'open',
                                  exchange, 'bts')
            if ST == "OK":
                return Oid
            else:
                return "Error,Insert Database open order failed"
        else:
            return Result['info']['error']

    else:
        return (str("Buy " + symbol + " Failed error is" + Result['info']['error']))
        # return 1

def buy_coin(id, symbol, volumn, price, exchange):
    try:
        Result = id.create_order(symbol, 'market', 'buy', volumn, price, {'leverage': 3})
        print(Result)
        if Result['info']['success'] == True:
            print("Buy " + symbol + " ID:" + str(Result['info']['order_id']) + "Price:" + str(price) + " Volumn:" + str(
                volumn) + " Quality:" + str(volumn / price))
            Oid = Result['info']['order_id']
            if Oid == 0:
                number = ''.join(random.sample("0123456789", 7))
                Oid = number
            if Oid != 0 and Oid != None:
                Total = volumn
                Qty = volumn / price
                ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), symbol, 'buy', price, Qty, Total, 'open',
                                      exchange,'bts')
                if ST == "OK":
                    return Oid
                else:
                    return "Error,Insert Database open order failed"
            else:
                return Result['info']['error']

        else:
            return (str("Buy " + symbol + " Failed error is" + Result['info']['error']))
            # return 1


    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')

######################
def cancel_coin_sim(order_id, symbol, exchange):
    if order_id != 0 and order_id != None:
       Result = True
       if Result['success'] == True:
          print("Cancel " + symbol + " Oerder ID:" + order_id + " -> Completed")
          Update_OpenOrder(order_id, exchange, 'close')
          return True
####################

def cancel_coin(id, order_id, symbol, exchange):
    try:
        if order_id != 0 and order_id != None:
            Result = id.cancel_order(order_id, symbol)
            if Result['success'] == True:
                print("Cancel " + symbol + " Oerder ID:" + order_id + " -> Completed")
                Update_OpenOrder(order_id, exchange, 'close')
                return True
            else:
                return (str("Cancel " + symbol + " Failed error is" + Result['info']['error']))
                # return 1
    except ccxt.DDoSProtection as e:
        # print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        # print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        # print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        # print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')


def get_coin_information(id, symbol):
    try:
        INFO = "|== Coin Information ==| \n"
        info = (id.fetch_ticker(symbol))
        INFO += str("Coin:" + symbol + "\n")
        INFO += str("Change:" + str(info['info']['change']) + "\n")
        INFO += str("LastPrice:" + str(info['info']['last_price']) + "\n")
        for infom in (info['info']):
            if infom == "orderbook":
                for order in info['info'][infom]:
                    if order == "asks":
                        INFO += "|- Asks -| \n"
                        for data in (info['info']['orderbook']['asks']):
                            INFO += str(data + ":" + str(info['info']['orderbook']['asks'][data]) + "\n")
                    if order == "bids":
                        INFO += "|- Bids -| \n"
                        for data in (info['info']['orderbook']['bids']):
                            INFO += str(data + ":" + str(info['info']['orderbook']['bids'][data]) + "\n")
                continue
        ST = id.fetch_order_book(symbol)
        count = 0
        INFO += ("|-- Last Order --|\n")
        INFO+=("|- Bids -| \n")
        for data in ST['bids']:
            INFO += (str(format_float(data[0])) + "|" + str(data[1]) + "\n")
            count += 1
            if count == 5:
                break
        count = 0
        INFO += ("|- Asks -|\n")
        for data in ST['asks']:
            INFO += (str(format_float(data[0])) + "|" + str(data[1]) + "\n")
            count += 1
            if count == 5:
                break

        #print(INFO)
        return INFO

    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        print(type(e).__name__, e.args, )


#######################
def get_lastprice_sim(symbol,exchange):
    Price=Get_Bittrex_Price(symbol, exchange)  ## Sim for Tesss
    return Price

#######################
def get_lastprice(id, symbol):
    try:
        Price = (id.fetch_ticker(symbol))
        return (Price['last'])

    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        print(type(e).__name__, e.args, )


def get_openorder(exchange, Type, coin):
    ST = Get_BittrexOpen_Order(exchange, Type, coin)
    for order in list(ST):
        time = (order[2])
        order_id = (order[1])
        coin = (order[3])
        rate = (order[5])
        qty = (order[6])
        total = (order[7])
        return str(
            "" + time + "\nO:/" + order_id + "\nC:" + coin + "\nR:" + str(rate) + "\nQ:" + str(qty) + "\nT:" + str(
                total))


# def apply_trailing_stop(lastprice):

def ck_close_order_sim(order_id, symbol, Type, exchange):
    lastprice = get_lastprice_sim(symbol,exchange)
    if lastprice == "failed":
        print("!!! Can't get lastprice ")
        return False
    print("Current Lasprice sim " + str(lastprice))
    # lastprice=get_lastprice(id,symbol)
    if Type == 'sell' and order_id != 0 and order_id != None:
        OpenRate = Get_Rate_OpenOrder(order_id, exchange, symbol, Type)
        print("Open Rate:" + str(OpenRate))
        if is_number(OpenRate) == True:
            if lastprice >= OpenRate:
                ST = Update_OpenOrder(order_id, exchange, 'close')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to closed")
                    return True
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    return False
    if Type == 'buy' and order_id != 0 and order_id != None:
        OpenRate = Get_Rate_OpenOrder(order_id, exchange, symbol, Type)
        print("Open Rate:" + str(OpenRate))
        if is_number(OpenRate) == True:
            if lastprice <= OpenRate:
                ST = Update_OpenOrder(order_id, exchange, 'close')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to closed")
                    return True
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    return False
    if Type == 'cancle' and order_id != 0 and order_id != None:
        ST = Update_OpenOrder(order_id, exchange, 'close')
        if ST == "OK":
            print("Update Open Order " + order_id + " to cancel")
            return True
        else:
            print("Update Open Order " + order_id + " failed")
            return False



def ck_close_order(id, order_id, symbol, Type, exchange):
    lastprice = get_lastprice(id, symbol)
    if lastprice == "failed":
        print("!!! Can't get lastprice ")
        return False
    print("Current Lasprice " + str(lastprice))
    # lastprice=get_lastprice(id,symbol)
    if Type == 'sell' and order_id != 0 and order_id != None:
        OpenRate = Get_Rate_OpenOrder(order_id, exchange, symbol, Type)
        print("Open Rate:" + str(OpenRate))
        if is_number(OpenRate) == True:
            if lastprice >= OpenRate:
                ST = Update_OpenOrder(order_id, exchange, 'close')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to closed")
                    return True
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    return False
    if Type == 'buy' and order_id != 0 and order_id != None:
        OpenRate = Get_Rate_OpenOrder(order_id, exchange, symbol, Type)
        print("Open Rate:" + str(OpenRate))
        if is_number(OpenRate) == True:
            if lastprice <= OpenRate:
                ST = Update_OpenOrder(order_id, exchange, 'close')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to closed")
                    return True
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    return False
    if Type == 'cancle' and order_id != 0 and order_id != None:
        ST = Update_OpenOrder(order_id, exchange, 'cancel')
        if ST == "OK":
            print("Update Open Order " + order_id + " to cancel")
            return True
        else:
            print("Update Open Order " + order_id + " failed")
            return False

def sync_balance_coin(id,Exchange,Coin,ChatID):
    try:
        INFO=""
        account_balance = id.fetch_balance({'type': 'account'})
        for coin in ((account_balance['total'])):
            Total=(str(format_floatc(account_balance['total'][coin], 6)))
            Used=(str(format_floatc(account_balance['used'][coin], 6)))
            Free=(str(format_floatc(account_balance['free'][coin], 6)))
            #-----------------------------------
            CK = Get_CoinBlance(Exchange,coin,ChatID)
            if str(CK) == "()" and coin == Coin:
                if Total != "" and Used != "" and Free != "":
                    CK=Insert_CoinBlance(Exchange,coin,Total,Used,Free,ChatID)
                    if str(CK) == "OK":
                        INFO+=("|--Sync Update New --|\
                        \nUser:" + str(ChatID) + "\
                        \nCoin:" + str(coin) + "\
                        \nTotal:" + str(Total) + "\
                        \nUsed:" + str(Used) + "\
                        \nFree:" + str(Free))
                        continue
                    else:
                        return("Sync Update database --> Failed")
            elif str(CK) != "()" and coin == Coin:
                CK=Update_CoinBlance(Exchange,coin,Total,Used,Free,ChatID)
                if str(CK) == "OK":
                    INFO+=("|--Sync Update--|\
                    \nUser:"+str(ChatID)+"\
                    \nCoin:"+coin+"\
                    \nTotal:"+str(Total)+"\
                    \nUsed:"+str(Used)+"\
                    \nFree:"+str(Free))
                    continue
                else:
                    return("Sync Update database --> Failed")

        return INFO

    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')


def sync_balance_all(id,Exchange,ChatID):
    try:
        INFO=""
        account_balance = id.fetch_balance({'type': 'account'})
        for coin in ((account_balance['total'])):
            Total=(str(format_floatc(account_balance['total'][coin], 6)))
            Used=(str(format_floatc(account_balance['used'][coin], 6)))
            Free=(str(format_floatc(account_balance['free'][coin], 6)))
            #-----------------------------------
            CK = Get_CoinBlance(Exchange,coin,ChatID)
            if str(CK) == "()":
                if Total != "" and Used != "" and Free != "":
                    CK=Insert_CoinBlance(Exchange,coin,Total,Used,Free,ChatID)
                    if str(CK) == "OK":
                        print("|--Sync Update New --|\
                        \nUser:" + str(ChatID) + "\
                        \nCoin:" + str(coin) + "\
                        \nTotal:" + str(Total) + "\
                        \nUsed:" + str(Used) + "\
                        \nFree:" + str(Free))
                        continue
                    else:
                        return("Sync Update database --> Failed")
            else:
                CK=Update_CoinBlance(Exchange,coin,Total,Used,Free,ChatID)
                if str(CK) == "OK":
                    print("|--Sync Update--|\
                \nUser:"+str(ChatID)+"\
                \nCoin:"+coin+"\
                \nTotal:"+str(Total)+"\
                \nUsed:"+str(Used)+"\
                \nFree:"+str(Free))
                    continue
                else:

                    return("Sync Update database --> Failed")

    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')




def main():
    # bxin=ccxt.bxinth()
    bxin = ccxt.bxinth({
        'apiKey': '8c9c30602acc',
        'secret': 'e7906fb559d2',
        "enableRateLimit": True,
    })
    ChatID=259669700
    CK = Get_CoinBlance('bxinth','LTC', str(ChatID))
    if CK != "faile":
        for bl in list(CK):
            coin=(bl[2])
            total=format_floatc(bl[3],5)
            used=format_floatc(bl[4],5)
            free=format_floatc(bl[5],5)
        print("\n|==Balance "+coin+" ==|\
                \n  Coin: "+coin+ "\
                \n  Total:"+total+"\
                \n  Used:"+used+"\
                \n  Free:"+free+"\
                \n|===============|")

    INFO=Update_Balance_Exc('bxinth','THB','THB',5,'buy',"C",str(ChatID))
    if INFO[0] == True:
        print(INFO[1])
    #print(sync_balance_coin(bxin,'bxinth','LTC',str(ChatID)))
    #print(CK)
    #BXCOIN=['BCH/THB','BTC/THB','LTC/THB']
    #INFO=""
    #for coin in BXCOIN:
    #     ST=get_balance(bxin,coin)
    #     if ST==201:
    #         continue
    #     else:
    #         INFO+=(ST)
    #print(INFO)

    #print(bxin.fe())



    #while True:
    #   #UUID, Exchange, LastPrice,StartRate
        #Lasprice=get_lastprice_sim('LTC/THB','bxinth')
        #ST=buy_StopBuy_shadow('86715032','bxinth',Lasprice,8000)
        #print(ST)
        #time.sleep(2)


    #buy=500000
    #p_point=[5,2,2,1,1,1,1]
    #data_ck=[]
    #data_ck=cal_stop_point(buy, p_point)
    #for data in data_ck:
    #    print("data is "+str(data))
    #ST=get_coin_information(bxin,'BTC/THB')
    #print(ST)

    #Coin=2
    #ratio=10
    #sell=(Coin / ratio)
    #ST=bxin.fetch_order_book('BTC/THB')
    #count=0
    #profit=[]
    #cont=""
    #cont+=("|-- BIDS --| \n")
    #for data in ST['bids']:
    #   cont+=("Bid:" + str(format_float(data[0])) + " vl:" + str(data[1])+"\n")
    #   count += 1
    #   if count == 5:
    #        break
    #count=0
    #cont+=("|-- ASKS --|\n")
    #for data in ST['asks']:
    #    cont+=("Ask:" + str(format_float(data[0])) + " vl:" + str(data[1])+"\n")
    #    count += 1
    #    if count == 5:
    #        break

    #print(cont)


    #print("Order Buy")
   # print(buy_coin_sim('DASH/THB',20,30000,'bxinth'))
   # print("Order Sell")
   # print(sale_coin_sim('DASH/THB', 20, 70000, 'bxinth'))
    #Order = (buy_coin(bxin, 'BTC/THB', 10, 600000, 'bxinth'))
    #print(Order)
    # print(Get_OrderBuy('bxinth','buy'))

    #SS = Get_OrderBuy('bxinth', 'buy')
    #for order in list(SS):
    #    Time = (order[1])
    #    order_id = (order[0])
    #    coin = (order[2])
    #    rate = (order[4])
    #    qty = (order[3])
    #    print("Starting trader " + coin)
    #    print("" + Time + " id:" + str(order_id) + " " + coin + " Qty" + str(qty) + " Rate:" + str(rate))
    #    volumn = format_float(qty / rate)
    #    print("Volumn: " + volumn)


      #  print("### Start Cutloss ###")
       # lastprice = get_lastprice(bxin, str(coin))
       # lastprice=30000
       # if is_number(lastprice) == True:
       #     if order_id != 0 and order_id != None:
        #        result=trailling_stop(bxin, order_id, 'bxinth', lastprice, coin, volumn)
        #        if result != None:
        #            if result[0] == "CutLoss":
         #               print("CutLoss "+str(result[1]))
         #               time.sleep(3)
         #           elif result[0] == "StopLoss":
         #               print("StopLoss "+str(result[1]))
       # else:
        #    print("Last Price is Null")
        #    continue




            #print("" + coin)
            #print(ck_close_order(bxin,'568863','DASH/THB','sell','bxinth'))
            # bxin.sign('https://bx.in.th/api/getorders/','p')
            #print(bxin.fetch_open_orders())
            #print(bxin.fetch_order_status('bxinth'))
            #trade=bxin.fetch_trades('DASH/THB')
            #for order in trade:
            #   print(order['info'])
            #print(TD)
           # ST=bxin.create_order('DASH/THB', 'THB', 'sale', 20, 200,{'leverage': 3})
            #print(ST)


#Result = bxin.create_order('OMG/THB', 'market', 'buy',30, 100, {'leverage': 3})
#print(Result)

            # print(bxin.fetch_trades('DASH/THB'))

            # print(cancel_coin(bxin,'542371','DASH/THB'))
            # print(get_lastprice(bxin,'DASH/THB'))
            #symbols('bxinth')
            #data=get_coin_information(bxin,'DASH/THB')
            #print(str(data))
            #print(get_balance(bxin,'THB'))
            #print(bxin.fetch_balance())
            #print(bxin.fetch_ticker('DASH/THB'))
            #print("----------------------------------------")
            #print(bxin.fetch_trades('DASH/THB',10000))
            #for trade in (bxin.fetch_trades('DASH/THB', 'xx')):
            #    #if trade['side'] == "sell":
            #    print("Type=>" + trade['side'])
            #    print("Trading_ID=>" + trade['id'])
            #    print("Order_ID=>" + trade['info']['order_id'])
            #    if Order == str(trade['info']['order_id']):
            #        print("Found ID")
            #if trade['info']['side'] == "buy":
            #   print(trade['info']['order_id'])
            #else:
            #  print(trade['info']['order_id'])
            # while True:  # print(get_openorder('bxinth','sell','DASH/THB'))  # Exchange = 'Bittrex'
# start = time.time()
# for uuid in Get_BittrexOrder_UUID(Exchange):
# print('UUID=>' + uuid[0])
# cutloss(uuid[0], Exchange, 'USDT-BCC')
#        print('-----------------------')
#        end = time.time()
#        if end - start < TICK_INTERVAL:
#            time.sleep(TICK_INTERVAL - (end - start))


if __name__ == "__main__":
   main()


