__author__ = 'thawornwit'
from bittrex_tokens import *  ## for accessing telegram api
import matplotlib  ## for ploting graph
import os
import sys
from operator import itemgetter
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
#from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
#from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
#from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
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
    StopLoss_Point = 0
    StopLoss = Get_BittrexDB(UUID, Exchange, 'ckloss', 'Stoploss')
    StopLoss = (list(StopLoss.split(',')))
    if len(StopLoss) > 1:
        print("Using Custom Mode !!")
        HaveCustom = True
    else:
        HaveCustom = False
        StopLoss = int(StopLoss[0])
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
    #MinProfit = (BuyRate + (BuyRate * (StopLoss / 100)))
    #print("Minimum Profit=>" + str(MinProfit))
    print("Start Cost =>" + str(BuyRate) + " Price Up =>" + str(LastPrice - BuyRate) + " (+/-) =>" + str(
        (100 * (LastPrice - BuyRate)) / BuyRate) + "%")
    print("--------------------------")
    ## Price UP ##
    if LastPrice > BuyRate:
        if StopLoss != "" or StopLoss != 0:
            StopLoss_Point_bf = Get_BittrexDB(UUID, Exchange, 'ckloss', 'StoplossPoint') ## Stop loss before
            if HaveCustom == False:
                StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))  ## current stop loss
            if HaveCustom == True:
                for StopPoint in StopLoss:
                    if StopLoss_Point_bf < int(StopPoint):
                        StopLoss_Point = int(StopPoint)
                        break
                    else:
                        StopLoss_Point = LastPrice
            #StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))  ## current stop loss
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
            if LastPrice < StopLoss_Point_bf:
                print("Sale coin because last price less than stop point => "+str(StopLoss_Point_bf)+"")
                return ('StopLoss',LastPrice,StopLoss)
    elif LastPrice == BuyRate:
        Update_Stoppoint(UUID, Exchange, '0')
        if HaveCustom == False:
            StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))
    elif LastPrice < BuyRate:
        if BuyRate != "failed":
            CutLossPrice = (BuyRate - (BuyRate * (CutLoss / 100)))
            print('CutLossPrice to Price =>' + str(CutLossPrice))
        if CutLossPrice >= LastPrice:
            return ('CutLoss', CutLossPrice,CutLoss)  ## Order  ##

## Order Buy ## Find good price and sale ,buy and find price up
def buy_trailling_stop_shadow(UUID, Exchange, LastPrice,BuyRate):
    StopLoss_Point_bf=0
    StopLoss_Point=0
    StopLoss = Get_BittrexDB(UUID,Exchange, 'ckloss', 'Stoploss')
    StopLoss = (list(StopLoss.split(',')))
    if len(StopLoss) > 1:
       print("Using Custom Mode !!")
       HaveCustom=True
    else:
        HaveCustom=False
        StopLoss = int(StopLoss[0])
    CutLoss = Get_BittrexDB(UUID,Exchange, 'ckloss', 'Cutloss')

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
    #MinProfit = (BuyRate + (BuyRate * (StopLoss / 100)))
    #print("Minimum Profit=>" + str(MinProfit))
    print("Buy Cost =>" + str(BuyRate) + " Price Up =>" + str(LastPrice - BuyRate) + " (+/-) =>" + str(
        (100 * (LastPrice - BuyRate)) / BuyRate) + "%")
    print("--------------------------")
    ## Price UP ##
    if LastPrice > BuyRate:
        if StopLoss != "" or StopLoss != 0:
            StopLoss_Point_bf = Get_BittrexDB(UUID, Exchange, 'ckloss', 'StoplossPoint') ## Stop loss before
            if HaveCustom == False:
                StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))  ## current stop loss
            if HaveCustom == True:
                for StopPoint in StopLoss:
                    if StopLoss_Point_bf < int(StopPoint):
                        StopLoss_Point=int(StopPoint)
                        break
                    else:
                        StopLoss_Point = LastPrice

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
            if LastPrice < StopLoss_Point_bf:
                print("Sale coin because last price less than stop point => "+str(StopLoss_Point_bf)+"")
                return ('StopLoss', LastPrice,StopLoss)
    elif LastPrice == BuyRate:
        Update_Stoppoint(UUID, Exchange, '0')
        if HaveCustom == False:
            StopLoss_Point = LastPrice - (LastPrice * (StopLoss / 100))
    elif LastPrice < BuyRate:
        if BuyRate != "failed":
            CutLossPrice = (BuyRate - (BuyRate * (CutLoss / 100)))
            print('CutLossPrice to Price =>' + str(CutLossPrice))
        if CutLossPrice >= LastPrice:
            return ('CutLoss', CutLossPrice,CutLoss)

