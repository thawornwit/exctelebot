##############################################################################################################################
# IAMS BOT for Int Telegram monitor all server and send alarm to bot include interacrive with all server by shell command    #
# This is project by THAWORNWIT PLANRAM                                                                                      #
# ID 5710421006 ,NIDA Com32                                                                                                  #
##############################################################################################################################

from tokens import *  ## for accessing telegram api
from botmain import *
import matplotlib  ## for ploting graph 
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
from iamsbot_function import *
#### Table format ###
from prettytable import PrettyTable
## GROBAL variable #####
##### Configuration memory threshold and interval for check system ########
memorythreshold = 80  # If memory usage more this %
roomtempthreshold = 35
roomflag = 0
poll = 60  # seconds
Notification = "ON"
Email = ""
Text_mail = ""
COUNT = 0

##########BOT COIN#############
BX = []
BITTREX = []
YOBIT = []

CKLOSS = []
CKCOMMAND = []
BXCOIN = ['THB/THB','BTC/THB', 'LTC/THB', 'DASH/THB', 'BCH/THB', 'OMG/THB', 'XRP/THB', 'REP/THB', 'GNO/THB', 'ETH/THB', 'XZC/THB']
COINTEMP = []
COINTEMP.append(0)
ORDERBUY = []
ORDERSELL = []
LASTPRICESIM = []
COINLISTINFO = []
STRATEGY = []
CKCLOSE=[]
EX = []
NOTISTATE_ACTION=[]
UPDATE_ACT=[]
SELL_ORDER=[]
CKBALANCE=[]
menucoinmarkup = {
    'keyboard': [['BACK'], ['BTC', 'BCH'], ['LTC', 'OMG','ETH'], ['EVX', 'DASH', 'XZC'], ['GNO', 'REP', 'XRP']]}
menuexchange = {'keyboard': [['BACK'], ['BXINTH', 'TDAX'], ['BITTREX', 'YOBIT']]}
mainmenu = {'keyboard': [['BUY', 'SELL', 'INFO'], ['SELL ORDER','CANCEL ORDER','BALANCE'], ['NOTIFICATION', 'STRATEGY'], ['TASK ORDER','CANCEL']]}
mainmenust = {'keyboard': [['BUY', 'SELL', 'INFO'], ['SELL ORDER','CANCEL ORDER'], ['NOTIFICATION', 'STRATEGY'], ['CLOSE','UPDATE']]}
## Default Stop loss and Cut loss ##
BuyStopLoss = 5
BuyCutLoss = 3
SellStopLoss = 5
SellCutLoss = 3

STRATEGY_CHECK="ON"
noti_sts = "ON"
noti_bts = "ON"
allow_cutloss_bts ="NO"
allow_stoploss_bts ="NO"
allow_update_bts="NO"
allow_cutloss_sts="NO"
allow_stoploss_sts="NO"
allow_update_sts="NO"
#-------Update Point-----#
allow_update_point_sts = "NO"
allow_update_point_bts = "NO"
#-------Close Order -----#
allow_close_sts = "NO"
allow_close_bts = "NO"

NOTIBTS_INFO=""
NOTISTS_INFO=""
simtest = ""
Coin = ""
################### make up keybord stop ######
stopmarkup = {'keyboard': [['Stop Interactive']]}  ## for build Stop command to telagram
cancelmarkup = {'keyboard': [[" "], ['CANCEL', 'BACK'], [" "]]}  ## for build cancle command to telagram
backmarkup = {'keyboard': [['Back']]}  ## for build cancle command to telagram
hide_keyboard = {'hide_keyboard': True}
###############################################
### BXINTH EXCHANGE ###
bxin = ccxt.bxinth({
    'apiKey': '8cdf0f0a666c',
    'secret': 'b6b22e1e51eb',
    "enableRateLimit": True,
})
#######################


class YourBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(YourBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None
        ########Init Member ID ######
        DB = Get_ID('register', 'ChatID', 'member')
        for L in DB:
            memberchatid.append(int(L[0]))
        print(memberchatid)
        ##############################
        DB = Get_ID('register', 'ChatID', 'admin')
        for L in DB:
            adminchatid.append(int(L[0]))
        print(adminchatid)
        ##############################

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata

            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def coin_buysalcan(self, chat_id, bxin, Coin):
        bot.sendChatAction(chat_id, 'typing')
        print("Debug Coin1" + Coin)
        if 'buyCoin' in BX:
            bot.sendMessage(chat_id, str(get_coin_information(bxin, Coin)))
            Bal = get_balance(bxin, 'THB')
            if Bal == 201:
                print("THB is balance not available.!!")
                bot.sendMessage(chat_id, str("THB Balance Not available.!!"))
                BX.clear()
            else:
                bot.sendMessage(chat_id, str(Bal))
                bot.sendMessage(chat_id, "How Many to Buy(THB) ?", reply_markup=cancelmarkup)
                BX.append(Coin)
        elif 'saleCoin' in BX:
            Bal = get_balance(bxin, Coin)
            if Bal == 201:
                print(Coin + " Balance Not available.!!")
                bot.sendMessage(chat_id, str(Coin + " Balance Not available.!!"))
                BX.clear()
            else:
                bot.sendMessage(chat_id, str(Bal))
                bot.sendMessage(chat_id, "How Many coin for Sell ?", reply_markup=cancelmarkup)
                BX.append(Coin)
                print("Debug Coin2" + Coin)
        elif 'cancelCoin' in BX:
            bot.sendMessage(chat_id, "|= TYPE =| \
                \n /BUY \
                \n /SELL ")

    def coin_buysalcanselect(self, chat_id, bxin, msg, Coin):
        bot.sendChatAction(chat_id, 'typing')
        if msg == "BACK":
            self.coinmenu(chat_id)
        elif msg == "CANCEL":
            return
        if 'buyCoin' in BX:
            Buy = msg
            # if Buy == "":
            #   return
            if is_number(Buy) == True and Buy != "0" or is_number(Buy) == True and float(Buy) > 0:
                print("DEBUG3" + Coin)
                if simtest == "yes":
                    bot.sendMessage(chat_id, "Now Sim Last Price:/" + str(get_lastprice_sim(str(Coin), 'bxinth')))
                else:
                    bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, Coin)))
                bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                if Coin in BX:
                    BX.remove(Coin)
                if 'buyCoin' in BX:
                    BX.remove('buyCoin')
                BX.append('BUY')
                return Buy
            else:

                bot.sendMessage(chat_id, "!! Enter number only and number more than zero")
                bot.sendMessage(chat_id, "How Many to Buy(THB) ?", reply_markup=cancelmarkup)

        elif 'saleCoin' in BX:
            Sell = msg
            print("DEBUG4" + Coin)
            if is_number(Sell) == True and Sell != "0" or is_number(Sell) == True and float(Sell) > 0:
                if simtest == "yes":
                    bot.sendMessage(chat_id, "Now Sim Last Price:/" + str(get_lastprice_sim(str(Coin), 'bxinth')))
                else:
                    bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, Coin)))
                bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                if Coin in BX:
                    BX.remove(Coin)
                if 'saleCoin' in BX:
                    BX.remove('saleCoin')
                BX.append('SELL')
                return Sell
            else:

                bot.sendMessage(chat_id, "!! Enter number only and using number more than zero")
                bot.sendMessage(chat_id, "How Many coin for sell ?", reply_markup=cancelmarkup)

    def coinbx(self, chat_id):
        bot.sendMessage(chat_id, "|=  COIN  =| \
            \n /BTC \
            \n /DASH \
            \n /LTC \
            \n /BCH \
            \n /GNO \
            \n /OMG \
            \n /REP \
            \n /XRP \
            \n /XZC \
            \n /EVX \
            \n /ETH ", reply_markup=menucoinmarkup)

    def coinmenu(self, chat_id):
        ## Clear Status ##
        BX.clear()
        CKCOMMAND.clear()
        ORDERBUY.clear()
        CKBALANCE.clear()
        COINLISTINFO.clear()
        SELL_ORDER.clear()
        ##############
        bot.sendMessage(chat_id, "|= EXCTELECOINS MENU  =|\
            \n\U0001F4B5 /buyCoin  \
            \n\U0001F4B5 /saleCoin \
            \n\U0001F4B5 /cancelCoin \
            \n\U0001F4B5 /ckCoinInfo \
            \n\U0001F4B5 /balance \
            \n\U0001F4B5 /strategy  \
            \n\U0001F4B5 /TaskOrder\
            \n\U0001F4B5 /Notification \
            \n\U0001F4B5 /ExchangeCompare \
            \n\U0001F4B5 /asicDash \
            \n\U0001F4B5 /cancel \
            \n--- Sim Price ---- \
            \n\U0001F4B5 /SetLastPrice \
            \n\U0001F4B5 /enableSimtest \
            ", reply_markup=mainmenu)

    def exchangemenu(self, chat_id, msg):
        bot.sendChatAction(chat_id, 'typing')
        ### Clear Status ###
        BX.clear()
        CKCOMMAND.clear()
        ORDERBUY.clear()
        #####################
        CKCOMMAND.append(msg)
        bot.sendMessage(chat_id, "|= EXCHANGE =| \
            \n /BXINTH  \
            \n /TDAX    \
            \n /BITTREX \
            \n /YOBIT   ", reply_markup=menuexchange)

    def on_chat_message(self, msg):
        global Notification
        global COUNT
        global COMMAND_ADD
        global COMMAND_ALIAS
        global SERVER_ADD
        global HOST
        global roomtempthreshold
        global roomflag
        global Buy
        global Sell
        global Rate
        global Coin
        global CutLoss
        global StopLoss
        global Oid
        global simtest
        global allow_cutloss_bts
        global allow_stoploss_bts
        global allow_cutloss_sts
        global allow_stoploss_sts
        global allow_update_bts
        global allow_update_sts
        global allow_update_point_sts
        global allow_update_point_bts
        global allow_close_sts
        global allow_close_bts
        global noti_bts
        global noti_sts
        global  STRATEGY_CHECK
        global NOTIBTS_INFO
        global NOTISTS_INFO

        content_type, chat_type, chat_id = telepot.glance(msg)
        content_type, chat_type, chat_id_test = telepot.glance(msg)
        print("Your chat_id_test:" + str(chat_id_test))

        # Do your stuff according to `content_type` ...
        print("Your chat_id:" + str(chat_id))  # this is chat_id
        print("Your admin_id:" + str(adminchatid))  # this is adminchatid
        print("Message Text:" + str(msg['text']))  ## message recived
        ### Connect to BX

        if chat_id in adminchatid:  # Store adminchatid variable in tokens.py
            # print("Welcome Administrator:")
            if content_type == 'text':
            ######### BTS Stratygy #########
               # self.bts('bxinth', chat_id)
                #if ST == False:
                #   continue
                  # print(ST)
                  # --------------------
                #time.sleep(2)
               # self.sts('bxinth',chat_id)
                # print(ST)
                #if ST == False:
                #    continue

                #time.sleep(2)
        ########### END BTS ##############
               # self.check_close_order('bxinth',chat_id)
                #if ST == False:
                #   continue

                if msg['text'] == "/setroomtemp" and chat_id not in settingroomtemp:
                    bot.sendChatAction(chat_id, 'typing')
                    settingroomtemp.append(chat_id)
                    bot.sendMessage(chat_id, "\U0001F4B2 Send me a new room temperature threshold to monitor?")
                if chat_id in settingroomtemp:
                    bot.sendChatAction(chat_id, 'typing')
                    try:
                        roomtempthreshold = int(msg['text'])
                        if roomtempthreshold < 50:
                            bot.sendMessage(chat_id, "\U00002714 Setting Room temperature completed ")
                            clearsetting(chat_id)
                        else:
                            1 / 0
                    except:
                        bot.sendMessage(chat_id, "Please send a proper numeric value below 50.")
                if msg['text'] == "BACK":
                    self.coinmenu(chat_id)

                if msg['text'] == '/enableSimtest':
                    bot.sendMessage(chat_id, "/YES \n /NO")
                    CKCOMMAND.append('enableSimtest')
                elif 'enableSimtest' in CKCOMMAND and msg['text'] == '/YES':
                    simtest = "yes"
                    bot.sendMessage(chat_id, "Enable Sim test mode -> Completed ")
                elif 'enableSimtest' in CKCOMMAND and msg['text'] == '/NO':
                    simtest = "no"
                    bot.sendMessage(chat_id, "Disable Sim test mode -> Completed ")

                if msg['text'] == '/SetLastPrice':
                    if simtest == "yes":
                        # bot.sendMessage(chat_id,"Enter Last Price For test:")
                        LASTPRICESIM.append('SimLastPrice')
                        self.coinbx(chat_id)
                    else:
                        bot.sendMessage(chat_id, "Enable Sim test Mode first /enableSimtest !!")
                elif 'SetLastPrice' in LASTPRICESIM and 'SimLastPrice' in LASTPRICESIM:
                    bot.sendChatAction(chat_id, 'typing')
                    Last = msg['text']
                    if is_number(Last) == True:
                        ST = Update_Last_Price(str(Last), Coin, 'bxinth')
                        if ST == "OK":
                            bot.sendMessage(chat_id, "Sim LastPrice " + Coin + " at " + Last + " => Completed",
                                            reply_markup=mainmenu)
                    LASTPRICESIM.clear()
                    Coin = ""
                elif 'SimLastPrice' in LASTPRICESIM:
                    bot.sendChatAction(chat_id, 'typing')
                    Coin = msg['text']
                    Coin = check_sys("data=" + Coin + ";echo ${data#*/}")
                    print("Data Set Lasprice 0 =" + Coin)
                    if simtest == "yes":
                        print("Data Set Lasprice 1 =" + Coin + "  Simtest =" + simtest)
                        Coin = Coin + "/THB"
                        # LASTPRICESIM.clear()
                        print("Data Set Lasprice =" + Coin)
                        bot.sendMessage(chat_id, "Now Sim Last Price:/" + str(get_lastprice_sim(str(Coin), 'bxinth')) + "\
                        \nEnter New Last Price for test:", reply_markup=hide_keyboard)
                        LASTPRICESIM.append('SetLastPrice')

                if msg['text'] == '/cancel' or msg['text'] == "CANCEL":
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, "\U00002714 Cancel all action-> OK ")
                    BX.clear()
                    CKCOMMAND.clear()
                    COINTEMP.insert(0, "")
                    CKCOMMAND.clear()
                    COINLISTINFO.clear()
                    CKLOSS.clear()
                    ORDERBUY.clear()
                    STRATEGY.clear()
                    NOTISTATE_ACTION.clear()
                    UPDATE_ACT.clear()
                    SELL_ORDER.clear()
                    Coin = ""
                    self.coinmenu(chat_id)
                #### SHOW TASK ###
                if msg['text'] == "TASK ORDER" or msg['text'] == "/TaskOrder":
                    bot.sendMessage(chat_id,"|=== TASK ORDER ==|")
                    self.taskorder('bxinth',chat_id)
                if msg['text'] == "/balance" or msg['text'] == "BALANCE":
                    self.coinbx(chat_id)
                    COUNT=0
                    CKBALANCE.append('BALANCE')
                elif 'BALANCE' in CKBALANCE:
                    bot.sendChatAction(chat_id, 'typing')
                    INFO=""
                    coin=msg['text']
                    if COUNT >= 2:
                        bot.sendMessage(chat_id,"Over repeat command ,Please wait few second !!")
                        time.sleep(10)
                        COUNT=0
                    ST = get_balance(bxin,"THB") ## MArket main
                    if ST == 201:
                        bot.sendMessage(chat_id,"THB Balance Not Available !!")
                    else:
                        INFO+=("+- Balance Available -+\n"+ST)
                        #bot.sendMessage(chat_id," Balance Available\n" + ST)
                    #--------------#
                    ST = get_balance(bxin, coin)
                    if ST == 201:
                        bot.sendMessage(chat_id,coin+ " Balance Not Available !!")
                    else:
                        INFO+=""+ST
                        bot.sendMessage(chat_id,INFO)
                    COUNT+=1
                    #print(INFO)
                ########### Allow Take Action Sell Coin ####
                if msg['text'] == "OK" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION \
                        or msg['text'] == "/OK" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION:
                    allow_cutloss_bts = "YES"
                    allow_stoploss_bts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_update_bts = "NO"
                    allow_update_sts = "NO"
                    print("Allow CutLoss =>"+allow_cutloss_bts)
                elif msg['text'] == "OK" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION \
                        or msg['text'] == "/OK" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION:
                    allow_stoploss_bts = "YES"
                    allow_cutloss_bts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_update_bts = "NO"
                    allow_update_sts = "NO"
                    print("Allow StopLoss =>" + allow_stoploss_bts)
                elif msg['text'] == "OK" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION \
                        or msg['text'] == "/OK" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION:
                    allow_update_bts = "YES"
                    allow_stoploss_bts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_update_sts = "NO"
                    print("allow Update bts sell =>" + allow_update_bts)
            ##################
                elif msg['text'] == "OK" and noti_sts == "ON" and 'sts_cutloss' in NOTISTATE_ACTION \
                        or msg['text'] == "/OK" and noti_sts == "ON" and 'sts_cutloss' in NOTISTATE_ACTION:
                    allow_cutloss_sts = "YES"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    print("allow Cutloss =>"+allow_cutloss_sts)
                elif msg['text'] == "OK" and noti_sts == "ON" and 'sts_stoploss' in NOTISTATE_ACTION \
                        or msg['text'] == "/OK" and noti_sts == "ON" and 'sts_stoploss' in NOTISTATE_ACTION:
                    allow_stoploss_sts = "YES"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    print("allow Stoploss =>" + allow_stoploss_sts)
                elif msg['text'] == "OK" and noti_sts == "ON" and 'sts_update' in NOTISTATE_ACTION \
                        or msg['text'] == "/OK" and noti_sts == "ON" and 'sts_update' in NOTISTATE_ACTION:
                    allow_update_sts="YES"
                    allow_update_bts="NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("allow Update sts sell =>" + allow_update_sts)

                ########
                #### Allow Take Action Update Point ###
                #########
                if msg['text'] == "UPDATE" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION \
                    or msg['text'] == "/UPDATE" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION:
                    UPDATE_ACT.append("UpdateAct")
                    bot.sendMessage(chat_id, "Enter new Stop Point:")
                    NOTISTATE_ACTION.append('StopPoint_Update')
                    allow_close_sts = "NO"
                    allow_close_bts = "NO"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("Allow CutLoss Point Sell =>" + allow_update_point_bts)
                elif msg['text'] == "UPDATE" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION \
                    or msg['text'] == "/UPDATE" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION:
                    bot.sendMessage(chat_id,"Enter new Stop Point:")
                    NOTISTATE_ACTION.append('StopPoint_Update')
                    UPDATE_ACT.append("UpdateAct")
                    allow_close_sts = "NO"
                    allow_close_bts = "NO"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("Allow Update StopLoss Point =>" + allow_update_point_bts)


                elif msg['text'] == "UPDATE" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION \
                    or msg['text'] == "/UPDATE" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION:
                    UPDATE_ACT.append("UpdateAct")
                    bot.sendMessage(chat_id, "Enter new Stop Point:")
                    NOTISTATE_ACTION.append('StopPoint_Update')
                    allow_close_sts = "NO"
                    allow_close_bts = "NO"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("allow Update bts Point sell =>" + allow_update_point_bts)
                ################## STS Update ####
                elif msg['text'] == "UPDATE" and noti_sts == "ON" and 'sts_cutloss' in NOTISTATE_ACTION \
                    or msg['text'] == "/UPDATE" and noti_sts == "ON" and 'sts_cutloss' in NOTISTATE_ACTION:
                    bot.sendMessage(chat_id, "Enter new Stop Point:")
                    NOTISTATE_ACTION.append('StopPoint_Update')
                    UPDATE_ACT.append("UpdateAct")
                    allow_close_sts = "NO"
                    allow_close_bts = "NO"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("allow Cutloss Update Point =>" + allow_update_point_sts)
                elif msg['text'] == "UPDATE" and noti_sts == "ON" and 'sts_stoploss' in NOTISTATE_ACTION \
                    or msg['text'] == "/UPDATE" and noti_sts == "ON" and 'sts_stoploss' in NOTISTATE_ACTION:
                    bot.sendMessage(chat_id, "Enter new Stop Point:")
                    NOTISTATE_ACTION.append('StopPoint_Update')
                    UPDATE_ACT.append("UpdateAct")
                    allow_close_sts = "NO"
                    allow_close_bts = "NO"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("allow StopLoss Update Poine =>" + allow_update_point_sts)
                elif msg['text'] == "UPDATE" and noti_sts == "ON" and 'sts_update' in NOTISTATE_ACTION \
                    or msg['text'] == "/UPDATE" and noti_sts == "ON" and 'sts_update' in NOTISTATE_ACTION:
                    UPDATE_ACT.append("UpdateAct")
                    bot.sendMessage(chat_id, "Enter new Stop Point:")
                    NOTISTATE_ACTION.append('StopPoint_Update')
                    allow_close_sts="NO"
                    allow_close_bts="NO"
                    #------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("allow Update Point sell =>" + allow_update_point_sts)
                elif 'StopPoint_Update' in NOTISTATE_ACTION:
                    StopLoss = msg['text']
                    if is_number(StopLoss) == True:
                        bot.sendMessage(chat_id, "Enter new CutLoss Point:")
                        NOTISTATE_ACTION.pop()
                        NOTISTATE_ACTION.append('CutlossPoint_Update')
                    else:
                        bot.sendMessage(chat_id, "Enter number only !!\nEnter new Stop Point:")
                elif "CutlossPoint_Update" in NOTISTATE_ACTION:
                    CutLoss = msg['text']
                    if is_number(CutLoss) == True:
                        bot.sendMessage(chat_id,"Apply to Order:")
                        NOTISTATE_ACTION.pop()
                        NOTISTATE_ACTION.append("ApplyUpdate")
                    else:
                        bot.sendMessage(chat_id, "Enter number only \n Enter New CutLoss Point:")
                elif "ApplyUpdate" in NOTISTATE_ACTION:
                    order_id = msg['text']
                    order_id = check_sys("data=" + order_id + ";echo ${data#*/}")
                    if is_number(order_id) == True:
                        CK = Update_StopLoss(order_id, 'bxinth', StopLoss)
                        if CK == "OK":
                            CK = Update_CutLoss(order_id, 'bxinth', CutLoss)
                            if CK == "OK":
                                bot.sendMessage(chat_id, "New Stop Loss Point:" + StopLoss + " %\
                        \nNew CutLoss Point:" + CutLoss + " % \
                        \n Update Order "+str(order_id)+" => Completed")
                        NOTISTATE_ACTION.clear()
                        UPDATE_ACT.clear()
                        time.sleep(1)
                    else:
                        NOTISTATE_ACTION.clear()
                        UPDATE_ACT.clear()

                        #####################
                    ########
                #### Allow Take Action Close Order ###
                    #########
                if msg['text'] == "CLOSE" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION \
                            or msg['text'] == "/CLOSE" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION:
                    bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                    NOTISTATE_ACTION.append("CloseOrder")
                    allow_close_sts = "NO"
                    allow_close_bts = "YES"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("Allow to CLose Order =>" + allow_close_bts)
                elif msg['text'] == "CLOSE" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION \
                            or msg['text'] == "/CLOSE" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION:
                    bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                    NOTISTATE_ACTION.append("CloseOrder")
                    allow_close_sts = "NO"
                    allow_close_bts = "YES"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("Allow to CLose Order =>" + allow_close_bts)
                elif msg['text'] == "CLOSE" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION \
                            or msg['text'] == "/CLOSE" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION:
                    bot.sendMessage(chat_id,"Enter OrderID:",reply_markup=mainmenu)
                    NOTISTATE_ACTION.append("CloseOrder")
                    allow_close_sts = "NO"
                    allow_close_bts = "YES"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("Allow to CLose Order =>" + allow_close_bts)
                elif "CloseOrder" in NOTISTATE_ACTION:
                     order_id=msg['text']
                     order_id = check_sys("data=" + order_id + ";echo ${data#*/}")
                     noti_bts = "ON"
                     # allow_cutloss = "NO"
                     if is_number(order_id) == True:
                        CK = Update_OrderBuy(order_id, 'bxinth', 'Close')
                        if CK == "OK":
                             bot.sendMessage(chat_id, "Close Order " + order_id + " =>" + CK)
                        else:
                             bot.sendMessage(chat_id, "Close Order " + order_id + " =>" + CK)
                        allow_close_bts = "NO"
                        NOTISTATE_ACTION.clear()
                        NOTISTS_INFO=""
                     else:
                        bot.sendMessage(chat_id, "Enter Number only !!, \
                        \nEnter OrderID:", reply_markup=mainmenu)

                ################## STS Update ####
                if msg['text'] == "CLOSE" and noti_sts == "ON" and 'sts_cutloss' in NOTISTATE_ACTION \
                            or msg['text'] == "/CLOSE" and noti_sts == "ON" and 'sts_cutloss' in NOTISTATE_ACTION:
                    bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                    NOTISTATE_ACTION.append("CloseOrder")
                    allow_close_sts = "YES"
                    allow_close_bts = "NO"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("Allow to CLose Order =>" + allow_close_sts)
                elif msg['text'] == "CLOSE" and noti_sts == "ON" and 'sts_stoploss' in NOTISTATE_ACTION \
                            or msg['text'] == "/CLOSE" and noti_sts == "ON" and 'sts_stoploss' in NOTISTATE_ACTION:
                    bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                    NOTISTATE_ACTION.append("CloseOrder")
                    allow_close_sts = "YES"
                    allow_close_bts = "NO"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("Allow to CLose Order =>" + allow_close_sts)
                elif msg['text'] == "CLOSE" and noti_sts == "ON" and 'sts_update' in NOTISTATE_ACTION \
                            or msg['text'] == "/CLOSE" and noti_sts == "ON" and 'sts_update' in NOTISTATE_ACTION:
                    bot.sendMessage(chat_id, "Enter OrderID:",reply_markup=mainmenu)
                    NOTISTATE_ACTION.append("CloseOrder")
                    allow_update_point_sts = "NO"
                    allow_update_point_bts = "NO"
                    allow_close_sts = "YES"
                    allow_close_bts = "NO"
                    # ------------------#
                    allow_update_sts = "NO"
                    allow_update_bts = "NO"
                    allow_stoploss_sts = "NO"
                    allow_cutloss_sts = "NO"
                    allow_cutloss_bts = "NO"
                    allow_stoploss_bts = "NO"
                    print("Allow to CLose Order =>" + allow_close_sts)

                elif "CloseOrder" in NOTISTATE_ACTION:
                    order_id = msg['text']
                    order_id = check_sys("data=" + order_id + ";echo ${data#*/}")
                    noti_bts = "ON"
                    # allow_cutloss = "NO"
                    if is_number(order_id) == True:
                        CK = Update_OrderSale(order_id, 'bxinth', 'Close')
                        if CK == "OK":
                            bot.sendMessage(chat_id, "Close Order " + order_id + " =>" + CK)
                        else:
                            bot.sendMessage(chat_id, "Close Order " + order_id + " =>" + CK)
                        allow_close_sts = "NO"
                        NOTISTS_INFO = ""
                        NOTISTATE_ACTION.clear()
                    else:
                        bot.sendMessage(chat_id,"Enter Number only !!, \
                        \nEnter OrderID:",reply_markup=mainmenu)
                        #####################
                ### SELL ORDER ####
                if msg['text'] == 'SELL ORDER':
                    bot.sendMessage(chat_id,'Enter Order:')
                    SELL_ORDER.append('SELL') ## DEV
                elif 'SELL' in SELL_ORDER:
                     Order=msg['text']
                     Order=check_sys("data=" + Order + ";echo ${data#*/}")
                     if is_number(Order) == True:
                        self.sellorder('bxinth',Order,chat_id)
                        SELL_ORDER.clear()
                     else:
                         bot.sendMessage(chat_id,"Enter Number only !!\n Enter Order:")

                #####################
                if msg['text'] == '/Notification' or msg['text'] == "NOTIFICATION":
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, "\
                    \n\U0001F534 /On_BTS \
                    \n\U0001F534 /Off_BTS \
                    \n\U0001F534 /On_STS \
                    \n\U0001F534 /Off_STS")
                if msg['text'] == "/On_BTS" or msg['text'] == "/Off_BTS" or msg['text'] == "/On_STS" \
                        or msg['text'] == "/Off_STS":
                    if msg['text'] == "/On_BTS":
                        noti_bts = "ON"
                        bot.sendMessage(chat_id, "On Notification Buy shadows Stop (BTS) --> OK")
                    if msg['text'] == "/Off_BTS":
                        noti_bts = "OFF"
                        bot.sendMessage(chat_id, "Off Notification Buy shadows Stop (BTS) --> OK")
                    if msg['text'] == "/On_STS":
                        noti_sts = "ON"
                        bot.sendMessage(chat_id, "On Notification Sell shadows Stop (STS) --> OK")
                    if msg['text'] == "/Off_STS":
                        noti_sts = "OFF"
                        bot.sendMessage(chat_id, "Off Notification Sell shadows Stop (STS) --> OK")

                if msg['text'] == '/menu':
                    self.coinmenu(chat_id)

                if msg['text'] == "/BXINTH" or msg['text'] == "BXINTH":
                    EX.append('BXINTH')

                if 'BXINTH' in EX and '/buyCoin' in CKCOMMAND or 'BXINTH' in EX and "BUY" in CKCOMMAND:
                    bot.sendChatAction(chat_id, 'typing')
                    BX.append('bxinth')
                    BX.append('buyCoin')
                    self.coinbx(chat_id)
                    CKCOMMAND.clear()
                    EX.clear()
                elif 'BXINTH' in EX and '/saleCoin' in CKCOMMAND or 'BXINTH' in EX and "SELL" in CKCOMMAND:
                    bot.sendChatAction(chat_id, 'typing')
                    BX.append('bxinth')
                    BX.append('saleCoin')
                    self.coinbx(chat_id)
                    CKCOMMAND.clear()
                    EX.clear()
                elif 'BXINTH' in EX and '/cancelCoin' in CKCOMMAND or 'BXINTH' in EX and "CANCEL ORDER" in CKCOMMAND:
                    bot.sendChatAction(chat_id, 'typing')
                    BX.append('bxinth')
                    BX.append('cancelCoin')
                    self.coinbx(chat_id)
                    CKCOMMAND.clear()
                    EX.clear()
                elif 'BXINTH' in EX and '/ckCoinInfo' in CKCOMMAND or 'BXINTH' in EX and "INFO" in CKCOMMAND:
                    bot.sendChatAction(chat_id, 'typing')
                    BX.append('bxinth')
                    BX.append('coinInfo')
                    self.coinbx(chat_id)
                    CKCOMMAND.clear()
                    EX.clear()


                    ### Check Coin infomation Buy coin and##
                if msg['text'] == '/buyCoin' or msg['text'] == '/ckCoinInfo' \
                        or msg['text'] == '/saleCoin' or msg['text'] == '/cancelCoin' \
                        or msg['text'] == 'BUY' or msg['text'] == 'SELL' \
                        or msg['text'] == 'CANCEL ORDER' or msg['text'] == 'INFO':
                    self.exchangemenu(chat_id, msg['text'])

                if 'coinInfo' in BX:
                    coin = msg['text']
                    coin = check_sys("data=" + coin + ";echo ${data#*/}")
                    market = "THB"
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, coin + "/" + market)))

                if msg['text'] == '/SELL' or msg['text'] == '/BUY' and 'bxinth' in BX or 'Cancel' in BX:
                    Coin = COINTEMP[0]
                    ST = ""
                    Order = msg['text']
                    Order = check_sys("data=" + Order + ";echo ${data#*/}")
                    if is_number(Order) == True and 'Cancel' in BX:
                        if cancel_coin(bxin, Order, Coin, 'bxinth') == True:
                            if simtest == "yes":
                                ST = ck_close_order_sim(Order, Coin, 'cancel', 'bxinth')
                            else:
                                ST = ck_close_order(bxin, Order, Coin, 'cancel', 'bxinth')
                            if ST == True:
                                bot.sendMessage(chat_id, "Cancel Order \"" + str(Order) + "\" => Completed",
                                                reply_markup=mainmenu)
                                time.sleep(2)
                        else:
                            Update_OpenOrder(Order, 'bxinth', 'close')
                            if simtest == "yes":
                                ST = ck_close_order_sim(Order, Coin, 'cancel', 'bxinth')
                            else:
                                ST = ck_close_order(bxin, Order, Coin, 'cancel', 'bxinth')
                            if ST == True:
                                bot.sendMessage(chat_id, "Cancel Order \"" + str(Order) + "\" => Completed",
                                                reply_markup=mainmenu)
                                time.sleep(2)
                                # else:
                                # bot.sendMessage(chat_id,"Not found order to database,clear this order !!")
                    if msg['text'] == '/BUY' or 'Cancel' in BX and '/BUY' in CKCOMMAND:
                        ST = Get_BittrexOpen_Order('bxinth', 'buy', Coin)
                        Type = "buy"
                        CKCOMMAND.append('/BUY')
                    if msg['text'] == '/SELL' or 'Cancel' in BX and '/SELL' in CKCOMMAND:
                        ST = Get_BittrexOpen_Order('bxinth', 'sell', Coin)
                        Type = "sell"
                        CKCOMMAND.append('/SELL')
                    if (str(ST)) == "failed" or (str(ST)) == "()":
                        # bot.sendMessage(chat_id, "Order \"" + Type + "\" in " + Coin + " is Clear")
                        bot.sendMessage(chat_id, "Order is empty !!... ")
                        CKCOMMAND.clear()
                        BX.clear()
                        COINTEMP.insert(0, "")
                        self.coinmenu(chat_id)
                    else:
                        Can = "|== Order Result " + Type + " ==| \n"
                        for order in list(ST):
                            date = (order[2])
                            order_id = (order[1])
                            coin = (order[3])
                            rate = (order[5])
                            qty = (order[6])
                            total = (order[7])
                            Can += ("OrderID:/" + order_id + "\nCoin:" + coin + "\nRate:" + str(rate) + "\nQty:" + str(
                                qty) + "\nTotal:" + str(total) + "\n ------------- \n")
                        bot.sendMessage(chat_id, str(Can))
                        bot.sendMessage(chat_id, "Enter OrderId ", reply_markup=cancelmarkup)
                        BX.append('Cancel')

                if 'bxinth' in BX and 'SELL' in BX:
                    bot.sendChatAction(chat_id, 'typing')
                    Coin = COINTEMP[0]
                    Rate = msg['text']
                    Rate = check_sys("data=" + Rate + ";echo ${data#*/}")
                    print("DEBUG1:Rate price" + str(Rate))
                    if is_number(Rate) == True and Rate != "0":
                        Oid = (sale_coin_res(Coin, float(Sell), float(Rate), 'bxinth'))  ## Open order sell temporary
                        if Oid == None:
                            Oid = 0
                        if is_number(Oid) == True:  ## Test
                            bot.sendMessage(chat_id, "Sell:" + Coin + "\nAmount:" + str(Sell) + "  \nRate:" + str(
                                Rate) + " Bath \n")
                            bot.sendMessage(chat_id, "Open Order " + str(Oid) + " --> Successfully")

                            ## Check Balance after Order ##
                            if simtest != "yes":
                                symbol = check_sys("data=" + Coin + ";echo ${data%/*}")
                                Bal = get_balance(bxin, symbol)
                                if Bal == 201:
                                    print(symbol + " Balance not available.!!")
                                    bot.sendMessage(chat_id, str(symbol + " Balance not available.!!"))
                                    BX.clear()

                                else:
                                    bot.sendMessage(chat_id, str(Bal))

                                CKCOMMAND.clear()
                                BX.clear()
                        else:
                            bot.sendMessage(chat_id, Oid)
                            CKCOMMAND.clear()
                            BX.clear()
                    else:
                        print("DEBUG2 " + str(is_number(Rate)))
                        bot.sendMessage(chat_id, "!! Enter number only and don't using rate = 0 ")
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, Coin)))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                    BX.clear()
                    COINTEMP.insert(0, "")

                if "bxinth" in BX and "BUY" in BX:
                    bot.sendChatAction(chat_id, 'typing')
                    Coin = COINTEMP[0]
                    Rate = msg['text']
                    Rate = check_sys("data=" + Rate + ";echo ${data#*/}")
                    print("Rate Debug" + str(Rate))
                    if is_number(Rate) == True and Rate != "0":
                        print("Rate1 " + str(Rate))
                        print("Coin1" + str(Coin))
                        print("Buy" + str(Buy))
                        bot.sendMessage(chat_id, "Processing .. ")
                        time.sleep(6)
                        if simtest == "yes":
                            Oid = (buy_coin_sim(Coin, float(Buy), float(Rate), 'bxinth'))
                        else:
                            Oid = (buy_coin(bxin, Coin, float(Buy), float(Rate), 'bxinth'))
                        print("Order ID:" + str(Oid))
                        if is_number(Oid) == True:  ## Test
                            bot.sendMessage(chat_id, "|= Result =|\
                            \nOrder:" + Oid + "\
                            \nBuy:" + Coin + "\
                            \nPrice:" + str(Buy) + " Bath \
                            \nRate:" + str(Rate) + " Bath \
                            \nQuality:" + str(format_float(float(Buy) / float(Rate))) + "\n" \
                                )
                            ORDERBUY.append(Coin)
                            ORDERBUY.append(Buy)
                            ORDERBUY.append(Rate)
                            ORDERBUY.append(str(format_float(float(Buy) / float(Rate))))

                            if simtest != "yes":
                                Bal = (get_balance(bxin, 'THB'))
                            else:
                                Bal = 202

                            if Bal == 201:
                                bot.sendMessage(chat_id, str("THB is balance not available.!!"))
                                BX.clear()
                                ORDERBUY.clear()
                            else:
                                bot.sendMessage(chat_id, "Open Order " + str(Oid) + "  --> Successfully")
                                BX.clear()
                                # bot.sendMessage(chat_id,"Enter /buyCoin command for continue trading ..")
                        else:
                            bot.sendMessage(chat_id, Oid)
                            BX.clear()

                    else:
                        bot.sendMessage(chat_id, "!! Enter number only and don't using rate = 0 ")
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, Coin)))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                    BX.clear()
                    COINTEMP.insert(0, "")

                ## SELECT COIN ##
                ### BTC BX ###
                if msg['text'] == '/BTC' and 'bxinth' in BX or msg['text'] == 'BTC' and 'bxinth' in BX:
                    COINTEMP.insert(0, "BTC/THB")
                    print("COIN =>" + COINTEMP[0])
                    Coin = COINTEMP[0]
                    print("MSG=" + msg['text'])
                    self.coin_buysalcan(chat_id, bxin, Coin)

                ## DASH BX ##
                elif msg['text'] == '/DASH' and 'bxinth' in BX or msg['text'] == 'DASH' and 'bxinth' in BX:
                    COINTEMP.insert(0, "DASH/THB")
                    Coin = COINTEMP[0]
                    print("MSG=" + msg['text'])
                    self.coin_buysalcan(chat_id, bxin, Coin)

                ## LTC BX ##
                elif msg['text'] == '/LTC' and 'bxinth' in BX or msg['text'] == 'LTC' and 'bxinth' in BX:
                    COINTEMP.insert(0, "LTC/THB")
                    Coin = COINTEMP[0]
                    self.coin_buysalcan(chat_id, bxin, Coin)

                ## BCH BX ##
                elif msg['text'] == '/BCH' and 'bxinth' in BX or msg['text'] == 'BCH' and 'bxinth' in BX:
                    COINTEMP.insert(0, "BCH/THB")
                    Coin = COINTEMP[0]
                    self.coin_buysalcan(chat_id, bxin, Coin)

                ## OMG BX ##
                elif msg['text'] == '/OMG' and 'bxinth' in BX or msg['text'] == 'OMG' and 'bxinth' in BX:
                    COINTEMP.insert(0, "OMG/THB")
                    Coin = COINTEMP[0]
                    self.coin_buysalcan(chat_id, bxin, Coin)
                ## REP BX ##
                elif msg['text'] == '/REP' and 'bxinth' in BX or msg['text'] == 'REP' and 'bxinth' in BX:
                    COINTEMP.insert(0, "REP/THB")
                    Coin = COINTEMP[0]
                    self.coin_buysalcan(chat_id, bxin, Coin)

                ## GNO BX ##
                elif msg['text'] == '/GNO' and 'bxinth' in BX or msg['text'] == 'GNO' and 'bxinth' in BX:
                    COINTEMP.insert(0, "GNO/THB")
                    Coin = COINTEMP[0]
                    self.coin_buysalcan(chat_id, bxin, Coin)

                ##  XZC BX ##
                elif msg['text'] == '/XZC' and 'bxinth' in BX or msg['text'] == 'XZC' and 'bxinth' in BX:
                    COINTEMP.insert(0, "XZC/THB")
                    Coin = COINTEMP[0]
                    self.coin_buysalcan(chat_id, bxin, Coin)

                ##  XRP BX ##
                elif msg['text'] == '/XRP' and 'bxinth' in BX or msg['text'] == 'XRP' and 'bxinth' in BX:
                    COINTEMP.insert(0, "XRP/THB")
                    Coin = COINTEMP[0]
                    self.coin_buysalcan(chat_id, bxin, Coin)
                ## ETH BX ##
                elif msg['text'] == '/ETH' and 'bxinth' in BX or msg['text'] == 'ETH' and 'bxinth' in BX:
                    COINTEMP.insert(0, "ETH/THB")
                    Coin = COINTEMP[0]
                    self.coin_buysalcan(chat_id, bxin, Coin)
                elif msg['text'] == '/EVX' and 'bxinth' in BX or msg['text'] == 'EVX' and 'bxinth' in BX:
                    COINTEMP.insert(0, "EVX/THB")
                    Coin = COINTEMP[0]
                    self.coin_buysalcan(chat_id, bxin, Coin)
                ## Check coin and take Action  
                elif 'buyCoin' in BX or 'saleCoin' in BX:
                    if COINTEMP[0] in BX:
                        Coin = COINTEMP[0]
                        print("DEBUG2 Coin =>" + str(Coin))
                        if 'buyCoin' in BX:
                            Buy = self.coin_buysalcanselect(chat_id, bxin, msg['text'], Coin)
                        if 'saleCoin' in BX:
                            Sell = self.coin_buysalcanselect(chat_id, bxin, msg['text'], Coin)

                #################################

                if msg['text'] == '/ckwan':
                    bot.sendChatAction(chat_id, 'typing')
                    sys_ck = check_sys("wget http://ipecho.net/plain -O - -q ; echo")
                    if sys_ck != "":
                        bot.sendMessage(chat_id, "\U0001F30F\U000026A1 Your ip wan is " + sys_ck)

                if msg['text'] == '/ckroomtemp':
                    bot.sendChatAction(chat_id, 'typing')
                    sys_ck = check_sys("bash /home/iams/iamsbot/bin/room_temperature")
                    if sys_ck != "":
                        bot.sendMessage(chat_id, "\U0001F6A8 Server Room temperature is " + sys_ck)

                if msg['text'] == '/asicDash' and chat_id not in setmail:
                    bot.sendChatAction(chat_id, 'typing')
                    sys_ck = check_sys("wget http://ipecho.net/plain -O - -q ; echo")
                    if sys_ck != "":
                        bot.sendMessage(chat_id, "\U0001F30F Click:http://" + sys_ck + ":4001")

                if chat_id in setmail:
                    bot.sendChatAction(chat_id, 'typing')
                    try:
                        global Email
                        Email = str(email(msg['text']))
                        if Email == "0":
                            Mail = msg['text']
                            ck_mail = str(send_mail(Mail, 'Test Send mail from bot'))
                            if ck_mail == "0":
                                bot.sendMessage(chat_id, "\U0001F4E7 Send Report to " + Mail + " Complete")
                                clearall(chat_id)
                        else:
                            bot.sendMessage(chat_id, "\U00002757 Email is invalid ,Please retype your email")
                    except:
                        bot.sendMessage(chat_id, "\U00002709 Please retype your email.")

                ### STRATEGY #####
                if msg['text'] == '/strategy' or msg['text'] == "STRATEGY":
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, "|== STRATEGY ==|\
                    \n /StopsShadows \
                    \n /CutlossShadows")

                elif msg['text'] == '/StopsShadows' or msg['text'] == "/CutlossShadows":
                    global SellStopLoss
                    global SellCutLoss
                    global BuyStopLoss
                    global BuyCutLoss
                    bot.sendChatAction(chat_id, 'typing')
                    if msg['text'] == '/StopsShadows':
                        bot.sendMessage(chat_id, "|-- STOP SHADOWS --| \
                        \n/NEW\
                        \n/UPDATE")
                        STRATEGY.append("StopsShadows")
                    if msg['text'] == "/CutlossShadows":
                        bot.sendMessage(chat_id, "|-- CUTLOSS SHADOWS --| \
                        \n/NEW\
                        \n/UPDATE")
                        STRATEGY.append("CutlossShadows")
                elif msg['text'] == "/NEW" and "CutlossShadows" in STRATEGY:
                    bot.sendMessage(chat_id, "What is Order to Apply,Please select !!\
                         \n/ORDER_BUY ")
                elif msg['text'] == "/UPDATE" and "CutlossShadows" in STRATEGY:
                    STRATEGY.clear()
                    bot.sendMessage(chat_id, "What is Order to Update,Please select !!\
                    \n/ORDER_BUY ")
                    STRATEGY.append("CutlossShadows_Update")
                elif msg['text'] == "/NEW" and "StopsShadows" in STRATEGY:
                    bot.sendMessage(chat_id, "What is Order to Apply,Please select !!\
                    \n/ORDER_BUY \
                    \n/ORDER_SELL")
                elif msg['text'] == "/UPDATE" and "StopsShadows" in STRATEGY:
                    STRATEGY.clear()
                    bot.sendMessage(chat_id, "What is Order to update,Please select !!\
                    \n/ORDER_BUY \
                    \n/ORDER_SELL")
                    STRATEGY.append("StopsShadows_Update")

                elif msg['text'] == "/ORDER_BUY" and "StopsShadows" in STRATEGY or msg[
                    'text'] == "/ORDER_SELL" and "StopsShadows" in STRATEGY \
                        or msg['text'] == "/ORDER_BUY" and "StopsShadows_Update" in STRATEGY or msg[
                    'text'] == "/ORDER_SELL" and "StopsShadows_Update" in STRATEGY:
                    if msg['text'] == "/ORDER_BUY":
                        SS = Get_OrderBuy('bxinth', 'buy')
                        print("OrderBuy => "+str(SS))
                        if str(SS) == "()":
                           bot.sendMessage(chat_id, "Not found Order for update !!! ..",reply_markup=mainmenu)
                           self.coinmenu(chat_id)
                           STRATEGY.clear()
                        else:
                           bot.sendMessage(chat_id, 'Enter OrderBuy Cut loss(%)', reply_markup=cancelmarkup)
                           CKLOSS.append('ckloss_buy')
                    if msg['text'] == "/ORDER_SELL":
                        SS = Get_OrderSale('bxinth', 'sell')
                        print("OrderSell =>"+str(SS))
                        if str(SS) == "()":
                           bot.sendMessage(chat_id, "Not found Order for update !!! ..",reply_markup=mainmenu)
                           self.coinmenu(chat_id)
                           STRATEGY.clear()
                        else:
                           bot.sendMessage(chat_id, 'Enter OrderSell Cut loss(%)', reply_markup=cancelmarkup)
                           CKLOSS.append('ckloss_sell')
                ##/DEV
                elif 'ckloss_buy' in CKLOSS:
                    CutLoss = msg['text']
                    if is_number(CutLoss) == True:
                        bot.sendMessage(chat_id, "Enter OrderBuy Stop loss(%)", reply_markup=cancelmarkup)
                        CKLOSS.remove('ckloss_buy')
                        CKLOSS.append('stoploss_buy')
                    else:
                        bot.sendMessage(chat_id, 'Enter number only !! \
                        \nEnter OrderBuy Cut loss(%)', reply_markup=cancelmarkup)
                elif 'ckloss_sell' in CKLOSS:
                    CutLoss = msg['text']
                    if is_number(CutLoss) == True:
                        bot.sendMessage(chat_id, "Enter OrderSell Stop loss(%)", reply_markup=cancelmarkup)
                        CKLOSS.remove('ckloss_sell')
                        CKLOSS.append('stoploss_sell')
                    else:
                        bot.sendMessage(chat_id, 'Enter number only !! \
                                \nEnter OrderSell Cut loss(%)', reply_markup=cancelmarkup)

                elif 'stoploss_buy' in CKLOSS and "StopsShadows_Update" in STRATEGY:
                    INFO = ""
                    StopLoss = msg['text']
                    # Coin = COINTEMP[0]
                    if is_number(StopLoss) == True:
                        BuyStopLoss = StopLoss
                        BuyCutLoss = CutLoss
                        # CKCOMMAND.append("ORDER BUY")
                        bot.sendMessage(chat_id, "Apply Order Buy to New order \
                               \n(%)StopLoss:" + str(BuyStopLoss) + " \
                               \n(%)CutLoss:" + str(BuyCutLoss) + " \
                               \n --------------- \
                               \n Next Step Update to your Order Buy as below!!!")
                        # self.exchangemenu(chat_id, "ORDER BUY")
                    SS = Get_OrderBuy('bxinth', 'buy')
                    for order in list(SS):
                        Time = (order[1])
                        order_id = (order[0])
                        coin = (order[2])
                        rate = (order[4])
                        qty = (order[3])
                        INFO += ("\nTrader BTS " + coin)
                        INFO += ("\n" + Time + "\
                        \nid:/" + str(order_id) + "\
                        \nCoin:" + coin + "\
                        \nQty:" + str(qty) + "\
                        \nRate:" + str(rate))
                        volumn = format_float(qty / rate)
                        INFO += ("\nVolumn: " + volumn)
                        StopLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Stoploss')
                        CutLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Cutloss')
                        INFO += ("\nStopLoss:" + str(StopLoss) + " %")
                        INFO += ("\nCutLoss:" + str(CutLoss) + " %")
                        INFO += ("\n----------------------")
                    bot.sendMessage(chat_id, INFO)
                    STRATEGY.append("UPDATE_NOW")
                    STRATEGY.append("stoploss_buy")
                    bot.sendMessage(chat_id, "Enter Order ID:")

                    CKLOSS.clear()
                    ORDERBUY.clear()
                    # STRATEGY.clear()
                elif 'stoploss_buy' in CKLOSS:
                    StopLoss = msg['text']
                    # Coin = COINTEMP[0]
                    if is_number(StopLoss) == True:
                        BuyStopLoss = StopLoss
                        BuyCutLoss = CutLoss
                        # CKCOMMAND.append("ORDER BUY")
                        bot.sendMessage(chat_id, "Apply Order Buy to New order \
                           \n(%)StopLoss:" + str(BuyStopLoss) + " \
                           \n(%)CutLoss:" + str(BuyCutLoss) + " \
                           \n --------------- \
                           \n Next Step Create New order to Buy !!!")
                        self.exchangemenu(chat_id, "BUY")
                        CKLOSS.clear()
                        ORDERBUY.clear()
                        STRATEGY.clear()
                    else:
                        bot.sendMessage(chat_id, 'Enter number only !! \
                            \nEnter OrderSell Stop loss(%)', reply_markup=cancelmarkup)

                        # ST = Insert_ckloss(Oid, 'bxinth', StopLoss, CutLoss, 0)
                        # if ST == "OK":
                        # ST = Insert_OrderBuy(Oid, 'bxinth', time.strftime('%Y-%m-%d %H:%M:%S'), ORDERBUY[0],
                        # ORDERBUY[1], ORDERBUY[2], 'buy')
                        # if ST == "OK":
                        #        bot.sendMessage(chat_id, "Apply strategy trailing stop to your order --> Completed !! ")
                        #        self.coinmenu(chat_id)
                        #    else:
                        #        bot.sendMessage(chat_id, "!! Apply strategy trailing stop to your order --> Failed !! ")
                        #        self.coinmenu(chat_id)
                elif 'stoploss_sell' in CKLOSS and "StopsShadows_Update" in STRATEGY:
                    INFO = ""
                    StopLoss = msg['text']
                    if is_number(StopLoss) == True:
                        SellStopLoss = StopLoss
                        SellCutLoss = CutLoss
                        # CKCOMMAND.append("ORDER SELL")
                        bot.sendMessage(chat_id, "Apply Order Sell to new order \
                               \n(%)StopLoss:" + str(SellStopLoss) + " \
                               \n(%)CutLoss:" + str(SellCutLoss) + " \
                               \n --------------- \
                               \n Next step,Update to your Order Sell as below !!!")
                        # self.exchangemenu(chat_id, "ORDER SELL")
                    SS = Get_OrderSale('bxinth', 'sell')
                    for order in list(SS):
                        Time = (order[1])
                        order_id = (order[0])
                        coin = (order[2])
                        rate = (order[4])
                        qty = (order[3])
                        INFO += ("\nTrader STS" + coin)
                        INFO += ("\n" + Time + "\
                        \nid:/" + str(order_id) + "\
                        \nCoin:" + coin + "\
                        \nQty:" + str(qty) + "\
                        \nRate:" + str(rate))
                        volumn = format_float(qty / rate)
                        INFO += ("\nVolumn:" + volumn)
                        StopLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Stoploss')
                        CutLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Cutloss')
                        INFO += ("\nStopLoss:" + str(StopLoss) + " %")
                        INFO += ("\nCutLoss:" + str(CutLoss) + " %")
                        INFO += ("\n-------------------")
                    bot.sendMessage(chat_id, INFO)

                    STRATEGY.append("UPDATE_NOW")
                    STRATEGY.append("stoploss_sell")
                    bot.sendMessage(chat_id, "Enter Order ID:")
                    # STRATEGY.clear()
                    CKLOSS.clear()
                    ORDERBUY.clear()
                    # STRATEGY.clear()
                elif "UPDATE_NOW" in STRATEGY:
                    INFO=""
                    Order = msg['text']
                    Uid = check_sys("data=" + Order + ";echo ${data#*/}")
                    print("Order ID " + Uid)
                    if is_number(Uid) == True:
                        if "stoploss_sell" in STRATEGY:
                            INFO=""
                            ST1 = Update_StopLoss(Uid, 'bxinth', SellStopLoss)
                            ST2 = Update_CutLoss(Uid, 'bxinth', SellCutLoss)
                            if ST1 == "OK" and ST2 == "OK":
                                bot.sendMessage(chat_id, "Update New value Completed !!", reply_markup=mainmenu)
                                SS = Get_OrderSale('bxinth', 'sell')
                                for order in list(SS):
                                    Time = (order[1])
                                    order_id = (order[0])
                                    coin = (order[2])
                                    rate = (order[4])
                                    qty = (order[3])
                                    if order_id != Uid:
                                        continue
                                    else:
                                        INFO += ("\nUpdate Trader STS New!!\n Coin:"+ coin)
                                        INFO += ("\n" + Time + "\
                                        \nid:/" + str(order_id) + "\
                                        \nCoin:" + coin + "\
                                        \nQty:" + str(qty) + "\
                                        \nRate:" + str(rate))
                                        volumn = format_float(qty / rate)
                                        INFO += ("\nVolumn:" + volumn)
                                        StopLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Stoploss')
                                        CutLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Cutloss')
                                        INFO += ("\nStopLoss:" + str(StopLoss) + " %")
                                        INFO += ("\nCutLoss:" + str(CutLoss) + " %")
                                        INFO += ("\n-------------------")
                                        bot.sendMessage(chat_id, INFO)
                            else:
                                bot.sendMessage(chat_id, "Update New value Failed !!", reply_markup=mainmenu)
                        elif "stoploss_buy" in STRATEGY:
                            INFO=""
                            ST1 = Update_StopLoss(Uid, 'bxinth', BuyStopLoss)
                            ST2 = Update_CutLoss(Uid, 'bxinth', BuyCutLoss)
                            if ST1 == "OK" and ST2 == "OK":
                                bot.sendMessage(chat_id, "Update New value Completed !!", reply_markup=mainmenu)
                                SS = Get_OrderBuy('bxinth', 'buy')
                                for order in list(SS):
                                    Time = (order[1])
                                    order_id = (order[0])
                                    coin = (order[2])
                                    rate = (order[4])
                                    qty = (order[3])
                                    if order_id != Uid:
                                        continue
                                    else:
                                        print("Order ID Update "+Uid)
                                        INFO += ("\nUpdate Trader BTS New!!\nCoin:" + coin)
                                        INFO += ("\n" + Time + "\
                                            \nid:/" + str(order_id) + "\
                                            \nCoin:" + coin + "\
                                            \nQty:" + str(qty) + "\
                                            \nRate:" + str(rate))
                                        volumn = format_float(qty / rate)
                                        INFO += ("\nVolumn:" + volumn)
                                        StopLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Stoploss')
                                        CutLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Cutloss')
                                        INFO += ("\nStopLoss:" + str(StopLoss) + " %")
                                        INFO += ("\nCutLoss:" + str(CutLoss) + " %")
                                        INFO += ("\n-------------------")
                                        bot.sendMessage(chat_id, INFO)
                            else:
                                bot.sendMessage(chat_id, "Update New value Failed !!", reply_markup=mainmenu)

                    else:
                        bot.sendMessage(chat_id, "Error Not found Uid !!")
                    CKLOSS.clear()
                    ORDERBUY.clear()
                    STRATEGY.clear()

                elif 'stoploss_sell' in CKLOSS:
                    StopLoss = msg['text']
                    if is_number(StopLoss) == True:
                        SellStopLoss = StopLoss
                        SellCutLoss = CutLoss
                        # CKCOMMAND.append("ORDER SELL")
                        bot.sendMessage(chat_id, "Apply Order Sell to new order \
                           \n(%)StopLoss:" + str(SellStopLoss) + " \
                           \n(%)CutLoss:" + str(SellCutLoss) + " \
                           \n --------------- \
                           \n Next step,Create New Order to Sell !!!")
                        self.exchangemenu(chat_id, "SELL")
                        CKLOSS.clear()
                        ORDERBUY.clear()
                        STRATEGY.clear()
                    else:
                        bot.sendMessage(chat_id, 'Enter number only !! \
                            \nEnter OrderSell Stop loss(%)', reply_markup=cancelmarkup)


                ####### END STRATEGY ###
               # if STRATEGY_CHECK == "ON":
                   #simtest="yes"
               #    print("Strategy Check Working --> Now")
               #    self.bts('bxinth', chat_id)
               #    self.sts('bxinth',chat_id)
               #    self.check_close_order('bxinth',chat_id)

                ## Algorithm Statigy ###
    def sellorder(self,exchange,order_sell,chat_id):
        order_id=""
        ST = Get_OrderBuy(exchange, 'buy')
        if ST == "()":
            return False
        for order in list(ST):
            Time = (order[1])
            order_id = (order[0])
            coin = (order[2])
            rate = (order[4])
            qty = (order[3])
            if order_sell == order_id:
                break
            else:
                 continue
        if order_sell == order_id:
            print("Order Sell " + coin)
            print("" + Time + \
              "\nOid:" + str(order_id) + \
              "\nCoin" + coin + \
              "\nQty" + str(qty) + \
              "\nRate:" + str(rate))
            volumn = format_float(qty / rate)
            if simtest == "yes":
                lastprice = get_lastprice_sim(str(coin), exchange)
            else:
                lastprice = get_lastprice(bxin, str(coin))
            if is_number(lastprice) == True and order_id != 0 and order_id != None:
                if simtest == "yes":
                    fee = 0.0025
                    volumn = format_float(float(volumn) - (float(volumn) * fee))
                    ST = sale_coin_sim(coin, float(volumn), float(lastprice), exchange)
                    if is_number(ST) == True:
                        profit = (((lastprice / rate) * qty) - qty)
                        profit_fee = (profit - (profit * fee))
                        bot.sendMessage(chat_id, "!!Sell Direct Completed !!\
                         \nCoin:" + coin + "\
                         \nOrder:" + str(order_id) + "\
                         \nBuy:" + str(qty) + "\
                         \nSold:" + str(format_float(((lastprice / rate) * qty))) + "\
                         \nChange Fee " + str(fee) + "\
                         \nProfit " + str(format_float(profit_fee)) + "Bath", reply_markup=mainmenu)
                        CK = Update_OrderBuy(order_id, exchange, 'sold')
                        if CK == "OK":
                            bot.sendMessage(chat_id, 'Update Status Sold Out =>' + CK)
                        else:
                            bot.sendMessage(chat_id, 'Update Status Sold Out =>' + CK)
                else:
                    fee = 0.0025
                    volumn = format_float(float(volumn) - (float(volumn) * fee))
                    ST = sale_coin(bxin, coin, float(volumn), float(lastprice), exchange)
                    if is_number(ST) == True:
                        profit = (((lastprice / rate) * qty) - qty)
                        profit_fee = (profit - (profit * fee))
                        bot.sendMessage(chat_id, "!!Sell Direct Completed !!\
                             \nCoin:" + coin + "\
                             \nOrder:" + str(order_id) + "\
                             \nBuy:" + str(qty) + "\
                             \nSold:" + str(format_float(((lastprice / rate) * qty))) + "\
                             \nChange Fee " + str(fee) + "\
                             \nProfit " + str(format_float(profit_fee)) + "Bath", reply_markup=mainmenu)
                        CK = Update_OrderBuy(order_id, exchange, 'sold')
                        if CK == "OK":
                            bot.sendMessage(chat_id, 'Update Status Sold Out =>' + CK)
                        else:
                            bot.sendMessage(chat_id, 'Update Status Sold Out =>' + CK)
                        return True
        else:
            bot.sendMessage(chat_id,"Not Found Order "+order_id+",Please verify !!")
            return False


    def taskorder(self,exchange,chat_id):
        order_id = ""
        bts=True
        sts=True
        INFO=""
        fee=0.00025
        ST = Get_OrderBuy(exchange, 'buy')
        if str(ST) != "()":
            for order in list(ST):
                Time = (order[1])
                order_id = (order[0])
                coin = (order[2])
                rate = (order[4])
                qty = (order[3])
                #--------#
                volumn = format_float(qty / rate)
                StopLoss = Get_BittrexDB(order_id,exchange, 'ckloss', 'Stoploss')
                CutLoss = Get_BittrexDB(order_id,exchange, 'ckloss', 'Cutloss')
                if simtest == "yes":
                    lastprice = get_lastprice_sim(str(coin), exchange)
                else:
                    lastprice = get_lastprice(bxin, str(coin))
                StopLoss_Point = lastprice - (lastprice * (StopLoss / 100))
                CutLossPrice = (rate - (rate * (CutLoss / 100)))
                MinProfit = (rate + (rate * (StopLoss / 100)))
                print("Start Cost =>" + str(rate) + " Price Up =>" + str(lastprice - rate) + " (+/-) =>" + str(
                (100 * (lastprice - rate)) / rate) + "%")
                profit = (((StopLoss_Point / rate) * qty) - qty)
                profit_last = (((lastprice / rate) * qty) - qty)
                profit_fee = (profit - (profit * fee))
                profit_lastfee = (profit_last - (profit_last * fee))
                INFO+= ("BTS Strategy Running " + Coin + \
                             "\nStopLoss:" + str(StopLoss)+\
                             " %\nCutLoss:" + str(CutLoss)+ \
                             " %\nCutLossPrice:" + str(CutLossPrice) + \
                             "\nMinimum Profit(Stop Point):"+ str(MinProfit) + \
                             "\nStart Rate =>" + str(rate) + \
                             "\nPrice Up =>" + str(lastprice - rate) + "(+/-) =>" + str((100 * (lastprice - rate)) / rate) + \
                             "%\n---------------- \
                              \nOrder:/" + str(order_id) + \
                             "\nBuy " + str(qty) + \
                             "\nRate " + str(rate) + \
                             "\nNow LastPrice:" + str(lastprice) + \
                             "\nNow StopPoint("+str(StopLoss)+" %):" + str(StopLoss_Point) + \
                             "\nChange Fee:" + str(fee) + \
                             "\nProfit(StopLoss):" + str(format_floatc(profit_fee,2)) + "  \
                              \nProfit(LastPrice):" + str(format_floatc(profit_lastfee,2)) + " \
                              \n----------------------")
        #bot.sendMessage(chat_id,INFO)
                print(INFO)
                bot.sendMessage(chat_id,INFO)
                INFO = ""
        else:
            bts=False
            #bot.sendMessage(chat_id,"No task Order BTS")

    #------STS------#
        ST = Get_OrderSale(exchange, 'sell')
        if str(ST) != "()":
            for order in list(ST):
                Time = (order[1])
                order_id = (order[0])
                coin = (order[2])
                rate = (order[4])
                qty = (order[3])
                # --------#
                volumn = format_float(qty / rate)
                StopLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Stoploss')
                CutLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Cutloss')
                if simtest == "yes":
                    lastprice = get_lastprice_sim(str(coin), exchange)
                else:
                    lastprice = get_lastprice(bxin, str(coin))
                StopLoss_Point = lastprice - (lastprice * (StopLoss / 100))
                CutLossPrice = (rate - (rate * (CutLoss / 100)))
                MinProfit = (rate + (rate * (StopLoss / 100)))
                print("Start Cost =>" + str(rate) + " Price Up =>" + str(lastprice - rate) + " (+/-) =>" + str(
                (100 * (lastprice - rate)) / rate) + "%")
                profit = (((StopLoss_Point / rate) * qty) - qty)
                profit_last = (((lastprice / rate) * qty) - qty)
                profit_fee = (profit - (profit * fee))
                profit_lastfee = (profit_last - (profit_last * fee))
                INFO += ("STS Strategy Running " + Coin + \
                             "\nStopLoss:" + str(StopLoss) + \
                             " %\nCutLoss:" + str(CutLoss) + \
                             " %\nCutLossPrice:" + str(CutLossPrice) + \
                             "\nMinimum Profit:" + str(MinProfit) + \
                             "\nStart Cost =>" + str(rate) + \
                             "\nPrice Up =>" + str(
                lastprice - rate) + "(+/-) =>" + str(
                (100 * (lastprice - rate)) / rate) + \
                             "%\n---------------------- \
                              \nOrder:/" + str(order_id) + \
                             "\nSale Volumn:" + str(volumn) + \
                             "\nStart Rate " + str(rate) + \
                             "\nNow LastPrice:" + str(lastprice) + \
                             "\nNow StopPoint(" + str(StopLoss) + " %):" + str(StopLoss_Point) + \
                             "\nChange Fee:" + str(fee) + \
                             "\nProfit(StopLoss):" + str(format_floatc(profit_fee,2)) +"\
                             \nProfit(LastPrice):" + str(format_floatc(profit_lastfee,2))+"")
        #bot.sendMessage(chat_id, INFO)
                print(INFO)
                bot.sendMessage(chat_id,INFO)
                INFO = ""
        else:
            sts=False
            #bot.sendMessage(chat_id,"No Task Order STS !!")
        if bts == False and sts == False :
            bot.sendMessage(chat_id,"Not found Task Order running !!")

    def bts(self, exchange, chat_id):

        global noti_bts
        global noti_sts
        global allow_cutloss_bts
        global allow_stoploss_bts
        global allow_update_bts
        global allow_update_point_bts
        global allow_close_bts
        global NOTIBTS_INFO
        result=""
        #global NOTISTATE_ACTION
        if exchange == 'bxinth':
            fee = 0.0025
        ST = Get_OrderBuy(exchange, 'buy')
        if ST == "()":
            return False
        for order in list(ST):
            Time = (order[1])
            order_id = (order[0])
            coin = (order[2])
            rate = (order[4])
            qty = (order[3])
            print("---------------------\n")
            print("Starting trader BTS " + coin)
            print("" + Time + \
                  "\nOid:" + str(order_id) + \
                  "\nCoin" + coin + \
                  "\nQty" + str(qty) + \
                  "\nRate:" + str(rate))
            volumn = format_float(qty / rate)
            print("Volumn: " + volumn)
            print("### Start Trailling Stop BTS " + coin + " ###")
            ## Lastprice for test ###
            if simtest == "yes":
                lastprice = get_lastprice_sim(str(coin), exchange)
            else:
                lastprice = get_lastprice(bxin, str(coin))
            if is_number(lastprice) == True and order_id != 0 and order_id != None:
                if simtest == "yes":
                    fee = 0.0025
                    volumn = format_float(float(volumn) - (float(volumn) * fee))
                    # print("Real Volume Sell Update" + str(float(volumn) - (float(volumn) * fee)))
                    if noti_bts == "ON" and allow_update_bts != "YES":
                        ST = "Noti"
                    elif noti_bts == "ON" and allow_update_point_bts == "YES":
                        bot.sendMessage(chat_id,"Update Order:/"+str(order_id)+"\n")
                    elif noti_bts == "OFF" or allow_update_bts == "YES":
                        ST = sale_coin_sim(coin, float(volumn), float(lastprice), exchange)
                else:
                    fee = 0.0025
                    volumn = format_float(float(volumn) - (float(volumn) * fee))
                    # print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))
                    if noti_bts == "ON" and allow_update_bts != "YES":
                        ST = "Noti"
                    elif noti_bts == "ON" and allow_update_point_bts == "YES":
                        bot.sendMessage(chat_id, "Update Order:/"+str(order_id) + "\n")
                    elif noti_bts == "OFF" or allow_update_bts == "YES":
                        ST = sale_coin(bxin, coin, float(volumn), float(lastprice), exchange)
                ## DEV##
                print("Sale update at " + str(lastprice) + " !!!")
                if allow_update_bts == "YES":
                    noti_bts = "ON"
                    # allow_cutloss = "NO"
                    CK = Update_OrderBuy(order_id, exchange, 'sold')
                    if CK == "OK":
                        bot.sendMessage(chat_id, 'Update Status Sold Out =>' + CK)
                    else:
                        bot.sendMessage(chat_id, 'Update Status Sold Out =>' + CK)
                ## Real Sale ###
                if is_number(ST) == True and allow_update_bts == "YES":
                    profit = (((lastprice / rate) * qty) - qty)
                    profit_fee = (profit - (profit * fee))
                    bot.sendMessage(chat_id, "!!Action Sell Update Completed \
                         \nCoin:" + coin + "\
                         \nOrder:" + str(order_id) + "\
                         \nBuy:" + str(qty) + "\
                         \nSold:" + str(format_floatc(((lastprice / rate) * qty),2)) + "\
                         \nChange Fee " + str(fee) + "\
                         \nProfit " + str(format_floatc(profit_fee,2)) + "Bath", reply_markup=mainmenu)
                        #print("Sale Update to Lastprice at " + str(lastprice) + " !!!")
                    allow_update_bts = "NO"
                    NOTIBTS_INFO = ""
                    continue


                if allow_update_bts != "YES":
                   result=buy_trailling_stop_shadow(order_id, exchange, lastprice, rate)
                   print("Status trailling =>" + str(result))
                if result != None:
                    if result[0] == "StopLossUpdate":
                        StopLoss_Point = result[1]
                        NOTIBTS_INFO += ("\n-------------------\
                              \n|= Update Point =|\
                              \nOrder:/" + order_id + "\
                              \nCoin:" + coin + "\
                              \nPrice:" + str(StopLoss_Point))
                        if ST == "Noti" and allow_update_bts == "NO":
                           NOTISTATE_ACTION.clear()
                           NOTISTATE_ACTION.append('bts_update')
                           print("!!! Update StopLoss Point at " + str(StopLoss_Point))
                           profit = (((StopLoss_Point / rate) * qty) - qty)
                           profit_last = (((lastprice / rate) * qty) - qty)
                           profit_fee = (profit - (profit * fee))
                           profit_lastfee = (profit_last - (profit_last * fee))
                           NOTIBTS_INFO+=("Update StopPoint BTS "+Coin+\
                                        "\nOrder:/" +str(order_id) + \
                                        "\nBuy " + str(qty) + \
                                        "\nRate " + str(rate) + \
                                        "\nNow LastPrice:" + str(lastprice) + \
                                        "\nNow StopPoin(" + str(result[2]) + " %):" + str(StopLoss_Point) + \
                                        "\nChange Fee:" + str(fee) + \
                                        "\nProfit(StopLoss):"+str(format_floatc(profit_fee,2))+ "  \
                                         \nProfit(LastPrice):"+str(format_floatc(profit_lastfee,2)) + " \
                                          ")
                    ##

                    if result[0] == "CutLoss":
                        CutLossPrice = result[1]
                        time.sleep(2)
                        if "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTIBTS_INFO+=(
                                        "|= CutLoss =| \
                                        \nOrder:/" + order_id + "\
                                        \nCoin:" + coin + "\
                                        \nPrice:" + str(CutLossPrice))
                        if simtest == "yes":
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                            print("Real Sim Volume Sell CutLoss " + str(float(volumn) - (float(volumn) * fee)))
                            # time.sleep(4)
                            if noti_bts == "ON" and allow_cutloss_bts != "YES":
                                ST = "Noti"
                            elif noti_bts == "OFF" or allow_cutloss_bts == "YES":
                                ST = sale_coin_sim(coin, float(volumn), float(CutLossPrice), exchange)
                        else:
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                            print("Real Volume Sell CutLoss " + str(float(volumn) - (float(volumn) * fee)))
                            # time.sleep(4)
                            if noti_bts == "ON" and allow_cutloss_bts != "YES":
                                ST = "Noti"
                            elif noti_bts == "OFF" or allow_cutloss_bts == "YES":
                                ST = sale_coin(bxin, coin, float(volumn), float(CutLossPrice), exchange)
                        if ST == "Noti" and allow_cutloss_bts == "NO" and "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('bts_cutloss')
                            profit = (((CutLossPrice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            NOTIBTS_INFO+=("\n -------------------- \
                                     \nPlease Take Action Cut Loss Now!! \
                                     \nCoin:"+coin+"\
                                     \nPercent " + str(result[2]) + " % \
                                     \nBuy " + str(qty) + "\
                                     \nSold " + str(format_floatc(((CutLossPrice / rate) * qty),2)) + "\
                                     \nChange Fee " + str(fee) + "\
                                     \nProfit " + str(format_floatc(profit_fee,2)) + " \
                                     \nAccept this Action or not ? \n/OK\n/CLOSE\n/UPDATE" \
                                      )
                            #time.sleep(4)
                            print("Sale Cut loss at " + str(CutLossPrice) + " !!!")
                        if allow_cutloss_bts == "YES":
                           noti_bts = "ON"
                           #allow_cutloss = "NO"
                           CK = Update_OrderBuy(order_id, exchange, 'sold')
                           if CK == "OK":
                              bot.sendMessage(chat_id, 'Update Action CutLoss Status =>' + CK)
                           else:
                              bot.sendMessage(chat_id, 'Update Action CutLoss Status =>' + CK)

                           allow_close_bts="NO"
                           NOTIBTS_INFO=""
                        ## Real Sale ###
                        if is_number(ST) == True and allow_cutloss_bts == "YES":
                            profit = (((CutLossPrice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            bot.sendMessage(chat_id, "!! Action Cut Loss at " + str(result[2]) + " % Completed \
                            \nCoin:"+coin+"\
                            \nOrder:"+str(order_id)+"\
                            \nBuy:" + str(qty) + "\
                            \nSold:" + str(format_floatc(((CutLossPrice / rate) * qty),2)) + "\
                            \nChange Fee " + str(fee) + "\
                            \nProfit " + str(format_floatc(profit_fee,2)) + " Bath",
                                            reply_markup=mainmenu)
                            print("Sale Cut loss at " + str(CutLossPrice) + " !!!")
                            allow_cutloss_bts="NO"
                            NOTIBTS_INFO=""
                            #CK = Update_OrderBuy(order_id, exchange, 'sold')
                            #if CK == "OK":
                            #    bot.sendMessage(chat_id, 'Update Status =>' + CK, reply_markup=mainmenu)
                            #else:
                            #    bot.sendMessage(chat_id, 'Update Status =>' + CK, reply_markup=mainmenu)

                    elif result[0] == "StopLoss":
                        LastPrice = result[1]
                        time.sleep(2)
                        if "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTIBTS_INFO+=(
                                        "\n|== StopLoss ==|\
                                        \nOrder:/" + order_id + "\
                                        \nCoin:" + coin + "\
                                        \nPrice:" + str(LastPrice))
                        if simtest == "yes":
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                            print("Real Volume Sell StopLoss" + str(float(volumn) - (float(volumn) * fee)))
                            # time.sleep(4)
                            if noti_bts == "ON" and allow_stoploss_bts != "YES":
                                ST = "Noti"
                            elif noti_bts == "OFF" or allow_stoploss_bts == "YES":
                                ST = sale_coin_sim(coin, float(volumn), float(LastPrice), exchange)
                        else:
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                            print("Real Volume Sell StopLoss" + str(float(volumn) - (float(volumn) * fee)))
                            #time.sleep(4)
                            if noti_bts == "ON" and allow_stoploss_bts != "YES" :
                                ST = "Noti"
                               # time.sleep(4)
                            elif noti_bts == "OFF" or allow_stoploss_bts == "YES":
                                ST = sale_coin(bxin, coin, float(volumn), float(LastPrice), exchange)
                        if ST == "Noti" and allow_stoploss_bts == "NO" and "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append("bts_stoploss")
                            profit = (((LastPrice / rate) * qty) - qty)
                            fee = 0.0025
                            profit_fee = (profit - (profit * fee))
                            NOTIBTS_INFO+=("\n--------------------- \
                            \nPlease Take Action StopLoss Now!!! \
                            \nCoin:"+coin+\
                            "\nBuy:" + str(qty)+\
                            "\nSold:" + str(format_floatc(((LastPrice / rate) * qty),2)) + "\
                            \nChange Fee " + str(fee) + "\
                            \nProfit " + str(format_floatc(profit_fee,2)) + " Bath \
                            \nAccept this Action or not? \n/OK\n/CLOSE\n/UPDATE")
                            print("Sale Stop loss at " + str(LastPrice) + " !!!")
                            print("Change fee" + str(fee))
                            print('Profit is ' + str(profit_fee))
                        time.sleep(1)
                        if allow_stoploss_bts == "YES":
                           noti_bts="ON"
                           #allow_stoploss = "NO"
                           CK = Update_OrderBuy(order_id, exchange, 'sold')
                           if CK == "OK":
                              bot.sendMessage(chat_id, 'Update Status Sold out =>' + CK)
                           else:
                              bot.sendMessage(chat_id, 'Update Status Sold out =>' + CK)

                           allow_close_bts="NO"
                           NOTIBTS_INFO=""

                        if is_number(ST) == True and allow_stoploss_bts == "YES":
                            profit = (((LastPrice / rate) * qty) - qty)
                            fee = 0.0025
                            profit_fee = (profit - (profit * fee))

                            bot.sendMessage(chat_id,
                                            "!! Action StopLoss Completed\
                                            \nOrder:"+str(order_id)+"\
                                            \nCoin:"+coin+"\
                                            \nBuy:" + str(qty) + "\
                                            \nSold:" + str(format_floatc(((LastPrice / rate) * qty),2)) + "\
                                            \nChange Fee:" + str(fee) + "\
                                            \nProfit:" + str(format_floatc(profit_fee,2)) + " Bath",
                                            reply_markup=mainmenu)
                            print("Sale Stop loss at " + str(LastPrice) + " !!!")
                            print("Change fee" + str(fee))
                            print('Profit is ' + str(profit_fee))
                            allow_stoploss_bts="NO"
                            NOTIBTS_INFO=""
                            #CK = Update_OrderBuy(order_id, exchange, 'sold')
                            #if CK == "OK":
                            #    bot.sendMessage(chat_id, 'Update Status Sold out =>' + CK)
                            #else:
                            #    bot.sendMessage(chat_id, 'Update Status Sold out =>' + CK)


            else:
                print("Last Price is Null")
                continue

            ##################################################

    def sts(self, exchange, chat_id):
        global noti_bts
        global noti_sts
        global allow_cutloss_sts
        global allow_stoploss_sts
        global allow_update_sts
        global allow_update_point_sts
        global allow_close_sts
        global NOTISTS_INFO
        result=""
        if exchange == 'bxinth':
            fee = 0.0025
        ST = Get_OrderSale(exchange, 'sell')
        if ST == "()":
            return False
        for order in list(ST):
            Time = (order[1])
            order_id = (order[0])
            coin = (order[2])
            rate = (order[4])
            qty = (order[3])
            print("---------------------\n")
            print("Starting trader STS " + coin)
            print("" + Time + \
                  "\nOid:" + str(order_id) + \
                  "\nCoin:" + coin + \
                  "\nQty:" + str(qty) + \
                  "\nRate:" + str(rate))
            volumn = format_float(qty / rate)
            print("Volumn: " + volumn)
            print("### Start Trailling Stop STS " + coin + " ###")
            ## Lastprice for test ###
            if simtest == "yes":
                lastprice = get_lastprice_sim(str(coin), exchange)
            else:
                lastprice = get_lastprice(bxin, str(coin))
            if is_number(lastprice) == True and order_id != 0 and order_id != None:
                if simtest == "yes":
                    fee = 0.0025
                    volumn = format_float(float(volumn) - (float(volumn) * fee))
                    # print("Real Volume Sell Update" + str(float(volumn) - (float(volumn) * fee)))
                    if noti_sts == "ON" and allow_update_sts != "YES":
                        ST = "Noti"
                    elif noti_sts == "OFF" or allow_update_sts == "YES":
                        ST = sale_coin_sim(coin, float(volumn), float(lastprice), exchange)
                else:
                    fee = 0.0025
                    volumn = format_float(float(volumn) - (float(volumn) * fee))
                    # print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))
                    if noti_sts == "ON" and allow_update_sts != "YES":
                        ST = "Noti"
                    elif noti_sts == "OFF" or allow_update_sts == "YES":
                        ST = sale_coin(bxin, coin, float(volumn), float(lastprice), exchange)
                ## DEV##
                print("Sale update at " + str(lastprice) + " !!!")
                if allow_update_sts == "YES":
                    noti_sts = "ON"
                    # allow_cutloss = "NO"
                    CK = Update_OrderBuy(order_id, exchange, 'sold')
                    if CK == "OK":
                        bot.sendMessage(chat_id, 'Update Status Sold Out =>' + CK)
                    else:
                        bot.sendMessage(chat_id, 'Update Status Sold Out =>' + CK)
                elif allow_close_sts == "YES":
                    noti_sts = "ON"
                    # allow_cutloss = "NO"
                    CK = Update_OrderBuy(order_id, exchange, 'Close')
                    if CK == "OK":
                        bot.sendMessage(chat_id, "Close Order "+order_id+" =>" +CK)
                    else:
                        bot.sendMessage(chat_id, "Close Order "+order_id+" =>" + CK)

                        ## Real Sale ###
                if is_number(ST) == True and allow_update_sts == "YES":
                    profit = (((lastprice / rate) * qty) - qty)
                    profit_fee = (profit - (profit * fee))
                    bot.sendMessage(chat_id, "!!Action Sell Update Completed \
                         \nCoin:" + coin + "\
                         \nOrder:" + str(order_id) + "\
                         \nBuy:" + str(qty) + "\
                         \nSold:" + str(format_floatc(((lastprice / rate) * qty),2)) + "\
                         \nChange Fee " + str(fee) + "\
                         \nProfit " + str(format_floatc(profit_fee,2)) + "Bath", reply_markup=mainmenu)
                    # print("Sale Update to Lastprice at " + str(lastprice) + " !!!")
                    allow_update_sts = "NO"
                    NOTISTS_INFO = ""
                    continue


                if allow_update_sts != "YES":
                    result = sell_trailling_stop_shadow(order_id, exchange, lastprice, rate)
#                    print("Status trailling =>"+(result))
                if result != None:
                    if result[0] == "StopLossUpdate":
                        StopLoss_Point = result[1]
                        if "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTS_INFO += (
                            "\n--------------------- \
                              \n|= Update Point =|\
                              \nOrder:/" + order_id + "\
                              \nCoin:" + coin + "\
                              \nPrice:" + str(StopLoss_Point))
                        if simtest == "yes":
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                           # print("Real Volume Sell Update" + str(float(volumn) - (float(volumn) * fee)))
                            if noti_sts == "ON" and allow_update_sts != "YES":
                                ST = "Noti"
                            elif noti_sts == "OFF" or allow_update_sts == "YES":
                                ST = sale_coin_sim(coin, float(volumn), float(lastprice), exchange)
                        else:
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                            #print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))
                            if noti_sts == "ON" and allow_update_sts != "YES":
                                ST = "Noti"
                            elif noti_sts == "OFF" or allow_update_sts == "YES":
                                ST = sale_coin(bxin, coin, float(volumn), float(lastprice), exchange)
                        ## DEV##
                        if ST == "Noti" and allow_update_sts == "NO":
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('sts_update')
                            print("!!! Update Point STS to " + str(StopLoss_Point))
                            profit = (((StopLoss_Point / rate) * qty) - qty)
                            profit_last=(((lastprice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            profit_lastfee=(profit_last - (profit_last * fee))
                            NOTISTS_INFO+=("\nUpdate StopPoint STS "+coin+ \
                                        "\nOrder:/" + order_id + \
                                        "\nSale Volumn:" + str(volumn) + \
                                        "\nRate Start:" + str(rate) + \
                                        "\nQty:" + str(qty) + \
                                        "\nNow LastPrice:" + str(lastprice) + \
                                        "\nNow StopPoint(" + str(result[2]) + " %):" + str(StopLoss_Point) + \
                                        "\nChange Fee:" + str(fee) + \
                                        "\nProfit(StopLoss):"+str(format_floatc(profit_fee,2)) + " \
                                         \nProfit(LastPrice):"+str(format_floatc(profit_lastfee,2))+ " \
                                         ")
                            #time.sleep(1)
                        print("Action Close Status"+allow_close_sts)
                        if allow_update_sts == "YES":
                            noti_sts = "ON"
                            # allow_stoploss = "NO"
                            CK = Update_OrderSale(order_id, exchange, 'sold')
                            if CK == "OK":
                                bot.sendMessage(chat_id, 'Update Status Sold out =>' + CK)
                            else:
                                bot.sendMessage(chat_id, 'Update Status Sold out =>' + CK)
                        elif allow_update_point_sts == "YES":
                            bot.sendMessage(chat_id, "Update New Point to Order:/" + str(order_id) + "\n")


                        if is_number(ST) == True and allow_update_sts == "YES":
                            profit = (((lastprice / rate) * qty) - qty)
                            fee = 0.0025
                            profit_fee = (profit - (profit * fee))
                            bot.sendMessage(chat_id,
                                            "!! Action Sale STS Completed \
                                            \nCoin:" + coin + \
                                            "\nOrder:/" + order_id + \
                                            "\nSale Volumn:" + str(volumn) + \
                                            "\nRate Start:" + str(rate) + \
                                            "\nQty:" + str(qty) + \
                                            "\nSold:" + str(format_floatc(((lastprice / rate) * qty),2)) + \
                                            "\nChange Fee:" + str(fee) + \
                                            "\nProfit:" + str(format_floatc(profit_fee,2)) + " Bath",
                                            reply_markup=mainmenu)
                            print("Sale Update at " + str(lastprice) + " !!!")
                            print("Change fee:" + str(fee))
                            print('Profit:' + str(profit_fee))
                            allow_update_sts = "NO"
                            NOTISTS_INFO = ""

                    if result[0] == "CutLoss":
                        CutLossPrice = result[1]
                        time.sleep(2)
                        if "UpdateAct" not in UPDATE_ACT:
                            NOTISTS_INFO+=(
                                        "|= CutLoss =|\
                                         \nOrder:/" + order_id + "\
                                         \nCoin:" + coin + "\
                                         \nPrice:" + str(CutLossPrice))
                        if simtest == "yes":
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                            print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))

                            if noti_sts == "ON" and allow_cutloss_sts != "YES":
                                ST = "Noti"

                            elif noti_sts == "OFF" or allow_cutloss_sts == "YES":
                                ST = sale_coin_sim(coin, float(volumn), float(CutLossPrice), exchange)
                        else:
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                            print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))

                            if noti_sts == "ON" and allow_cutloss_sts != "YES":
                                ST = "Noti"

                            elif noti_sts == "OFF" or allow_cutloss_sts == "YES":
                                ST = sale_coin(bxin, coin, float(volumn), float(CutLossPrice), exchange)
                        if ST == "Noti" and allow_cutloss_sts == "NO" and "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('sts_cutloss')
                            profit = (((CutLossPrice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            NOTISTS_INFO+=("\n------------------------ \
                                            \n!! Please Take Action to Cut Loss STS ,Now!!\
                                            \n|--CutLoss "+coin+" --| \
                                            \nOrder:/" + order_id + \
                                            "\nSale Volumn:" + str(volumn) + \
                                            "\nRate Start:" + str(rate) + \
                                            "\nQty:" + str(qty) + \
                                            "\nSold:" + str(format_floatc(((CutLossPrice / rate) * qty),2)) + \
                                            "\nChange Fee:" + str(fee) + \
                                            "\nProfit:" + str(format_floatc(profit_fee,2)) + " Bath \
                                             \n Accept this Action or not?\n/OK\n/CLOSE\n/UPDATE")
                            print("Sale Cut loss at " + str(CutLossPrice) + " !!!")


                        if allow_cutloss_sts == "YES":
                            noti_sts = "ON"
                            #allow_cutloss = "NO"
                            CK = Update_OrderSale(order_id, exchange, 'sold')
                            if CK == "OK":
                                bot.sendMessage(chat_id, 'Update Action CutLoss Status =>' + CK)
                            else:
                                bot.sendMessage(chat_id, 'Update Action CutLoss Status =>' + CK)
                            allow_close_sts="NO"
                            NOTISTS_INFO=""


                        if is_number(ST) == True and allow_cutloss_sts == "YES":
                            profit = (((CutLossPrice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            bot.sendMessage(chat_id,
                                            "!! Action Cut Loss STS Completed \
                                             \nCoin:"+coin+\
                                            "\nOrder:/" +order_id + \
                                            "\nSale Volumn:" + str(volumn) + \
                                            "\nRate Start:" + str(rate) + \
                                            "\nQty:" + str(qty) + \
                                            "\nSold:" + str(format_floatc(((CutLossPrice / rate) * qty),2)) + \
                                            "\nChange Fee:" + str(fee) + \
                                            "\nProfit:" + str(format_floatc(profit_fee,2)) + " Bath",
                                            reply_markup=mainmenu)
                            print("Sale Cut loss at " + str(CutLossPrice) + " !!!")
                            allow_cutloss_sts="NO"
                            NOTIISTS_INFO=""
                           # CK = Update_OrderSale(order_id, exchange, 'sold')
                           #if CK == "OK":
                           #     bot.sendMessage(chat_id, 'Update Status =>' + CK)
                           # else:
                           #     bot.sendMessage(chat_id, 'Update Status =>' + CK)

                    elif result[0] == "StopLoss":
                        LastPrice = result[1]
                        time.sleep(2)
                        if "UpdateAct" not in UPDATE_ACT:
                            NOTISTS_INFO+=(
                                        "|= StopLoss =|\
                                         \nOrder:/" + order_id + "\
                                         \nCoin:" + coin + "\
                                         \nPrice:" + str(
                                            LastPrice))
                        if simtest == "yes":
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                            print("Real Volume Sell" + str(float(volumn) - (float(volumn) * fee)))
                            if noti_sts == "ON" and allow_stoploss_sts != "YES":
                                ST = "Noti"

                            elif noti_sts == "OFF" or allow_stoploss_sts == "YES":
                                ST = sale_coin_sim(coin, float(volumn), float(LastPrice), exchange)
                        else:
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                            print("Real Volume Sell" + str(float(volumn) - (float(volumn) * fee)))
                            print("Sale Coin Stop Loss !! at " + str(LastPrice) + " " + coin)
                            time.sleep(4)
                            if noti_sts == "ON" and allow_stoploss_sts != "YES":
                                ST = "Noti"
                                time.sleep(4)
                            elif noti_sts == "OFF" or allow_stoploss_sts == "YES":
                                # bot.sendMessage(chat_id,"")
                                ST = sale_coin(bxin, coin, float(volumn), float(LastPrice), exchange)
                            # ST=False
                            print("Status Sale Order " + str(ST))
                        if ST == "Noti" and allow_stoploss_sts == "NO" and "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('sts_stoploss')
                            profit = (((LastPrice / rate) * qty) - qty)
                            fee = 0.0025
                            profit_fee = (profit - (profit * fee))
                            NOTISTS_INFO+=("---------------------\
                                            \n!! Please Take Action StopLoss STS Noww !!\
                                            \n|--StopLoss "+coin+" --| \
                                            \nOrder:/" + order_id + \
                                            "\nSale Volumn:" + str(volumn) + \
                                            "\nRate Start:" + str(rate) + \
                                            "\nQty:" + str(qty) + \
                                            "\nSold:" + str(format_floatc(((LastPrice / rate) * qty),2)) + \
                                            "\nChange Fee:" + str(fee) + \
                                            "\nProfit:" + str(format_floatc(profit_fee,2)) + " Bath \
                                             \nAccept this Action or not ? \n/OK\n/CLOSE\n/UPDATE")

                            print("Sale Stop loss at " + str(LastPrice) + " !!!")
                            print("Change fee:" + str(fee))
                            print('Profit:' + str(profit_fee))
                            time.sleep(1)
                        if allow_stoploss_sts == "YES":
                           noti_sts = "ON"
                           #allow_stoploss = "NO"
                           CK = Update_OrderSale(order_id, exchange, 'sold')
                           if CK == "OK":
                              bot.sendMessage(chat_id, 'Update Status Sold out =>' + CK)
                           else:
                              bot.sendMessage(chat_id, 'Update Status Sold out =>' + CK)



                        if is_number(ST) == True and allow_stoploss_sts == "YES" :
                            profit = (((LastPrice / rate) * qty) - qty)
                            fee = 0.0025
                            profit_fee = (profit - (profit * fee))
                            bot.sendMessage(chat_id,
                                            "!! Action StopLoss STS Completed \
                                            \nCoin:"+coin+\
                                            "\nOrder:/" + order_id + \
                                            "\nSale Volumn:" + str(volumn) + \
                                            "\nRate Start:" + str(rate) + \
                                            "\nQty:" + str(qty) + \
                                            "\nSold:" + str(format_floatc(((LastPrice / rate) * qty),2)) + \
                                            "\nChange Fee:" + str(fee) + \
                                            "\nProfit:" + str(format_floatc(profit_fee,2)) + " Bath",
                                            reply_markup=mainmenu)
                            print("Sale Stop loss at " + str(LastPrice) + " !!!")
                            print("Change fee:" + str(fee))
                            print('Profit:' + str(profit_fee))
                            allow_stoploss_sts="NO"
                            NOTISTS_INFO=""
                            #CK = Update_OrderSale(order_id, exchange, 'sold')
                            #if CK == "OK":
                            #    bot.sendMessage(chat_id, 'Update Status Sold out =>' + CK)
                            #else:
                            #   bot.sendMessage(chat_id, 'Update Status Sold out =>' + CK)


            else:
                print("Last Price is Null")
                continue

    def sell_ratio(self, coin, Vlcoin, ratio, chat_id, exchange):
        if exchange == "bxinth":
            fee = 0.0025
        sell = (Vlcoin / ratio)
        ST = bxin.fetch_order_book(coin)
        count = 0
        profit = []
        for data in ST['bids']:
            lastprice = data[0]
            vl = data[1]

            print("Sell Lastprice:" + str(lastprice) + "\nvl:" + str(vl) + "\nSell:" + str(sell) + "\nProfit " + str(
                sell * lastprice))
            if simtest == "yes":
                time.sleep(4)
                ST = sale_coin_sim(coin, float(vl), float(lastprice), exchange)
            else:
                time.sleep(4)
                ST = sale_coin(bxin, coin, float(vl), float(lastprice), exchange)
            if is_number(ST) == True:
                count += 1
                profit = (sell * lastprice)
                profit_fee = (profit - (profit * fee))
                profit.append(profit_fee)
                bot.sendMessage(chat_id,
                                "!! Sell Ratio " + ratio + " num:" + count + " Completed\
                                \nOrder:/" + ST + \
                                "\nSale Volumn:" + str(vl) + \
                                "\nRate Start:" + str(lastprice) + \
                                "\nChange Fee:" + str(fee) + \
                                "\nProfit:" + str(format_float(profit_fee)) + " Bath")

            if count == ratio:
                break
            time.sleep(6)
            ProfitCount = 0
        for sum in profit:
            ProfitCount += sum
        bot.sendMessage(chat_id, "!! Profit Sum is:" + str(ProfitCount) + " Bath")

    def sell_increase(self, coin, Vlcoin, increase, chat_id, exchange):
        if exchange == "bxinth":
            fee = 0.0025
        # sell = (Vlcoin / ratio)
        ST = bxin.fetch_order_book(coin)
        count = 0
        profit = []
        for data in ST['bids']:
            lastprice = data[0] + (data[0] * increase / 100)
            vl = data[1]

            print(
                "Sell Lastprice:" + str(lastprice) + "\nvl:" + str(vl) + "\nSell:" + str(lastprice) + "\nProfit " + str(
                    Vlcoin * lastprice))
            if simtest == "yes":
                time.sleep(4)
                ST = sale_coin_sim(coin, float(vl), float(lastprice), exchange)
            else:
                time.sleep(4)
                ST = sale_coin(bxin, coin, float(vl), float(lastprice), exchange)
            if is_number(ST) == True:
                count += 1
                profit = (Vlcoin * lastprice)
                profit_fee = (profit - (profit * fee))
                profit.append(profit_fee)
                bot.sendMessage(chat_id,
                                "!! Sell Increase " + increase + " num:" + count + " Completed\
                                \nOrder:/" + ST + \
                                "\nSale Volumn:" + str(vl) + \
                                "\nRate Start:" + str(lastprice) + \
                                "\nChange Fee:" + str(fee) + \
                                "\nProfit:" + str(format_float(profit_fee)) + " Bath")

            if count == 10:
                break
            time.sleep(6)
            ProfitCount = 0
        for sum in profit:
            ProfitCount += sum
        bot.sendMessage(chat_id, "!! Profit Sum is:" + str(ProfitCount) + " Bath")


    def check_close_order(self, exchange, chat_id):
        ST = Get_OpenOrder(exchange, 'open')
        if ST == "()":
            return False
        print("|= Remaining Open Order  =|")
        for order in list(ST):
            Time = (order[2])
            order_id = (order[1])
            coin = (order[3])
            Type = (order[4])
            rate = (order[5])
            volumn = (order[6])
            qty = (order[7])
            print("" + Time + "\nO:/" + order_id + "\nC:" + coin + "\nR:" + str(rate) + "\nQ:" + str(
                qty) + "\nVolumn:" + str(volumn) + "\nType " + Type)
            print("---------------------")
            if Type == "buy":
                if simtest == "yes":
                    ST = ck_close_order_sim(order_id, coin, 'buy', exchange)
                else:
                    ST = ck_close_order(bxin, order_id, coin, 'buy', exchange)
            elif Type == "sell":
                if simtest == "yes":
                    ST = ck_close_order_sim(order_id, coin, 'sell', exchange)
                else:
                    ST = ck_close_order(bxin, order_id, coin, 'sell', exchange)

            if ST == True and Type == "buy": ## Dev
                #CKCLOSE.append('ckclose_buy_apply')
                print("DEBUG Insert Ckloss StopLoss " + str(BuyStopLoss) + " CutLoss " + str(BuyCutLoss))
               # bot.sendMessage(chat_id,"Apply BST Strategy or not?\n /Apply\n/No")
                ST = Insert_ckloss(order_id, 'bxinth', BuyStopLoss, BuyCutLoss, 0)
                if ST == "OK":
                    ST = Insert_OrderBuy(order_id, exchange, time.strftime('%Y-%m-%d %H:%M:%S'), coin, qty, rate, 'buy')
                    print("DEBUG Status Insert OrderBuy " + ST)
                    if ST == "OK":
                        bot.sendMessage(chat_id, "Order buy have been closed !!")
                        bot.sendMessage(chat_id,
                                        "Auto Apply BST \
                                        \nOrder ID:" + str(order_id) + "\
                                        \nCutLoss:" + str(BuyCutLoss) + " % \
                                        \nStopLoss:" + str(BuyStopLoss) + "% \
                                        \nApply --> Completed ", reply_markup=mainmenu)
                    else:
                        bot.sendMessage(chat_id,
                                        "!! Apply Strategy Trailing Stop to Order Buy " + order_id + "--> Failed !! ")

            if ST == True and Type == "sell":
                print("DEBUG Insert Ckloss StopLoss " + str(SellStopLoss) + " CutLoss " + str(SellCutLoss))
                ST = Insert_ckloss(order_id, exchange, SellStopLoss, SellCutLoss, 0)
                if ST == "OK":
                    ST = Insert_OrderSale(order_id, exchange, time.strftime('%Y-%m-%d %H:%M:%S'), coin, qty, rate,
                                          'sell')
                    print("DEBUG Status Insert OrderSell " + ST)
                    if ST == "OK":
                        bot.sendMessage(chat_id, "Order Sell have been closed !!")
                        bot.sendMessage(chat_id,
                                        "Auto Apply STS \
                                        \nOrder ID:" + str(order_id) + "\
                                             \nCutLoss:" + str(SellCutLoss) + " % \
                                             \nStopLoss:" + str(SellStopLoss) + "% \
                                             \nApply --> Completed ", reply_markup=mainmenu)
                    else:
                        bot.sendMessage(chat_id,
                                        "!! Apply Strategy Trailing Stop to Order Sell " + order_id + "--> Failed !! ")


TOKEN = telegrambot
bot = YourBot(TOKEN)
bot.message_loop()


#############MAIN PROGRAM ###########
while True:
      if STRATEGY_CHECK == "ON":
         simtest="yes"
         for adminid in adminchatid:
             bot.bts('bxinth',adminid)
             if NOTIBTS_INFO != "":
                bot.sendMessage(adminid, NOTIBTS_INFO, reply_markup=mainmenust)
                NOTIBTS_INFO = ""
             ####################
             bot.sts('bxinth',adminid)
             bot.check_close_order('bxinth',adminid)
             if NOTISTS_INFO != "":
                bot.sendMessage(adminid, NOTISTS_INFO, reply_markup=mainmenust)
                NOTISTS_INFO = ""
        ######## BTS Stratygy #########
      time.sleep(15)
#    print("Admin ChatID "+str(adminid))
#    ST = bot.bts('bxinth', adminid)
#    if ST == False:
#       continue
                # print(ST)
                # --------------------
#       time.sleep(2)
#       ST = bot.sts('bxinth', adminid)
               # print(ST)
#       if ST == False:
#          continue
          
#    time.sleep(2)        
        ########### END BTS ##############
    #    for adminid in adminchatid:
#    print("Admin ChatID "+str(adminid))
#    ST = bot.check_close_order('bxinth', adminid)
#    if ST == False:
#       continue
    #if Notification == "ON":
    #    for adminid in adminchatid:
            # print("Notification --> Open")
    #        Enable = "OK"
    #elif Notification == "OFF":
    #    print("Notification state close to all member..")