## Find price deep dows ## Find price low and Buy
def buy_StopBuy_shadow(UUID, Exchange, LastPrice,StartRate):
    print("UUID="+str(UUID))
    StopBuy = Get_BittrexDB(UUID, Exchange, 'ckstopbuy', 'StopBuy')
    StopBuy=(list(StopBuy.split(",")))
    print("Debug StopBuy"+str(StopBuy))
    if len(StopBuy) > 1:
        print("Using Custom Mode !!")
        HaveCustom = True
    else:
        HaveCustom = False
        StopBuy = int(StopBuy[0])
    StopRisk = Get_BittrexDB(UUID, Exchange, 'ckstopbuy', 'StopRisk')
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
            if HaveCustom == False:
                StopBuy_Point = LastPrice - (LastPrice * (StopBuy / 100))  ## current cutloss
                print('StopBuy_Point=' + str(StopBuy_Point))
                print('StopBuy_Point_Action=' + str(StopBuy_Point_bf))
            if HaveCustom == True:
                for StopPoint in StopBuy:
                    if StopBuy_Point_bf > int(StopPoint):
                        StopBuy_Point = int(StopPoint)
                        break
                    else:
                        StopBuy_Point = LastPrice

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
            if LastPrice > StopBuy_Point_bf:
                print("Buy coin because last price up than Stop Buy Point => "+str(StopBuy_Point_bf)+"")
                return ('StopBuy', LastPrice,StopBuy)  ### Stop and Buy coin Now !!!
    elif LastPrice == StartRate:
        Update_StopBuyPoint(UUID, Exchange, '0')
        if HaveCustom == False:
            StopBuy_Point = LastPrice - (LastPrice * (StopBuy / 100))
    elif LastPrice > StartRate:
        if StartRate != "failed":
            StopRiskPrice = (StartRate + (StartRate * (StopRisk / 100)))
            print('StopRisk Price =>' + str(StopRiskPrice))
        if StopRiskPrice <= LastPrice:
            return ('StopRisk', StopRiskPrice,StopRisk)   ### StopRisk becuase price is up



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



def symbols(exc,base_market):
    try:
        exchange_found = exc in ccxt.exchanges
        if exchange_found:
            exchange = getattr(ccxt, exc)({
                # 'proxy':'https://cors-anywhere.herokuapp.com/',
            })
            # load all markets from the exchange
            markets = exchange.load_markets()
            #print("Matket => " + str(markets))
            # output a list of all market symbols
            #dump(green(id), 'has', len(exchange.symbols), 'symbols:', exchange.symbols)
            tuples = list(ccxt.Exchange.keysort(markets).items())
            # debug
            #for (k, v) in tuples:
            #   print(v['info']['secondary_currency'])
            # output a table of all markets
            dump(pink('{:<9} {:<9} {:<9} {:<9}'.format('id', 'symbol', 'base', 'quote')))
            for (k, v) in tuples:
                if v['quote'] == str(base_market):
                    dump('{:<9} {:<9} {:<9} {:<9}'.format(v['id'], v['symbol'], v['base'], v['quote'], v['info']))
        else:

            dump('Exchange ' + red(id) + ' not found')
            print_supported_exchanges()

    except Exception as e:
        dump('[' + type(e).__name__ + ']', str(e))
        #dump("Usage: python " + sys.argv[0], green('id'))


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
                \n[= UPDATE BALANCE =]\
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
            total = format_floatc(bl[3], 8)
            used = format_floatc(bl[4], 8)
            free = format_floatc(bl[5], 8)
            INFO=("\n[BALANCE (" + coin +")]\
                   \nTotal:[" + total + "]\
                   \nUsed:[" + used + "]\
                   \nFree:["+ free + "]\
                   \n----------------")
        if float(total) > 0:
            return (True,free,INFO)
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
        #print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        #print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        #print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        #print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
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
                                  'open', exchange,'cts')
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
                return Oid
            else:
                return Result['info']['error']
        else:
            return (str("Sale " + symbol + " Failed error is" + Result['info']['error']))
            # return 1

    except ccxt.DDoSProtection as e:
        #print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        #print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        #print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        #print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
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
        #print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        #print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        #print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        #print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')

def buy_coin_res(symbol, volumn, price, exchange):
    number = ''.join(random.sample("0123456789", 8))
    print("Number of randome is" +str(number))
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
                                  exchange,'bls')
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
def buy_coin_sim(symbol, volumn, price):
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
            #Total = volumn
            #Qty = volumn / price
            #ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), symbol, 'buy', price, Qty, Total, 'open',
            #                      exchange, 'bts')
            #if ST == "OK":
            return Oid
            #else:
            #    return "Error,Insert Database open order failed"
        else:
            return Result['info']['error']

    else:
        return (str("Buy " + symbol + " Failed error is" + Result['info']['error']))
        # return 1

def buy_coin(id, symbol, volumn, price):
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
                #Total = volumn
                #Qty = volumn / price
                #ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), symbol, 'buy', price, Qty, Total, 'open',
                 #                     exchange,'bts')
                #if ST == "OK":
                return Oid
                #else:
                   # return "Error,Insert Database open order failed"
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


def get_coin_information(id, symbol,line):
    try:
        INFO = "[COIN INFORMATION] \n"
        info = (id.fetch_ticker(symbol))
        print(info)
        bid=(info['info']['orderbook']['bids']['volume'])
        aks=(info['info']['orderbook']['asks']['volume'])

        INFO += str("Coin:" + symbol + "\n")
        INFO += str("Change:" + str(info['info']['change']) + " %\n")
        INFO += str("[Buy/Sell]:"+str(format_floatc(((bid/aks)*100),2))+" %\n")
        INFO += str("LastPrice:" + str(format_floatc((info['info']['last_price']),4)) + "\n")
        INFO += "|--------------------| \n"
        ST = id.fetch_order_book(symbol)
        #print(ST)
        count = 0
        INFO += ("[LAST BX ORDER]\n")
        INFO+=("[ BIDS ][Vl:"+str(format_floatc(bid,4))+"]\n")
        for data in ST['bids']:
            count += 1
            INFO +=("("+str(count)+")|"+str(format_floatc((data[0]),4)) + "|" + str(format_floatc((data[1]),4)) + "\n")
            if count == line:
                break
        count = 0
        INFO += ("[ ASKS ][Vl:"+str(format_floatc(aks,4))+"]\n")
        for data in ST['asks']:
            count += 1
            INFO += ("("+str(count)+")|"+str(format_floatc((data[0]),4)) + "|" + str(format_floatc((data[1]),4)) + "\n")
            if count == line:
                break
        INFO +="|--------------------| \n"

        #print(INFO)
        return INFO

    except ccxt.DDoSProtection as e:
        #print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        #print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        #print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        #print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')

def good_coin_ck(id,exc,base_market):
    try:
        INFO=""
        PBUY=[]
        exchange_found = exc in ccxt.exchanges
        if exchange_found:
            exchange = getattr(ccxt, exc)({
                    # 'proxy':'https://cors-anywhere.herokuapp.com/',
            })
                # load all markets from the exchange
            markets = exchange.load_markets()
                # print("Matket => " + str(markets))
                # output a list of all market symbols
                #dump(green(id), 'has', len(exchange.symbols), 'symbols:', exchange.symbols)
            tuples = list(ccxt.Exchange.keysort(markets).items())
           # print(str(tuples))
                # debug
                #for (k, v) in tuples:
                #   print(v['info']['secondary_currency'])
                # output a table of all markets
            #INFO+=(('{:<10}{:<10}'.format('Coin','Buy/Sell(%)')))
            PBUY.clear()
            for (k, v) in tuples:
                if v['quote'] == str(base_market):
                    info = (id.fetch_ticker(v['symbol']))
                    bid = (info['info']['orderbook']['bids']['volume'])
                    aks = (info['info']['orderbook']['asks']['volume'])
                    buy_sell=float(format_floatc(((bid / aks) * 100), 2))
                    sell_buy=float(format_floatc(((aks / bid) * 100), 2))
                    PBUY.append((v['base'],buy_sell,sell_buy))
                    #INFO+=("\n"+('{:<10}{:<10}'.format(v['base'],str(format_floatc(((bid/aks)*100),2))+" %")))
                    #dump('{:<9} {:<9} {:<9} {:<9}'.format(v['symbol'], v['base'], v['quote']))

            return sorted(PBUY,key=itemgetter(1),reverse=True)
            #return sorted(PBUY,key = lambda good: good[1])

            #return sorted(PBUY, key=itemgetter(1))

        else:

            dump('Exchange ' + red(id) + ' not found')
            print_supported_exchanges()

        #info = (id.fetch_ticker(symbol))
        #print(info)
        #bid=(info['info']['orderbook']['bids']['volume'])
        #aks=(info['info']['orderbook']['asks']['volume'])

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

def get_coin_lastorder(id, symbol,type):
    try:
        INFO=""
        ST = id.fetch_order_book(symbol)
        #print(ST)
        count = 0
        if type == "buy":
            for data in ST['bids']:
                count += 1
                return (str(format_floatc((data[0]),4)),str(format_floatc((data[1]),4)))
                if count == 1:
                    break
        count = 0
        if type == "sell":
            for data in ST['asks']:
                count += 1
                return (str(format_floatc((data[0]),4)),str(format_floatc((data[1]),4)))
                if count == 1:
                    break

    except ccxt.DDoSProtection as e:
        #print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        #print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        #print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        #print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')

def check_coin_list(id, symbol,rate,volumn,type):
    try:
        INFO=""
        order_list = id.fetch_order_book(symbol)
        #print("OrderList>"+str(order_list))
        if type == "buy":
            count = 0
            for data in order_list['bids']:
                count += 1
                rate_ck=str(format_floatc((data[0]), 4))
                volumn_ck= str(format_floatc((data[1]), 4))
                #print(rate_ck+"|"+volumn_ck)
                if str(rate) == str(rate_ck) and str(volumn_ck) == str(volumn):
                    return (True,""+str(count)+"|"+str(rate_ck) + "|" + str(volumn_ck) + "\n")
                    break
                else:
                    INFO += ("" + str(count) + "|" + str(rate_ck) + "|" + str(volumn_ck) + "\n")
                    continue
        elif type == "sell":
            count = 0
            for data in order_list['asks']:
                count += 1
                rate_ck =format_floatc((data[0]), 4)
                volumn_ck =format_floatc((data[1]), 4)
                if str(rate) == str(rate_ck) and str(volumn) == str(volumn_ck):
                    return (True,""+str(count)+"|"+str(rate_ck) + "|" + str(volumn_ck) + "\n")
                    break
                else:
                    INFO += ("" + str(count) + "|" + str(rate_ck) + "|" + str(volumn_ck) + "\n")
                    continue

        return(False,"Not found order")


    except ccxt.DDoSProtection as e:
        #print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (False,str(e)+'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        #print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (False,str(e)+'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        #print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (False,str(e)+'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        #print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (False,str(e)+'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (False,str(e)+'Exchange Error')


def check_coin_list_sim(Coin,rate_ck,volumn_ck,type,exchange):
        INFO=""
        if type == "buy":
            count = 0
            ##Tor Dev
            data_trading = Get_OpenOrder(exchange, 'trading')
            if str(data_trading) == "()":
                return (False,"Data is null")
            ST=sorted(list(data_trading), key=itemgetter(4), reverse=True)
            print("List Trading Open order"+str(ST))
            for order in list(ST):
                Time = (order[2])
                order_id = (order[1])
                coin = (order[3])
                Type = (order[4])
                rate = (order[5])
                volumn = (order[6])
                exchange = (order[9])
                strategy = (order[10])
                qty = (order[7])
                if coin == Coin:
                    count += 1
                    print("Coin "+coin+"\nrate:"+str(format_floatc(rate,4))+" rate_ck:"+str(rate_ck)+"\nVolumne"+str(format_floatc(volumn,4))+"VolumnCK"+str(volumn_ck))
                    if str(rate_ck) == str(format_floatc(rate,4)) and str(volumn_ck) == str(format_floatc(volumn,4)):
                        print ("Acccess to comppare coin rate check and volum check for check Await Order")
                        return (True,""+str(count)+"|"+str(rate_ck) + "|" + str(volumn_ck) + "\n")
                    else:
                        continue
                else:
                    continue

            return (False, "Not found order")

        elif type == "sell":
            count = 0
            data_trading = Get_OpenOrder(exchange, 'trading')
            if str(data_trading) == "()":
                return (False, "Data is null")
            ST = sorted(list(data_trading), key=itemgetter(4), reverse=True)
            print("List Trading Open order" + str(ST))
            for order in list(ST):
                Time = (order[2])
                order_id = (order[1])
                coin = (order[3])
                Type = (order[4])
                rate = (order[5])
                volumn = (order[6])
                exchange = (order[9])
                strategy = (order[10])
                qty = (order[7])

                if coin == Coin:
                    count += 1
                    print("Coin " + coin + "\nrate:" + str(format_floatc(rate, 4)) + " rate_ck:" + str(
                        rate_ck) + "\nVolumne" + str(format_floatc(volumn, 4)) + "VolumnCK" + str(volumn_ck))
                    if str(rate_ck) == str(format_floatc(rate, 4)) and str(volumn_ck) == str(format_floatc(volumn, 4)):
                        print("Acccess to comppare coin rate check and volum check for check Await Order")
                        return (True, "" + str(count) + "|" + str(rate_ck) + "|" + str(volumn_ck) + "\n")
                    else:
                        continue
                else:
                    continue
            return (False, "Not found order")
        else:
            return(False,"Not found order")
#def check_close_trader():









#######################
def get_lastprice_sim(symbol,exchange):
    Price=Get_Bittrex_Price(symbol, exchange)  ## Sim for Tesss
    return Price

#######################
def get_lastprice(id, symbol):
    try:
        Price = (id.fetch_ticker(symbol))
       # print(str(Price))
        return (Price['last'])

    except ccxt.DDoSProtection as e:
        #print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e)+'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        #print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e)+'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        #print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        #print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e)+'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        #print(type(e).__name__, e.args,'Exchange Error' )
        return (str(e)+'Exchange Error')


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

def get_lastcoin(id,exc):
    try:
        COINLIST = []
        exchange_found = exc in ccxt.exchanges
        if exchange_found:
            exchange = getattr(ccxt,exc)({
                # 'proxy':'https://cors-anywhere.herokuapp.com/',
            })
            markets = exchange.load_markets()
            tuples = list(ccxt.Exchange.keysort(markets).items())
            COINLIST.clear()
            for (k, v) in tuples:
                if v['quote'] == "THB":
                    info = (id.fetch_ticker(v['symbol']))
                    ch = str(info['info']['change'])
                    ls = str(format_floatc((info['info']['last_price']),2))
                    COINLIST.append((v['base'],format_floatc(float(ls),2),float(ch)))
            return sorted(COINLIST, key=itemgetter(2), reverse=True)

    except ccxt.DDoSProtection as e:
        #print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        #print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        #print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        #print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')


# def apply_trailing_stop(lastprice):

### CHECK CLOSE ORDER ##

def ck_close_order_sim(order_id, symbol, Type, exchange):
    lastprice = get_lastprice_sim(symbol,exchange)
    if lastprice == "failed" or lastprice == None:
        print("!!! Can't get lastprice ")
        return False
    print("Current Lasprice sim " + str(lastprice))
    # lastprice=get_lastprice(id,symbol)
    if Type == 'sell' and order_id != 0 and order_id != None:
        OpenRate = Get_Rate_OpenOrder(order_id, exchange, symbol, Type)
        print("Open Rate:" + str(OpenRate))
        if is_number(OpenRate) == True:
            if float(lastprice) >= float(OpenRate):
                ST = Update_OpenOrder(order_id, exchange, 'close')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to closed")
                    return (True,"close")
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    return (False,"close")
            else:
                ST = Update_OpenOrder(order_id, exchange, 'trading')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to trading")
                    return (True, "trading")
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    return (False, "trading")

    if Type == 'buy' and order_id != 0 and order_id != None:
        OpenRate = Get_Rate_OpenOrder(order_id, exchange, symbol, Type)
        print("Open Rate:" + str(OpenRate))
        if is_number(OpenRate) == True:
            if float(lastprice) <= float(OpenRate):
                ST = Update_OpenOrder(order_id, exchange, 'close')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to closed")
                    return (True,"close")
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    return (False,"close")
            else:
                ST = Update_OpenOrder(order_id, exchange, 'trading')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to trading")
                    return (True, "trading")
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    return (False, "trading")

    if Type == 'cancle' and order_id != 0 and order_id != None:
        ST = Update_OpenOrder(order_id, exchange, 'close')
        if ST == "OK":
            print("Update Open Order " + order_id + " to cancel")
            return (True,"cancel")
        else:
            print("Update Open Order " + order_id + " failed")
            return (False,"cancel")



def ck_close_order(id, order_id, symbol, Type, exchange):
    lastprice = get_lastprice(id, symbol)
    if lastprice == "failed" and lastprice == None:
        print("!!! Can't get lastprice ")
        return False
    print("Current Lasprice " + str(lastprice))
    # lastprice=get_lastprice(id,symbol)
    if Type == 'sell' and order_id != 0 and order_id != None:
        OpenRate = Get_Rate_OpenOrder(order_id, exchange, symbol, Type)
        print("Open Rate:" + str(OpenRate))
        if is_number(OpenRate) == True:
            last_rate=get_coin_lastorder(id,symbol,'buy')
            if lastprice >= OpenRate and OpenRate <= float(last_rate[0]):
                ST = Update_OpenOrder(order_id, exchange, 'close')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to closed ..")
                    return (True,"close")
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    return (False,"close")
            else:
                ST = Update_OpenOrder(order_id, exchange, 'trading')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to trading ..")
                    return (True,"trading")
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to trading and failed")
                    return (False,"trading")

    if Type == 'buy' and order_id != 0 and order_id != None:
        OpenRate = Get_Rate_OpenOrder(order_id, exchange, symbol, Type)
        print("Open Rate:" + str(OpenRate))
        if is_number(OpenRate) == True:
            last_rate = get_coin_lastorder(id, symbol, 'sell')
            if lastprice <= OpenRate and OpenRate >= float(last_rate[0]):
                ST = Update_OpenOrder(order_id, exchange, 'close')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to closed ..")
                    return (True,"close")
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    return (False,"close")
            else:
                ST = Update_OpenOrder(order_id, exchange, 'trading')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to trading ..")
                    return (True,"trading")
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to trading and failed")
                    return (False,"trading")

    if Type == 'cancel' and order_id != 0 and order_id != None:
        ST = Update_OpenOrder(order_id, exchange, 'cancel')
        if ST == "OK":
            print("Update Open Order " + order_id + " to cancel")
            return (True,"cancel")
        else:
            print("Update Open Order " + order_id + " failed")
            return (False,"cancel")

    if order_id == 0 and order_id == None:
        return(False,"nocase")


### SYNC BALANCE ###

def sync_balance_coin(id,Exchange,Coin,ChatID):
    try:
        INFO=""
        Coin = check_sys("data=" + Coin + ";echo ${data%/*}")
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
        #print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        #print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        #print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        #print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
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
                        return "Sync Update database --> Failed"
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
                    return "Sync Update database --> Failed"

    except ccxt.DDoSProtection as e:
        #print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        return (str(e) + 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        #print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        return (str(e) + 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        #print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        return (str(e) + 'Exchange Not Available due to downtime or maintenance (ignoring)')
    except ccxt.AuthenticationError as e:
        #print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        return (str(e) + 'Authentication Error (missing API keys, ignoring)')
    except ccxt.ExchangeError as e:
        return (str(e) + 'Exchange Error')




def main():
    # bxin=ccxt.bxinth()
    bxin = ccxt.bxinth({
        'apiKey': '063689a6d467',
        'secret': '69e49ad534c5',
        "enableRateLimit": True,
    })
   # print(get_lastprice(bxin,'BTC/THB'))
    #info = bxin.fetch_ticker('DASH/THB')
    #print("bids"+str(info['info']['orderbook']['bids']['volume']))
    #print("asks"+str(info['info']['orderbook']['asks']['volume']))
    #print(symbols('bxinth','THB'))
    #CK=(good_coin_ck(bxin,'bxinth','THB'))
    #CK=get_lastcoin(bxin,'bxinth')
    #sorted(CK, key=itemgetter(1), reverse=True)
    #print(str(CK))
   # for i in CK:
   #     print(str(i[0])+"|"+str(i[1])+"|"+str(i[2]))

    #print(bxin.
   # ChatID=259669700
    #CK = Get_CoinBlance('bxinth','LTC', str(ChatID))
   # if CK != "faile":
   #   for bl in list(CK):
   #         coin=(bl[2])
   ##         total=format_floatc(bl[3],5)
    #        used=format_floatc(bl[4],5)
    #        free=format_floatc(bl[5],5)
    #    print("\n|==Balance "+coin+" ==|\
    #            \n  Coin: "+coin+ "\
    #            \n  Total:"+total+"\
    #            \n  Used:"+used+"\
    #            \n  Free:"+free+"\
    #            \n|===============|")

    #volumn = format_floatc((float(volumn) - (float(volumn) * fee)), 4)
    #bot.sendMessage(chat_id, "" + emoji.emojize(':hourglass:') + " Sell under Processing .. ")
    #vl=5.2
    #vl=vl-(vl*0.0025)
    #price=19
    #print(Get_OrderSale('bxinth','trading'))
    #OID=sale_coin(bxin,'LTC/THB',float(format_floatc(vl,4)),float(format_floatc(price,4)))
    #print(OID)
    #INFO=get_coin_information(bxin,'POW/THB',100)
    #print(INFO)
    #print(str(format_floatc(price,4)))
    #print(str(format_floatc(vl,4)))
    #INFO=check_coin_list(bxin,'POW/THB',str(format_floatc(price,4)),str(format_floatc(vl,4)),'sell')
    #print(INFO)
    #if INFO != None:
    #    if INFO[0] == True:
    #        print(INFO[1])
    #else:
    #    print("Not Found !!")

    #print(get_coin_lastorder(bxin,'LTC/THB','asks'))
    #print(get_lastcoin(bxin,'LTC/THB'))
    #SK=get_coin_information(bxin,'LTC/THB',2)
    #print(SK)
    #if INFO[0] == True:
     #   print(INFO[1])
        #print(bxin.fetch_balance())
       # print(sync_balance_all(bxin,'bxinth',str(ChatID)))

    #INFO=Update_Balance_Exc('bxinth','THB','THB',5,'buy',"C",str(ChatID))
    #if INFO[0] == True:
    #print(get_coin_information(bxin,'LTC/THB'))
     #   print(INFO[1])
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


