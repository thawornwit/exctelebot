__author__ = 'thawornwit'
from tokens import *  ## for accessing telegram api
from botmain import *
import matplotlib  ## for ploting graph 
import ccxt
import emoji
import chart
import tradingview
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
CKSTOPBUY = []
CKCOMMAND = []
BXCOIN = ['BTC/THB', 'LTC/THB', 'DASH/THB', 'BCH/THB', 'OMG/THB', 'XRP/THB', 'REP/THB', 'GNO/THB', 'ETH/THB','POW/THB', 'XZC/THB']
COINTEMP = []
COINTEMP.append(0)
ORDERBUY = []
ORDERSELL = []
LASTPRICESIM = []
COINLISTINFO = []
STRATEGY = []
ACTION_UPDATE=[]
CKCLOSE = []
EX = []
NOTISTATE_ACTION = []
UPDATE_ACT = []
SELL_ORDER = []
BUY_ORDER=[]
CKBALANCE = []
CLOSECON=[]
STOPPOINT=[]
CKORDERWAIT=[]
menucoinmarkup = {'keyboard': [['BACK'], ['BTC', 'BCH','POW'], ['LTC', 'OMG', 'ETH'], ['EVX', 'DASH', 'XZC'], ['GNO', 'REP', 'XRP']]}
menuexchange = {'keyboard': [['BACK'], ['BXINTH', 'TDAX'], ['BITTREX', 'YOBIT']]}
menubuypercent = {'keyboard': [['BACK'], ['10%', '20%','25%'], ['40%', '45%','50%'],['60%', '75%','100%']]}
menusellpercent = {'keyboard': [['BACK'], ['10%', '20%','25%'], ['40%', '45%','50%'],['60%', '75%','100%']]}
mainmenu = {'keyboard': [['BUY', 'SELL', 'COIN'], ['BUY ORDER', 'SELL ORDER', 'CAN ORDER'], ['COIN RAITO', 'BALANCE','INFO'],
             ['NOTIFY','TASK ORDER', 'CANCEL'], ['ORDER WAIT','IDEAS','CHART'],['STRATEGY']]}
mainmenust = {'keyboard': [['BUY', 'SELL', 'INFO'], ['BUY ORDER', 'SELL ORDER', 'CAN ORDER'], ['CANCEL', 'STRATEGY'],
                           ['NEW','CLOSE', 'UPDATE']]}
selectst = {'keyboard': [['BUY', 'SELL', 'INFO'], ['BUY ORDER', 'SELL ORDER', 'CAN ORDER'], ['CANCEL', 'STRATEGY'],
                           ['BTS', 'BLS', 'CTS']]}
mainmenuby = {'keyboard': [['BUY', 'SELL', 'INFO'], ['BUY ORDER', 'CAN ORDER'], ['NOTIFY', 'STRATEGY'], ['CLOSE', 'UPDATE']]}
mainmenutk = {'keyboard': [['BUY', 'SELL', 'INFO'], ['BUY ORDER', 'SELL ORDER', 'CAN ORDER'], ['CANCEL', 'STRATEGY'],
                           ['CLOSE', 'UPDATE']]}
## Default Stop loss and Cut loss ##
BuyStopLoss = 5
BuyCutLoss = 3
SellStopLoss = 5
SellCutLoss = 3
#CoinRate=""
##############
BuyStopRisk = 3
BuyStopBuy = 3

Pause = "NO"
STRATEGY_CHECK = "ON"
NT=""
noti_sts = "ON"
noti_bts = "ON"
noti_bss = "ON"
# -----------------------#
allow_cutloss_bts = "NO"
allow_stoploss_bts = "NO"
allow_update_bts = "NO"
#------------------------#
allow_cutloss_sts = "NO"
allow_stoploss_sts = "NO"
allow_update_sts = "NO"
#------------------------#
allow_stopbuy_bss = "NO"
allow_stoprisk_bss = "NO"
allow_update_bss = "NO"
#-------Update Point-----#
allow_update_point_sts = "NO"
allow_update_point_bts = "NO"
allow_update_point_bss = "NO"
#-------Close Order -----#
allow_close_sts = "NO"
allow_close_bts = "NO"
allow_close_bss = "NO"

NOTIBTS_INFO = ""
NOTISTS_INFO = ""
NOTIBSS_INFO = ""
ACT = ""
ORDER = ""
simtest = ""
Coin = ""
CK1=""
CK2=""
CK3=""
BL=""
################### make up keybord stop ######
stopmarkup = {'keyboard': [['Stop Interactive']]}  ## for build Stop command to telagram
cancelmarkup = {'keyboard': [['YES','NO'], ['CANCEL', 'BACK'], [" "]]}  ## for build cancle command to telagram
backmarkup = {'keyboard': [['Back']]}  ## for build cancle command to telagram
hide_keyboard = {'hide_keyboard': True}
###############################################



class YourBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(YourBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None
        # self.sendMessage(self.chat_id,"Hello Guy ,Welcome to exctelecoinss \n Typing Command as below for start trading ..",reply_markup=mainmenu)

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

    def clear_strategy(self):
        STRATEGY.clear()
        CKLOSS.clear()
        CKSTOPBUY.clear()
        CLOSECON.clear()

    def clear_state(self):
        global CK1
        global CK2
        global CK3
        global ORDER
        global ACT
        global CONTINUE
        global Coin
        #-----------#
        BX.clear()
        CKCOMMAND.clear()
        COINTEMP.insert(0, "")
        CKCOMMAND.clear()
        COINLISTINFO.clear()
        ORDERBUY.clear()
        NOTISTATE_ACTION.clear()
        UPDATE_ACT.clear()
        SELL_ORDER.clear()
        BUY_ORDER.clear()
        STRATEGY.clear()
        NT == "Noti"
        Coin = ""
        CK1 = ""
        CK2 = ""
        CK3 = ""
        ORDER = ""
        ACT = ""

    def coin_buysalcan(self, chat_id, bxin, Coin):
        bot.sendChatAction(chat_id, 'typing')
        global CKBALANCE
        print("Debug Coin1" + Coin)
        if 'buyCoin' in BX:
            #bot.sendMessage(chat_id, str(get_coin_information(bxin, Coin,3)))
            sync_balance_coin(bxin,'bxinth','THB',str(chat_id))
            Bal = get_balance('bxinth','THB',str(chat_id))
            if Bal == False:
                print("\U0000274C (THB) Balance Not Available.!!")
                bot.sendMessage(chat_id, str("\U0000274C (THB) Balance Not Available.!!"),reply_markup=mainmenu)
                BX.clear()
            else:
                CKBALANCE = list(Bal)
                print("list -> Balance Buy" + str(CKBALANCE))
                bot.sendMessage(chat_id,str(Bal[2]))
                bot.sendMessage(chat_id, "How Many to Buy(THB) ?",reply_markup=menubuypercent)
                BX.append(Coin)
        elif 'saleCoin' in BX:
            sync_balance_coin(bxin,'bxinth',Coin,str(chat_id))
            Bal = get_balance('bxinth', Coin,str(chat_id))
            if Bal == False:
                print("["+Coin+"] Balance Not Available.!!")
                bot.sendMessage(chat_id, str("\U0000274C ["+Coin+"] Balance Not Available.!!"),reply_markup=mainmenu)
                BX.clear()
            else:
                CKBALANCE=list(Bal)
                print("list -> Balance"+str(CKBALANCE))
                bot.sendMessage(chat_id, str(Bal[2]))
                bot.sendMessage(chat_id, "How Many coin for Sell ?",reply_markup=menusellpercent)
                BX.append(Coin)
                print("Debug Coin2" + Coin)
        elif 'cancelCoin' in BX:
            OPST = Get_OpenOrder('bxinth', 'trading')
            if (str(OPST)) == "Failed" or (str(OPST)) == "()":
                bot.sendMessage(chat_id, "Not Found Your Order on Trading tables !!... ",reply_markup=mainmenu)
                time.sleep(4)
                CKCOMMAND.clear()
                BX.clear()
                COINTEMP.insert(0, "")
            elif (str(OPST)) == "OK" or (str(OPST)) != "()" and (str(OPST)) == "OK" or OPST != None:
                 CanInfo = "[ Order Result Trading ]\n"
                 print("Debug ST" + str(OPST))
                 for order in list(OPST):
                     uid = (order[0])
                     order_id = (order[1])
                     date = (order[2])
                     coin = (order[3])
                     type = (order[4])
                     rate = (order[5])
                     qty = (order[6])
                     total = (order[7])
                     if type == "buy":
                         type="Bids"
                     elif type == "sell":
                         type ="Asks"
                     CanInfo += ("["+type+"]\
                     \nOrderID:/"+ order_id + "\
                     \nCoin:" + coin + "\
                     \nRate:" + str(format_floatc(rate,4)) + "\
                     \nQty:" + str(format_floatc(qty,4)) + "\
                     \nTotal:" + str(format_floatc(total,4)) + "\
                     \n ------------- \n")
                 OPST = None
                 bot.sendMessage(chat_id, str(CanInfo))
                 bot.sendMessage(chat_id, "Enter OrderId:", reply_markup=cancelmarkup)
                 BX.append('Cancel')

    def coin_buysalcanselect(self, chat_id, bxin, msg, Coin):
        bot.sendChatAction(chat_id, 'typing')
        global CKBALANCE
        global Pause
        if msg == "BACK":
            Pause = "NO"
            self.clear_state()
            self.clear_strategy
            self.coinmenu(chat_id)
        elif msg == "CANCEL":
            return

        if 'buyCoin' in BX:
            Buy = msg
            print("Buy Befor >" + str(Buy))
            buy = self.trading_percent(chat_id,Buy,'THB')
            Buy = str(buy)
            if "%" in msg:
                bot.sendMessage(chat_id,"Buy "+str(msg)+" is "+str(Buy)+" Bath")
            print("Buy After >" + str(Buy))
            print(str(CKBALANCE))
            if is_number(float(CKBALANCE[1])) == True and is_number(Buy) == True and simtest != "yes":
                if float(CKBALANCE[1]) < float(Buy):
                    bot.sendMessage(chat_id, "!! Amount entered more than your " + str(CKBALANCE[1]) + " available !!\
                        Retype new balance ..\n")
                    bot.sendMessage(chat_id, "How Many to Buy(THB) ?",reply_markup=menubuypercent)
                    Buy = ">bl"
                elif float(Buy) < 10:
                    bot.sendMessage(chat_id, "!! There is minimum order of 10 THB,(" + str(CKBALANCE[1]) + ") is available !!\
                        Retype new balance ..\n")
                    bot.sendMessage(chat_id, "How Many to Buy(THB) ?",reply_markup=menubuypercent)
                    Buy = ">bl"

            if is_number(Buy) == True and float(Buy) > 0:
                print("DEBUG3" + Coin)
                if simtest == "yes":
                    bot.sendMessage(chat_id, "Now Sim Last Price:/" + str(get_lastprice_sim(str(Coin), 'bxinth')))
                else:
                    lastprice=get_lastprice(bxin, Coin)
                    if is_number(lastprice) == True:
                        bot.sendMessage(chat_id, "Now[Last]:/" + str(format_floatc((lastprice),2))+"\
                        \nNow[Asks]:/"+str(get_coin_lastorder(bxin,Coin,'sell')[0])+"\
                        \nNow[Bids]:/"+str(get_coin_lastorder(bxin,Coin,'buy')[0])+"")
                    else:
                        bot.sendMessage(chat_id,str(lastprice))

                if "bls" not in STRATEGY:
                    bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                else:
                    bot.sendMessage(chat_id,"[BLS]Start Coin Price Rate ? ",reply_markup=cancelmarkup)
                   # msg['text']=(format_floatc((get_lastprice(bxin, Coin)), 2))
                if Coin in BX:
                    BX.remove(Coin)
                if 'buyCoin' in BX:
                    BX.remove('buyCoin')
                BX.append('BUY')
                return Buy
            elif is_number(Buy) == True and float(Buy) <= 0 and str(Buy) != ">bl":
                bot.sendMessage(chat_id, "!! You must enter number amount more than zero only")
                bot.sendMessage(chat_id,"How Many to Buy(THB) ?",reply_markup=menubuypercent)
            elif is_number(Buy) == False and str(Buy) != ">bl":
                bot.sendMessage(chat_id, "!! You must enter number only,don't using text word !!")
                bot.sendMessage(chat_id, "How Many to Buy(THB) ?",reply_markup=menubuypercent)

        #### SALE COIN ###
        elif 'saleCoin' in BX:
            Sell = msg
            if "/" in str(Coin):
                C=str(Coin).split('/')
            print("Sell Befor >"+str(Sell))
            sell = self.trading_percent(chat_id,Sell,C[0])
            Sell= str(sell)
            print("Sell After >"+str(Sell))
            bot.sendMessage(chat_id, "Sell coin " + str(msg) + " is " + str(sell))
            ###########
            print(str(CKBALANCE))
            if is_number(float(CKBALANCE[1])) == True and is_number(Sell) == True and simtest != "yes":
                if float(CKBALANCE[1]) < float(Sell):
                    bot.sendMessage(chat_id,"!! Amount entered more than your "+str(CKBALANCE[1])+" available !!\
                    Retype new balance ..\n")
                    bot.sendMessage(chat_id, "How Many coin for sell ?",reply_markup=menusellpercent)
                    Sell=">bl"
            print("DEBUG4" + Coin)
            if is_number(Sell) == True and float(Sell) > 0:
                if simtest == "yes":
                    bot.sendMessage(chat_id, "Now Sim Last Price:/" + str(get_lastprice_sim(str(Coin), 'bxinth')))
                    bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                else:
                    lastprice=(get_lastprice(bxin, Coin))
                    if is_number(lastprice) == True:
                        bot.sendMessage(chat_id, "Now[Last]:/" +str(lastprice)+"\
                        \nNow [Bids]:/"+str(get_coin_lastorder(bxin,Coin,'buy')[0])+"\
                        \nNow[Asks]:/" + str(get_coin_lastorder(bxin, Coin, 'sell')[0]) + "")
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                    else:
                        bot.sendMessage(chat_id,str(lastprice))

                if Coin in BX:
                    BX.remove(Coin)
                if 'saleCoin' in BX:
                    BX.remove('saleCoin')
                BX.append('SELL')
                return Sell
            elif is_number(Sell) == True and float(Sell) <= 0 and str(Sell) != ">bl":
                bot.sendMessage(chat_id, "!! You must enter number amount more than zero only")
                bot.sendMessage(chat_id, "How Many coin for sell ?",reply_markup=menusellpercent)
            elif is_number(Sell) == False and str(Sell) != ">bl":
                bot.sendMessage(chat_id, "!! You must enter number only,don't using text word !!")
                bot.sendMessage(chat_id, "How Many coin for sell ?",reply_markup=menusellpercent)

    def coinbx(self, chat_id):
        global Pause
        Pause = "YES"
        bot.sendMessage(chat_id, "[ SELECT COIN ] \
            \n/BTC \
            \n/DASH \
            \n/LTC \
            \n/BCH \
            \n/GNO \
            \n/OMG \
            \n/REP \
            \n/XRP \
            \n/XZC \
            \n/EVX \
            \n/POW \
            \n/ETH ", reply_markup=menucoinmarkup)

    def coinmenu(self, chat_id):
        global Pause
        Pause = "NO"
        BX.clear()
        CKCOMMAND.clear()
        ORDERBUY.clear()
        CKBALANCE.clear()
        COINLISTINFO.clear()
        SELL_ORDER.clear()
        BUY_ORDER.clear()
        STRATEGY.clear()

        ##############
        bot.sendMessage(chat_id, "[ EXCTELECOINS MENU ]\
            \n\U0001F4B5 /buycoin  \
            \n\U0001F4B5 /salecoin \
            \n\U0001F4B5 /cancelcoin \
            \n\U0001F4B5 /ckcoininfo \
            \n\U0001F4B5 /balance \
            \n\U0001F4B5 /strategy  \
            \n\U0001F4B5 /chart  \
            \n\U0001F4B5 /ideas  \
            \n\U0001F4B5 /taskorder\
            \n\U0001F4B5 /notify \
            \n\U0001F4B5 /exchangecompare \
            \n\U0001F4B5 /cancel \
            \n|--- Sim Price ----| \
            \n\U0001F4B5 /setlastprice \
            \n\U0001F4B5 /setbalance \
            \n\U0001F4B5 /enablesimtest\
            ", reply_markup=mainmenu)

    def exchangemenu(self, chat_id, msg):
        bot.sendChatAction(chat_id, 'typing')
        global Pause
        ### Clear Status ###
        Pause="YES"
        BX.clear()
        CKCOMMAND.clear()
        ORDERBUY.clear()
        #####################
        CKCOMMAND.append(msg)
        bot.sendMessage(chat_id, "[ EXCHANGE ] \
            \n /BXINTH  \
            \n /TDAX  \
            \n /BITTREX \
            \n /YOBIT   ", reply_markup=menuexchange)


    def trading_percent(self,chat_id,percent,coin):
        if "%" in percent:
            res = get_balance('bxinth',coin, chat_id)
            price = percent
            data = str(price).split("%")
            if is_number(res[1]):
                data = format_floatc(((float(data[0]) / 100) * float(res[1])), 5)
                return str(data)
        else:
            return percent


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
        global StopBuy
        global StopRisk
        global BuyStopRisk
        global BuyStopBuy
        global Oid
        global simtest
        global allow_cutloss_bts
        global allow_stoploss_bts
        global allow_close_bss
        #--------------------#
        global allow_stopbuy_bss
        global allow_stoprisk_bss
        global allow_update_bss
        #--------------------#
        global allow_cutloss_sts
        global allow_stoploss_sts
        global allow_update_bts
        global allow_update_sts
        global allow_update_point_sts
        global allow_update_point_bts
        global allow_update_point_bss
        global allow_close_sts
        global allow_close_bts
        global noti_bts
        global noti_sts
        global noti_bss
        global Pause
        global STRATEGY_CHECK
        global NOTIBTS_INFO
        global NOTISTS_INFO
        global NOTIBSS_INFO
        global ORDER
        global ACT
        global CONTINUE
        BL=""

        content_type, chat_type, chat_id = telepot.glance(msg)
        content_type, chat_type, chat_id_test = telepot.glance(msg)
        print("Your chat_id_test:" + str(chat_id_test))
        # bot.sendMessage(chat_id,"Hello Guy ,Welcome to exctelecoinss \n Typing Command as below for start trading ..",reply_markup=mainmenu)
        # Do your stuff according to `content_type` ...
        print("Your chat_id:" + str(chat_id))  # this is chat_id
        print("Your admin_id:" + str(adminchatid))  # this is adminchatid
        print("Message Text:" + str(msg['text']))  ## message recived
        ### Connect to BX
        if chat_id in adminchatid:  # Store adminchatid variable in tokens.py
            ## Select Type Action
            TEXT = msg['text']
            CK1 = check_sys("echo " + TEXT + "|grep OK")
            CK2 = check_sys("echo " + TEXT + "|grep UPDATE")
            CK3 = check_sys("echo " + TEXT + "|grep CLOSE")
            #print("Status check =>"+CK3)
            if str(CK1) != "" or str(CK2) != "" or str(CK3) != "":
                ACT = check_sys("echo " + TEXT + "|awk -F_ '{print $1}'")
                ORDER = check_sys("echo " + TEXT + "|awk -F_ '{print $2}'")
                print("Select Action =>" + ACT + " Order=>" + ORDER)

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

            if msg['text'] == '/enablesimtest':
                bot.sendMessage(chat_id, "[/YES]||\n[/NO]")
                CKCOMMAND.append('enableSimtest')
            elif 'enableSimtest' in CKCOMMAND and msg['text'] == '/YES':
                simtest = "yes"
                bot.sendMessage(chat_id, "Enable Sim test mode -> Completed ")
            elif 'enableSimtest' in CKCOMMAND and msg['text'] == '/NO':
                simtest = "no"
                bot.sendMessage(chat_id, "Disable Sim test mode -> Completed ")

            if msg['text'] == '/setlastprice':
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
                if "/" in str(Coin):
                    Coin=str(Coin).split("/")[1]
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
                Pause = "NO"
                self.clear_state()
                self.clear_strategy()
                bot.sendMessage(chat_id, "\U00002714 Cancel all action-> OK ")

                self.coinmenu(chat_id)
            if msg['text'] == "COIN" or msg['text'] == "/coin":
                COUNT=0
                bot.sendChatAction(chat_id, 'typing')
                bot.sendMessage(chat_id,""+emoji.emojize(':hourglass:')+"Coin Under Processing ..")
                INFO=""
                INFO="[[- COIN LASTPRICE -]]\n"
                CK = get_lastcoin(bxin, 'bxinth')
                for c in CK:
                    COUNT+=1
                    INFO+=(str(COUNT)+")"+str(c[0]) + "|" + str(c[1]) + "|["+str(c[2])+"]\n")
                bot.sendMessage(chat_id,INFO)

            if msg['text'] == "COIN RAITO" or msg['text'] == "/coinraito":
                bot.sendChatAction(chat_id, 'typing')
                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+"Raito Under Processing ..")
                INFO = ""
                INFO = "[- (%)COIN TRADING -]\n"
                CK = (good_coin_ck(bxin, 'bxinth', 'THB'))
                COUNT = 0
                for buy_coin in CK:
                    COUNT += 1
                    INFO += (str(COUNT) + ")" + buy_coin[0] + " [" + str(buy_coin[1]) + "]["+str(buy_coin[2])+"]\n")
                bot.sendMessage(chat_id, INFO + "\n")

            if msg['text'] == "CHART" or msg['text'] == "/chart":
                bot.sendChatAction(chat_id, 'typing')
                bot.sendMessage(chat_id,"This command will get a 24 hour graph of selected currency from poloniex\n")
                self.coinbx(chat_id)
                BX.append("chart")
            elif "chart" in BX and msg['text'] != "":
                coin=msg['text']
                #print("Coin =>"+coin)
                try:
                    chart.make_graph(coin,10,30)
                    bot.sendPhoto(chat_id=chat_id, photo=open('./example.png', 'rb'),reply_markup=mainmenu)
                    BX.clear()
                except Exception as e:
                    bot.sendMessage(chat_id,"Error parsing data. Invalid ticker or API timeout\n"+str(e))

            if msg['text'] == "IDEAS" or msg['text'] == "/ideas":
                bot.sendChatAction(chat_id, 'typing')
                bot.sendMessage(chat_id,"Ideas is parse ideas from 20 page of \"tradingview.com\" in the last hours\n")
                bot.sendMessage(chat_id,"Enter number of last hours")
                BX.append('ideas')
            elif 'ideas' in BX:
                H=msg['text']
                if is_number(H) != True:
                    bot.sendMessage(chat_id, "!! Enter number only,,\
                        \nEnter number of last hours")
                    msg['text']=""
                elif int(H) < 1 and is_number(H) == True:
                    bot.sendMessage(chat_id,"Please input positive number of hours")
                elif int(H) > 1 and is_number(H) == True:
                    try:
                        bot.sendMessage(chat_id,"Analytical 20 pages of tradingview.com in the last {} hours...".format(str(H)))
                        bot.sendMessage(chat_id, "" + emoji.emojize(':hourglass:') + "Under Analytic Processing ..")
                        text = tradingview.sort_and_order(tradingview.parse(20,int(H)))
                        bot.sendMessage(chat_id,text)
                        BX.clear()
                    except Exception as e:
                        bot.sendMessage("Error parsing tradingview\n" + str(e))



            #### SHOW TASK ###
            if msg['text'] == "TASK ORDER" or msg['text'] == "/taskorder":
                Pause = "YES"
                #bot.sendMessage(chat_id, "[ STRATEGY TASK ]")
                self.taskorder('bxinth', chat_id)
            if msg['text'] == "ORDER WAIT" or msg['text'] == "/orderwait":
                #bot.sendMessage(chat_id, "|= WAIT T =|")
                Pause="YES"
                ST=self.check_trading_wait('bxinth',chat_id)
            if msg['text'] == "/balance" or msg['text'] == "BALANCE":
                Pause = "YES"
                sync_balance_all(bxin, 'bxinth', str(chat_id))
                self.coinbx(chat_id)
                CKBALANCE.clear()
                COUNT = 0
                CKBALANCE.append('BALANCE')
            elif 'BALANCE' in CKBALANCE:
                bot.sendChatAction(chat_id, 'typing')
                INFO = ""
                coin = msg['text']
                ST = get_balance('bxinth',"THB",str(chat_id))  ## MArket main
                if ST == False:
                    bot.sendMessage(chat_id,"\U0000274C [THB] Balance Not Available !!")
                else:
                    INFO +=(ST[2])
                    #bot.sendMessage(chat_id," Balance Available\n" + ST)
                #--------------#
                ST = get_balance('bxinth', coin,str(chat_id))
                if ST == False:
                    bot.sendMessage(chat_id,"\U0000274C ["+coin+"] Balance Not Available !!")
                else:
                    INFO +=ST[2]
                    bot.sendMessage(chat_id,INFO)
                COUNT += 1
                #print(INFO)
            ########### Allow Take Action BTS####
            if ACT == "/OK" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION:
                allow_cutloss_bts = "YES"
                allow_stoploss_bts = "NO"
                #-------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                #--------------------#
                allow_cutloss_sts = "NO"
                allow_stoploss_sts = "NO"
                #--------------------#
                allow_update_bts = "NO"
                allow_update_sts = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("Allow CutLoss =>" + allow_cutloss_bts)
            elif ACT == "/OK" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION:
                allow_stoploss_bts = "YES"
                allow_cutloss_bts = "NO"
                #---------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                #---------------------#
                allow_cutloss_sts = "NO"
                allow_stoploss_sts = "NO"
                #--------------------#
                allow_update_bts = "NO"
                allow_update_sts = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("Allow StopLoss =>" + allow_stoploss_bts)
            elif ACT == "/OK" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION:
                allow_update_bts = "YES"
                allow_stoploss_bts = "NO"
                allow_cutloss_bts = "NO"
                #---------------------#
                allow_cutloss_sts = "NO"
                allow_stoploss_sts = "NO"
                allow_update_sts = "NO"
                #----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("allow Update bts sell =>" + allow_update_bts)
                ########### Allow Take Action BSS####
            elif ACT == "/OK" and noti_bss == "ON" and 'bls_stopbuy' in NOTISTATE_ACTION:
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                # -------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "YES"
                #--------------------#
                allow_cutloss_sts = "NO"
                allow_stoploss_sts = "NO"
                #--------------------#
                allow_update_bts = "NO"
                allow_update_sts = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("Allow StopBuy =>" + allow_stopbuy_bss)
            elif ACT == "/OK" and noti_bss == "ON" and 'bls_stoprisk' in NOTISTATE_ACTION:
                allow_stoploss_bts = "NO"
                allow_cutloss_bts = "NO"
                # ---------------------#
                allow_stoprisk_bss = "YES"
                allow_stopbuy_bss = "NO"
                #---------------------#
                allow_cutloss_sts = "NO"
                allow_stoploss_sts = "NO"
                #--------------------#
                allow_update_bts = "NO"
                allow_update_sts = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("Allow Stoprisk =>" + allow_stoprisk_bss)
            elif ACT == "/OK" and noti_bss == "ON" and 'bls_update' in NOTISTATE_ACTION:
                allow_update_bts = "NO"
                allow_stoploss_bts = "NO"
                allow_cutloss_bts = "NO"
                # ---------------------#
                allow_cutloss_sts = "NO"
                allow_stoploss_sts = "NO"
                allow_update_sts = "NO"
                #----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "YES"
                ACT = ""
                print("allow Update bss buy =>" + allow_update_bss)
            ##################
            elif ACT == "/OK" and noti_sts == "ON" and 'cts_cutloss' in NOTISTATE_ACTION:
                allow_cutloss_sts = "YES"
                allow_stoploss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("allow Cutloss =>" + allow_cutloss_sts)
            elif ACT == "/OK" and noti_sts == "ON" and 'cts_stoploss' in NOTISTATE_ACTION:
                allow_stoploss_sts = "YES"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("allow Stoploss =>" + allow_stoploss_sts)
            elif ACT == "/OK" and noti_sts == "ON" and 'cts_update' in NOTISTATE_ACTION:
                allow_update_sts = "YES"
                allow_update_bts = "NO"
                allow_stoploss_sts = "NO"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("allow Update sts sell =>" + allow_update_sts)

            ########
            #### Allow Take Action Update Point ###
            ##### BSS Update ########
            if ACT == "UPDATE" and noti_bss == "ON" and 'bls_stopbuy' in NOTISTATE_ACTION and ACT == "UPDATE" \
                    or ACT == "/UPDATE" and noti_bss == "ON" and 'bls_stopbuy' in NOTISTATE_ACTION and ACT == "/UPDATE":
                UPDATE_ACT.append("UpdateAct")
                Pause = "YES"
                bot.sendMessage(chat_id, "Enter new StopBuy Point:")
                NOTISTATE_ACTION.append('StopBuy_Update')
                allow_close_sts = "NO"
                allow_close_bts = "NO"
                # ------------------#
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                allow_stoploss_sts = "NO"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = "NO"
                print("Allow StopBuy Point =>" + allow_update_point_bss)
            elif ACT == "UPDATE" and noti_bss == "ON" and 'bls_stoprisk' in NOTISTATE_ACTION and ACT == "UPDATE" \
                    or ACT == "/UPDATE" and noti_bss == "ON" and 'bls_stoprisk' in NOTISTATE_ACTION and ACT == "/UPDATE":
                bot.sendMessage(chat_id, "Enter new StopBuy Point:")
                NOTISTATE_ACTION.append('StopBuy_Update')
                UPDATE_ACT.append("UpdateAct")
                Pause = "YES"
                allow_close_sts = "NO"
                allow_close_bts = "NO"
                # ------------------#
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                allow_stoploss_sts = "NO"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("Allow Update StopRisk  =>" + allow_update_point_bss + "")
            elif ACT == "UPDATE" and noti_bss == "ON" and 'bls_update' in NOTISTATE_ACTION and ACT == "UPDATE" \
                    or ACT == "/UPDATE" and noti_bss == "ON" and 'bls_update' in NOTISTATE_ACTION and ACT == "/UPDATE":
                bot.sendMessage(chat_id, "Enter new StopBuy Point:")
                NOTISTATE_ACTION.append('StopBuy_Update')
                UPDATE_ACT.append("UpdateAct")
                Pause = "YES"
                allow_close_sts = "NO"
                allow_close_bts = "NO"
                # ------------------#
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                allow_stoploss_sts = "NO"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
            elif 'StopBuy_Update' in NOTISTATE_ACTION:
                StopBuy = msg['text']
                if is_number(StopBuy) == True:
                    bot.sendMessage(chat_id, "Enter new StopRisk Point(%):")
                    NOTISTATE_ACTION.pop()
                    NOTISTATE_ACTION.append('StopRiskPoint_Update')
                else:
                    bot.sendMessage(chat_id, "Enter number only !!\nEnter new StopBuy Point:")
            elif "StopRiskPoint_Update" in NOTISTATE_ACTION:
                StopRisk = msg['text']
                print("Check StopRisk=>" + ORDER)
                if is_number(StopRisk) == True and ORDER == "":
                    NOTISTATE_ACTION.pop()
                    NOTISTATE_ACTION.append("ApplyUpdate_BSS")
                    bot.sendMessage(chat_id, "Apply to Order:")
                elif str(ORDER) != "":
                    NOTISTATE_ACTION.pop()
                    NOTISTATE_ACTION.append("ApplyUpdate_BSS")
                    bot.sendMessage(chat_id, "Apply to Order ["+ORDER +"] or not?\
                    \n[/YES]||[/NO]")
                else:
                    bot.sendMessage(chat_id, "Enter number only \n Enter New StopRisk Point:")
            elif "ApplyUpdate_BSS" in NOTISTATE_ACTION and msg['text'] == "/YES":
                print("Check Apply StopRisk=>" + ORDER)
                if str(ORDER) == "":
                    order_id = msg['text']
                    if "/" in str(order_id):
                        order_id=str(order_id).split("/")[1]
                else:
                    order_id = ORDER
                if is_number(order_id) == True and ORDER == "":
                    CK = Update_StopRisk(order_id, 'bxinth', StopRisk)
                    if CK == "OK":
                        CK = Update_StopBuy(order_id, 'bxinth', StopBuy)
                        if CK == "OK":
                            bot.sendMessage(chat_id, "New StopBuy Point:" + StopBuy + " %\
                        \nNew StopRisk Point:" + StopRisk + " % \
                        \n Update Order " + str(order_id) + " => Completed")
                    NOTISTATE_ACTION.clear()
                    UPDATE_ACT.clear()
                    time.sleep(1)
                elif str(ORDER) != "":
                    print("Update It !!!!! =>" + ORDER)
                    CK = Update_StopRisk(order_id, 'bxinth', StopRisk)
                    if CK == "OK":
                        CK = Update_StopBuy(order_id, 'bxinth', StopBuy)
                        if CK == "OK":
                            bot.sendMessage(chat_id, "New StopBuy Point:" + StopBuy + " %\
				\nNew StopRisk Point:" + StopRisk + " % \
                            \n Update Order " + str(order_id) + " => Completed")
                    else:
                        bot.sendMessage(chat_id, "Update New Point => Failed")
                    print("Update =>" + CK)
                    NOTISTATE_ACTION.clear()
                    UPDATE_ACT.clear()
                    time.sleep(1)
                    ORDER = ""
                else:
                    NOTISTATE_ACTION.clear()
                    UPDATE_ACT.clear()
                    ACT = ""
                    ORDER = ""
                    #####################

                    ##### BTS Update #######
            if ACT == "UPDATE" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION \
                    or ACT == "/UPDATE" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION:
                UPDATE_ACT.append("UpdateAct")
                bot.sendMessage(chat_id, "Enter new Stop Point:")
                NOTISTATE_ACTION.append('StopPoint_Update')
                Pause = "YES"
                allow_close_sts = "NO"
                allow_close_bts = "NO"
                # ------------------#
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                allow_stoploss_sts = "NO"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("Allow CutLoss Point Sell =>" + allow_update_point_bts)
            elif ACT == "UPDATE" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION \
                    or ACT == "/UPDATE" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION:
                bot.sendMessage(chat_id, "Enter new Stop Point:")
                NOTISTATE_ACTION.append('StopPoint_Update')
                UPDATE_ACT.append("UpdateAct")
                Pause = "YES"
                allow_close_sts = "NO"
                allow_close_bts = "NO"
                # ------------------#
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                allow_stoploss_sts = "NO"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("Allow Update StopLoss Point =>" + allow_update_point_bts)
            elif ACT == "UPDATE" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION \
                    or ACT == "/UPDATE" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION:
                UPDATE_ACT.append("UpdateAct")
                Pause = "YES"
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
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("allow Update bts Point sell =>" + allow_update_point_bts)
            ################## STS Update ####
            elif ACT == "UPDATE" and noti_sts == "ON" and 'cts_cutloss' in NOTISTATE_ACTION \
                    or ACT == "/UPDATE" and noti_sts == "ON" and 'cts_cutloss' in NOTISTATE_ACTION:
                bot.sendMessage(chat_id, "Enter new Stop Point:")
                NOTISTATE_ACTION.append('StopPoint_Update')
                Pause = "YES"
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
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("allow Cutloss Update Point =>" + allow_update_point_sts)
            elif ACT == "UPDATE" and noti_sts == "ON" and 'cts_stoploss' in NOTISTATE_ACTION \
                    or ACT == "/UPDATE" and noti_sts == "ON" and 'cts_stoploss' in NOTISTATE_ACTION:
                bot.sendMessage(chat_id, "Enter new Stop Point:")
                NOTISTATE_ACTION.append('StopPoint_Update')
                Pause = "YES"
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
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
                print("allow StopLoss Update Poine =>" + allow_update_point_sts)
            elif ACT == "UPDATE" and noti_sts == "ON" and 'cts_update' in NOTISTATE_ACTION \
                    or ACT == "/UPDATE" and noti_sts == "ON" and 'cts_update' in NOTISTATE_ACTION:
                UPDATE_ACT.append("UpdateAct")
                Pause = "YES"
                bot.sendMessage(chat_id, "Enter new Stop Point:")
                NOTISTATE_ACTION.append('StopPoint_Update')
                allow_close_sts = "NO"
                allow_close_bts = "NO"
                #------------------#
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                allow_stoploss_sts = "NO"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                # ----------------------#
                allow_stoprisk_bss = "NO"
                allow_stopbuy_bss = "NO"
                allow_update_bss = "NO"
                ACT = ""
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
                if is_number(CutLoss) == True and ORDER == "":
                    bot.sendMessage(chat_id, "Apply to Order:")
                    NOTISTATE_ACTION.pop()
                    NOTISTATE_ACTION.append("ApplyUpdate")
                elif is_number(CutLoss) == True and ORDER != "":
                    NOTISTATE_ACTION.pop()
                    bot.sendMessage(chat_id, "Apply to Order [" +ORDER+ "] or not?\
                    \n[/YES]||[/NO]")
                    NOTISTATE_ACTION.append("ApplyUpdate")
                else:
                    bot.sendMessage(chat_id, "Enter number only \n Enter New CutLoss Point:")
            elif "ApplyUpdate" in NOTISTATE_ACTION and msg['text'] == "/YES":
                if ORDER == "":
                    order_id = msg['text']
                    if "/" in str(order_id):
                        order_id=str(order_id).split("/")[1]
                else:
                    order_id = ORDER
                if is_number(order_id) == True and ORDER == "":
                    CK = Update_StopLoss(order_id, 'bxinth', StopLoss)
                    if CK == "OK":
                        CK = Update_CutLoss(order_id, 'bxinth', CutLoss)
                        if CK == "OK":
                            bot.sendMessage(chat_id, "New StopLoss Point:" + StopLoss + " %\
                        \nNew CutLoss Point:" + CutLoss + " % \
                        \n Update to Order " + str(order_id) + " => Completed")
                    NOTISTATE_ACTION.clear()
                    UPDATE_ACT.clear()
                    time.sleep(1)
                elif ORDER != "":
                    CK = Update_StopLoss(order_id, 'bxinth', StopLoss)
                    if CK == "OK":
                        CK = Update_CutLoss(order_id, 'bxinth', CutLoss)
                        if CK == "OK":
                            bot.sendMessage(chat_id, "\n[RESULT UPDATE]\nNew StopLoss Point:" + StopLoss + " %\
                            \nNew CutLoss Point:" + CutLoss + " % \
                            \nUpdate to Order " + str(order_id) + " => Completed")
                    NOTISTATE_ACTION.clear()
                    UPDATE_ACT.clear()
                    ACT = ""
                    ORDER = ""
                    time.sleep(1)
                else:
                    NOTISTATE_ACTION.clear()
                    UPDATE_ACT.clear()
                    ACT = ""
                    ORDER = ""
                    ########
                    #### Allow Take Action Close Order ###
                    #########


                #### Allow Take Action BSS Close Order ###
                #########
            print("BSS CLOSE "+ORDER)
            if ACT == "CLOSE" and noti_bss == "ON" and 'bls_stopbuy' in NOTISTATE_ACTION \
                or ACT == "/CLOSE" and noti_bss == "ON" and 'bls_stopbuy' in NOTISTATE_ACTION:
                #bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                Pause = "YES"
                NOTISTATE_ACTION.pop()
                bot.sendMessage(chat_id, "Do you want to Close Order " + str(ORDER) + " or not ?,\n[/YES]||[/NO]")
                NOTISTATE_ACTION.append("CloseOrder")
                allow_close_sts = "NO"
                allow_close_bts = "NO"
                allow_close_bss = "YES"
                # ------------------#
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                allow_stoploss_sts = "NO"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                print("Allow to CLose Order =>" + allow_close_bss)
                ACT=""
            elif ACT == "CLOSE" and noti_bss == "ON" and 'bls_stoprisk' in NOTISTATE_ACTION \
                or ACT == "/CLOSE" and noti_bss == "ON" and 'bls_stoprisk' in NOTISTATE_ACTION:
                #bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                NOTISTATE_ACTION.pop()
                bot.sendMessage(chat_id, "Do you want to Close Order " + str(ORDER) + " or not ?\n[/YES]||[/NO]")
                NOTISTATE_ACTION.append("CloseOrder")
                allow_close_sts = "NO"
                allow_close_bts = "NO"
                allow_close_bss = "YES"
                # ------------------#
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                allow_stoploss_sts = "NO"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                print("Allow to CLose Order =>" + allow_close_bss)
                ACT=""
            elif ACT == "CLOSE" and noti_bss == "ON" and 'bls_update' in NOTISTATE_ACTION \
                or ACT == "/CLOSE" and noti_bss == "ON" and 'bls_update' in NOTISTATE_ACTION:
                #bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                NOTISTATE_ACTION.pop()
                bot.sendMessage(chat_id, "Do you want to Close Order " + str(ORDER) + " or not ?\n[/YES]||[/NO]")
                NOTISTATE_ACTION.append("CloseOrder")
                allow_close_sts = "NO"
                allow_close_bts = "NO"
                allow_close_bss = "YES"
                # ------------------#
                allow_update_sts = "NO"
                allow_update_bts = "NO"
                allow_stoploss_sts = "NO"
                allow_cutloss_sts = "NO"
                allow_cutloss_bts = "NO"
                allow_stoploss_bts = "NO"
                ACT=""
                print("Allow to CLose Order =>" + allow_close_bss)
            elif ACT == "CLOSE" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION \
                    or ACT == "/CLOSE" and noti_bts == "ON" and 'bts_cutloss' in NOTISTATE_ACTION:
                #bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                NOTISTATE_ACTION.pop()
                bot.sendMessage(chat_id, "Do you want to Close Order " + str(ORDER) + " or not ?\n[/YES]||[/NO}")
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
            elif ACT == "CLOSE" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION \
                    or ACT == "/CLOSE" and noti_bts == "ON" and 'bts_stoploss' in NOTISTATE_ACTION:
                #bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                NOTISTATE_ACTION.pop()
                bot.sendMessage(chat_id, "Do you want to Close Order " + str(ORDER) + " or not ?{/YES]||[/NO]")
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
            elif ACT == "CLOSE" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION \
                    or ACT == "/CLOSE" and noti_bts == "ON" and 'bts_update' in NOTISTATE_ACTION:
                #bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                NOTISTATE_ACTION.pop()
                bot.sendMessage(chat_id, "Do you want to Close Order " + str(ORDER) + " or not ?[/YES]||[/NO]")
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
            ################## STS Update ####
            elif ACT == "CLOSE" and noti_sts == "ON" and 'cts_cutloss' in NOTISTATE_ACTION \
                    or ACT == "/CLOSE" and noti_sts == "ON" and 'cts_cutloss' in NOTISTATE_ACTION:
                #bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                NOTISTATE_ACTION.pop()
                bot.sendMessage(chat_id, "Do you want to Close Order " + str(ORDER) + " or not ?,\n[/YES]||[/NO]")
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
            elif ACT == "CLOSE" and noti_sts == "ON" and 'cts_stoploss' in NOTISTATE_ACTION \
                    or ACT == "/CLOSE" and noti_sts == "ON" and 'cts_stoploss' in NOTISTATE_ACTION:
                #bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                NOTISTATE_ACTION.pop()
                bot.sendMessage(chat_id, "Do you want to Close Order " + str(ORDER) + " or not ?\n[/YES]||[/NO]")
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
            elif ACT == "CLOSE" and noti_sts == "ON" and 'cts_update' in NOTISTATE_ACTION \
                    or ACT == "/CLOSE" and noti_sts == "ON" and 'cts_update' in NOTISTATE_ACTION:
                #bot.sendMessage(chat_id, "Enter OrderID:", reply_markup=mainmenu)
                NOTISTATE_ACTION.pop()
                bot.sendMessage(chat_id, "Do you want to Close Order " + str(ORDER) + " or not ?\n[/YES]||[/NO]")
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
            elif "CloseOrder" in NOTISTATE_ACTION and msg['text'] == "/YES":
                noti_bss = "ON"
                print("Apply Close Stage !!")
                if str(ORDER) == "":
                    NOTISTATE_ACTION.pop()
                    bot.sendMessage(chat_id, "Enter OrderID:")
                    NOTISTATE_ACTION.append("ApplyClose")
                elif str(ORDER) != "":
                    order_id = ORDER
                    if is_number(ORDER) == True:
                        if allow_close_bss == "YES":
                           CK = Update_OrderStopBuy(order_id, 'bxinth', 'Close')
                        elif allow_close_bts == "YES":
                           CK = Update_OrderBuy(order_id, 'bxinth', 'Close')
                        elif allow_close_sts == "YES":
                           CK = Update_OrderSale(order_id, 'bxinth', 'Close')
                        if CK == "OK":
                            bot.sendMessage(chat_id, "Close Order " + order_id + " =>" + CK)
                            allow_close_bss = "NO"
                            allow_close_bts = "NO"
                            allow_close_sts = "NO"
                            NOTISTATE_ACTION.clear()
                        else:
                            bot.sendMessage(chat_id, "Close Order " + order_id + " =>" + CK)
                    else:
                        bot.sendMessage(chat_id, "Not found Order ID!!, \
                                    \nEnter OrderID:", reply_markup=mainmenu)
                    #NOTISTATE_ACTION.append("ApplyClose")
            elif "ApplyClose" in NOTISTATE_ACTION and msg['text'] != "":
                print("Apply CLose Order !!!")
                if str(ORDER) == "":
                    order_id = msg['text']
                    if "/" in str(order_id):
                        order_id=str(order_id).split("/")[1]
                    if is_number(order_id) == True:
                        if allow_close_bss == "YES":
                            CK = Update_OrderStopBuy(order_id, 'bxinth', 'Close')
                        elif allow_close_bts == "YES":
                            CK = Update_OrderBuy(order_id, 'bxinth', 'Close')
                        elif allow_close_sts == "YES":
                            CK = Update_OrderSale(order_id, 'bxinth', 'Close')
                        if CK == "OK":
                            bot.sendMessage(chat_id, "Close Order " + order_id + " =>" + CK)
                            allow_close_bss = "NO"
                            allow_close_bts = "NO"
                            allow_close_sts = "NO"
                            NOTISTATE_ACTION.clear()
                        else:
                            bot.sendMessage(chat_id, "Close Order " + order_id + " =>" + CK)
                    else:
                        bot.sendMessage(chat_id, "Enter Number only !!, \
                                \nEnter OrderID:", reply_markup=mainmenu)



            ### SELL ORDER ####
            if msg['text'] == 'SELL ORDER' or msg['text'] == 'BUY ORDER':
                Pause = "YES"
                if msg['text'] == 'SELL ORDER':
                    bot.sendMessage(chat_id, 'Using for Sell Coin Directly,For Support BTS,CTS order !!!',
                                reply_markup=cancelmarkup)
                    bot.sendMessage(chat_id, 'Enter Your Order:', reply_markup=cancelmarkup)
                    SELL_ORDER.append('SELL')  ## DEV
                if msg['text'] == 'BUY ORDER':
                    bot.sendMessage(chat_id, 'Using for Sell Coin Directly,For Support BLS order !!!',
                                    reply_markup=cancelmarkup)
                    bot.sendMessage(chat_id, 'Enter Your Order:', reply_markup=cancelmarkup)
                    BUY_ORDER.append('BUY')  ## DEV

            elif 'SELL' in SELL_ORDER:
                Order = msg['text']
                if "/" in str(Order):
                    Order=str(Order).split("/")[1]
                if is_number(Order) == True:
                    self.sellorder('bxinth', Order, chat_id)
                    SELL_ORDER.clear()
                else:
                    bot.sendMessage(chat_id, "Enter Number only !!\n Enter Your Order:", reply_markup=cancelmarkup)
            #####################

            elif 'BUY' in BUY_ORDER:
                Order = msg['text']
                if "/" in str(Order):
                    Order = str(Order).split("/")[1]
                if is_number(Order) == True:
                    self.buyorder('bxinth', Order, chat_id)
                    BUY_ORDER.clear()
                else:
                    bot.sendMessage(chat_id, "Enter Number only !!\n Enter Your Order:", reply_markup=cancelmarkup)

            #####################
            if msg['text'] == '/notify' or msg['text'] == "NOTIFY":
                bot.sendChatAction(chat_id, 'typing')
                bot.sendMessage(chat_id,"Note:\
                    \nIf you close notification program \
                    will take action stoploss,cutloss by directly\
                    \n------------\
                    \n\U0001F537 [/ON_BTS ] \
                    \n\U0001F534 [/OFF_BTS] \
                    \n\U0001F537 [/ON_CTS ] \
                    \n\U0001F534 [/OFF_CTS]\
                    \n\U0001F537 [/ON_BLS ] \
                    \n\U0001F534 [/OFF_BLS] \
                            ")
            if msg['text'] == "/ON_BTS" or msg['text'] == "/OFF_BTS" or msg['text'] == "/ON_CTS" \
                    or msg['text'] == "/OFF_CTS" or msg['text'] == "/ON_BLS" or msg['text'] == "/OFF_BLS":
                if msg['text'] == "/ON_BTS":
                    noti_bts = "ON"
                    bot.sendMessage(chat_id, "\U00002714 Open Notify (BTS) -> OK")
                if msg['text'] == "/OFF_BTS":
                    noti_bts = "OFF"
                    bot.sendMessage(chat_id, "\U00002714 Close Notify (BTS) -> OK")
                if msg['text'] == "/ON_CTS":
                    noti_sts = "ON"
                    bot.sendMessage(chat_id, "\U00002714 Open Notify (CTS) -> OK")
                if msg['text'] == "/OFF_CTS":
                    noti_sts = "OFF"
                    bot.sendMessage(chat_id, "\U00002714 Close Notify (CTS) -> OK")
                if msg['text'] == "/ON_BLS":
                    noti_bss = "ON"
                    bot.sendMessage(chat_id, "\U00002714 Open Notify (BLS) -> OK")
                if msg['text'] == "/OFF_BLS":
                    noti_bss = "OFF"
                    bot.sendMessage(chat_id, "\U00002714 Close Notify (BLS) -> OK")

            if msg['text'] == '/menu':
                self.coinmenu(chat_id)

            if msg['text'] == "/BXINTH" or msg['text'] == "BXINTH":
                EX.append('BXINTH')

            if 'BXINTH' in EX and '/buycoin' in CKCOMMAND or 'BXINTH' in EX and "BUY" in CKCOMMAND:
                bot.sendChatAction(chat_id, 'typing')
                #global NT
                NT == ""
                BX.append('bxinth')
                BX.append('buyCoin')
                self.coinbx(chat_id)
                CKCOMMAND.clear()
                EX.clear()
            elif 'BXINTH' in EX and '/salecoin' in CKCOMMAND or 'BXINTH' in EX and "SELL" in CKCOMMAND:
                bot.sendChatAction(chat_id, 'typing')
                NT == ""
                BX.append('bxinth')
                BX.append('saleCoin')
                self.coinbx(chat_id)
                CKCOMMAND.clear()
                EX.clear()
            elif 'BXINTH' in EX and '/cancelcoin' in CKCOMMAND or 'BXINTH' in EX and "CAN ORDER" in CKCOMMAND:
                bot.sendChatAction(chat_id, 'typing')
                BX.append('bxinth')
                BX.append('cancelCoin')
                self.coinbx(chat_id)
                CKCOMMAND.clear()
                EX.clear()
            elif 'BXINTH' in EX and '/ckcoininfo' in CKCOMMAND or 'BXINTH' in EX and "INFO" in CKCOMMAND:
                bot.sendChatAction(chat_id, 'typing')
                CKCOMMAND.clear()
                EX.clear()
                BX.append('bxinth')
                BX.append('coinInfo')
                self.coinbx(chat_id)
            elif 'coinInfo' in BX:
                coin = msg['text']
                if "/" in str(coin):
                    coin = str(coin).split("/")[1]
                market = "THB"
                bot.sendMessage(chat_id, str(get_coin_information(bxin, coin + "/" + market, 3)))
                ### Pause action notify
                Pause = "YES"



                ##"######## BUY COIN ##########"
                ### Check Coin infomation Buy coin and##
            if msg['text'] == '/buycoin' or msg['text'] == '/ckcoininfo' \
                    or msg['text'] == '/salecoin' or msg['text'] == '/cancelcoin' \
                    or msg['text'] == 'BUY' or msg['text'] == 'SELL' \
                    or msg['text'] == 'CAN ORDER' or msg['text'] == 'INFO':
                Pause = "YES"
                self.exchangemenu(chat_id,msg['text'])

            if 'bxinth' in BX or 'Cancel' in BX:
                Coin = COINTEMP[0]
                NT == ""
                ST = ""
                OPST=""
                Type=""
                Order = msg['text']
                if "/" in str(Order):
                    Order=str(Order).split("/")[1]
                if is_number(Order) == True and 'Cancel' in BX:
                    if cancel_coin(bxin, Order, Coin, 'bxinth') == True:
                        if simtest == "yes":
                            CT = ck_close_order_sim(Order, Coin, 'cancel', 'bxinth')
                            print("DEBUG Cancel=>" + str(CT))
                        else:
                            CT = ck_close_order(bxin, Order, Coin, 'cancel', 'bxinth')
                            print("DEBUG Cancel=>"+str(CT))

                        if CT[0] == True and CT[1] == "cancel":
                            bot.sendMessage(chat_id,emoji.emojize(':heavy_check_mark:')+"Cancel ["+Coin+"] OrderID:\"" + str(Order) + "\" => Completed",
                                            reply_markup=mainmenu)
                            CKCOMMAND.clear()
                            BX.clear()
                            COINTEMP.insert(0, "")
                            time.sleep(1)
                    else:
                        Update_OpenOrder(Order, 'bxinth', 'close')
                        if simtest == "yes":
                            CT = ck_close_order_sim(Order, Coin, 'cancel', 'bxinth')
                        else:
                            CT = ck_close_order(bxin, Order, Coin, 'cancel', 'bxinth')
                        if CT[0] == True and CT[1] == "cancel":
                            bot.sendMessage(chat_id,emoji.emojize(':heavy_check_mark:')+"Cancel "+Coin+" OrderID:\""+str(Order) + "\" => Completed",
                                            reply_markup=mainmenu)
                            CKCOMMAND.clear()
                            BX.clear()
                            COINTEMP.insert(0, "")
                            time.sleep(1)

             ######## SALE COIN ###########

            if 'bxinth' in BX and 'SELL' in BX and 'point_select_cts' not in CKLOSS:
                bot.sendChatAction(chat_id, 'typing')
                Rate = msg['text']  ## Rate of coin
                if "/" in str(Rate):
                    Rate=str(Rate).split("/")[1]
                print("Rate is "+str(Rate))
                if is_number(Rate) != True or Rate <= "0" and 'point_select_cts' not in CKLOSS:
                    bot.sendMessage(chat_id,"!! Enter Number only,Don't using text word or typing number zero\n Enter Coin Price Rate ?")
                if "cts" in STRATEGY and "point_select_cts" not in CKLOSS:
                    bot.sendMessage(chat_id, "Enter [CTS]CutLoss(%)")
                    CKLOSS.append('point_select_cts')
                    STRATEGY.clear()
                elif "point_select_cts" not in CKLOSS and "cts" not in STRATEGY:
                    bot.sendMessage(chat_id,"Do you want to apply [CTS] Strategy or Not ?\
                        \n[/YES]\n[/NO]")
                    BX.remove('SELL')
                    BX.append('RES_ACT_SELL')
            elif 'bxinth' in BX and 'RES_ACT_SELL' in BX and msg['text'] == "/YES" or msg['text'] == "YES" and 'RES_ACT_SELL' in BX:
                bot.sendChatAction(chat_id, 'typing')
                bot.sendMessage(chat_id,"Enter [CTS]CutLoss(%)")
                CKLOSS.append('point_select_cts')
            elif 'point_select_cts' in CKLOSS and is_number(msg['text'] == True):
                STOPPOINT.clear()
                CutLoss = msg['text']
                if is_number(CutLoss) != True:
                    bot.sendMessage(chat_id,"Enter Number Only!! \n Enter [CTS]CutLoss(%)")
                else:
                    Rate = float(Rate)
                    bot.sendMessage(chat_id, "CutLoss Price " + str(CutLoss) + "[%]\n >" + str(
                    Rate - (Rate * (int(CutLoss) / 100))) + " Bath")  ## TOV DEV
                    bot.sendMessage(chat_id, "\
                    \n [StopPoint Mode] \
                    \n[/Auto] \
                    \n[/Custom]\
                    \n ------------")
                    COUNT = 0
                    BX.clear()
                    CKLOSS.remove('point_select_cts')
                    CKLOSS.append('mode_sell')
            elif msg['text'] == "/Auto" and 'mode_sell' in CKLOSS:
                if is_number(CutLoss) == True:
                    bot.sendMessage(chat_id, "Enter [CTS]StopPoint(%):")
                    CKLOSS.append('stoploss_sell1')
                    msg['text'] = ""
                else:
                    bot.sendMessage(chat_id, 'Enter number only !! \
                        \nEnter StopLoss(%):')
            elif 'insert_point1_cts' in CKLOSS:
                point = msg['text']
                print("Debug> " + str(point) + ":" + str(COUNT) + "->" + str(STOPPOINT))
                if COUNT == 1 and is_number(point) == True:
                    STOPPOINT.append(point)
                elif is_number(point) == True and int(STOPPOINT[int(COUNT) - 2]) > int(point):
                    bot.sendMessage(chat_id, "Point less than previous value !\
                    \n")
                elif is_number(point) == True and int(STOPPOINT[int(COUNT) - 2]) < int(point):
                    STOPPOINT.append(point)
                    COUNT += 1
                if COUNT == 1 and is_number(point) == True:
                    COUNT += 1
                if COUNT > 5 and is_number(point) == True:
                    CKLOSS.remove('insert_point1_cts')
                    CKLOSS.append('stoploss_sell1')
                    bot.sendMessage(chat_id, "Enter [/Apply] For Continue ..")
                else:
                    if is_number(CutLoss) == True and COUNT <= 5 and is_number(point) == True:
                        bot.sendMessage(chat_id, "Enter Price StopPoint(" + str(COUNT) + "):")
                    else:
                        # COUNT+= 1
                        bot.sendMessage(chat_id, "Enter number only !! \
                        \nEnter Price StopPoint(""" + str(COUNT) + "):")
            elif msg['text'] == "/Custom" and 'mode_sell' in CKLOSS:
                COUNT += 1
                if is_number(CutLoss) == True and COUNT < 5:
                    bot.sendMessage(chat_id, "Enter Price StopPoint(" + str(COUNT) + "):")
                    CKLOSS.append('insert_point1_cts')
                    msg['text'] = ""
                else:
                    bot.sendMessage(chat_id, 'Enter number only !! \
                        \nEnter Price StopLoss(%):')

            elif 'bxinth' in BX and 'RES_ACT_SELL' in BX and msg['text'] == "/NO" or msg['text'] == "NO" and 'RES_ACT_SELL' in BX:
                bot.sendChatAction(chat_id, 'typing')
                Coin = COINTEMP[0]
                if "/" in str(Rate):
                    Rate=str(Rate).split("/")[1]
                print("DEBUG1:Rate price" + str(Rate))
                if is_number(Rate) == True and Rate != "0":
                    BL = Update_Balance_Exc('bxinth', Coin, 'THB', float(Sell), 'sell', "O", str(chat_id))
                    if BL[0] != True:
                        bot.sendMessage(chat_id, BL[1])
                    else:
                        bot.sendMessage(chat_id, "" + emoji.emojize(':hourglass:') + " Sell under Processing .. ")
                        if simtest != "yes":
                            Oid= sale_coin(bxin, Coin, float(Sell), float(Rate)) ##Dev112t
                            time.sleep(3)
                        else:
                            Oid = sale_coin_sim(Coin, float(Sell), float(Rate))  ##Dev112t
                            time.sleep(3)
                    if Oid == None:
                        Oid = 0
                    if is_number(Oid) == True and BL[0] == True:  ## Tes
                        Qty =(float(Sell) / float(Rate))
                        ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'),Coin,'sell', Rate,\
                                                  Qty,Sell, 'open','bxinth', 'normal')
                        if ST == "OK":
                            bot.sendMessage(chat_id, "Sell:" + Coin + "\nAmount:"+str(format_floatc(float(Sell),4))+ "  \nRate:" + str(
                            format_floatc(float(Rate),4)) + " Bath \n")
                            bot.sendMessage(chat_id, "" + emoji.emojize(':heavy_check_mark:') + "Open Order " + str(
                                Oid) + " --> Successfully")

                            CKCOMMAND.clear()
                            BX.clear()
                    else:
                        bot.sendMessage(chat_id, Oid)
                        CKCOMMAND.clear()
                        BX.clear()
                else:
                    print("DEBUG2 " + str(is_number(Rate)))
                    bot.sendMessage(chat_id, "!! Enter number only and don't using rate by zero ")
                    lastprice = (get_lastprice(bxin, Coin))
                    if is_number(lastprice) == True:
                        bot.sendMessage(chat_id, "Now[Last]:/" + str(lastprice)+"\
                        \nNow [Bids]:/"+str(get_coin_lastorder(bxin,Coin,'buy')[0])+"\
                        \nNow[Asks]:/" + str(get_coin_lastorder(bxin, Coin, 'sell')[0])+"")
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                    else:
                        bot.sendMessage(chat_id,str(lastprice))
                BX.clear()
                COINTEMP.insert(0, "")
           ### TOR DEV
            elif 'stoploss_sell1' in CKLOSS:
                bot.sendChatAction(chat_id, 'typing')
                Coin = COINTEMP[0]
                point=True
                if len(STOPPOINT) == 0:
                    StopLoss = msg['text']
                    if is_number(StopLoss) != True:
                        bot.sendMessage(chat_id,"Enter Number Only \nEnter [CTS]StopPoint(%):")
                        point=False
                    if simtest == "yes" and point == True:
                        lastprice = get_lastprice_sim(Coin, 'bxinth')
                        bot.sendMessage(chat_id, "Start[StopLoss] " + str(StopLoss) + "[%]\n >" + str(
                            lastprice + (lastprice * (int(StopLoss) / 100))) + " Bath")  ## TOV DEV
                    elif simtest != "yes" and point == True:
                        lastprice = get_lastprice(bxin,Coin)
                        if is_number(lastprice) == True:
                            bot.sendMessage(chat_id, "Start[StopLoss] " + str(StopLoss) + "[%]\n >" + str(
                            lastprice + (lastprice * (int(StopLoss) / 100))) + " Bath")  ## TOV DEV
                        else:
                            bot.sendMessage(chat_id,str(lastprice))
                #Rate_ck=(get_coin_lastorder(bxin,Coin,'buy'))
                #Rate = check_sys("data=" + Rate + ";echo ${data#*/}")
                if is_number(Rate) == True and Rate != "0" and point == True:
                    if simtest != "yes":
                        BL = Update_Balance_Exc('bxinth', Coin, 'THB', float(Sell), 'sell',"O", str(chat_id))
                        if BL[0] != True:
                            bot.sendMessage(chat_id, BL[1])
                        else:
                            Oid = (sale_coin_res(Coin, float(Sell), float(Rate), 'bxinth'))  ## Open order sell temporary
                        if Oid == None:
                            Oid = 0
                        elif is_number(Oid) != True:
                            bot.sendMessage(chat_id, Oid)
                            CKCOMMAND.clear()
                            BX.clear()
                    elif simtest == "yes":
                        Oid = (sale_coin_res(Coin, float(Sell), float(Rate), 'bxinth'))  ## Open order sell temporary
                        if Oid == None:
                            Oid = 0
                        elif is_number(Oid) != True:
                            bot.sendMessage(chat_id, Oid)
                            CKCOMMAND.clear()
                            BX.clear()

                    if len(STOPPOINT) != 0:
                        StopLoss = ""
                        COUNT = 0
                        print(str(STOPPOINT))
                        for P in STOPPOINT:
                            StopLoss += P
                            if COUNT >= (len(STOPPOINT) - 1):
                                break
                            else:
                                StopLoss += ","
                                COUNT += 1
                        SK = Insert_ckloss(Oid, 'bxinth', str(StopLoss), CutLoss, '0')
                        print("Insert Database ID>" + str(Oid) + "\nStopLoss >" + str(StopLoss) + "\nCutLoss>" + str(
                            CutLoss))
                    else:
                        print("Insert Database ID>" + str(Oid) + "\nStopLoss >" + str(StopLoss) + "\nCutLoss>" + str(
                            CutLoss))
                        SK = Insert_ckloss(Oid, 'bxinth', StopLoss, CutLoss, '0')

                    if is_number(Oid) == True and SK == "OK":  ## Test
                        bot.sendMessage(chat_id, "Sell:" + Coin + "\nAmount:" + str(Sell) + "  \nRate:" + str(
                            Rate) + " Bath \n")

                        bot.sendMessage(chat_id, "" + emoji.emojize(':heavy_check_mark:') + "Open Order " + str(
                            Oid) + " --> Successfully")
                        CKCOMMAND.clear()
                        BX.clear()
                        COINTEMP.insert(0, "")

                elif is_number(Rate) != True or float(Rate) <= 0:
                    print("DEBUG2 " + str(is_number(Rate)))
                    bot.sendMessage(chat_id, "!! Enter number only and don't using rate by zero ")
                    lastprice=(get_lastprice(bxin, Coin))
                    if is_number(lastprice) == True:
                        bot.sendMessage(chat_id, "Now[Last]:/" + str(lastprice)+"\
                        \nNow [Bids]:/"+str(get_coin_lastorder(bxin,Coin,'buy')[0])+"\
                        \nNow[Asks]:/"+str(get_coin_lastorder(bxin, Coin, 'sell')[0])+"")
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                    else:
                        bot.sendMessage(chat_id,str(lastprice))


        ### BUY COIN ########
            if "bxinth" in BX and "BUY" in BX and "point_select_buy1" not in CKLOSS:
                bot.sendChatAction(chat_id, 'typing')
                Rate = msg['text']  ## Rate of coin
                if "/" in str(Rate):
                    Rate=str(Rate).split("/")[1]
                print("Rate Debug11 >"+str(Rate))
                if is_number(Rate) != True or float(Rate) <= 0 and "point_select_buy1" not in CKLOSS:
                    bot.sendMessage(chat_id, "Enter number Only ,Don't using text word!!\nEnter Coin Price Rate ?")

                if "bls" in STRATEGY and "point_select_buy1" not in CKLOSS:
                    bot.sendMessage(chat_id, 'Enter [BLS]StopRisk(%):')
                    CKLOSS.append('point_select_buy1')
                    STRATEGY.clear()
                    STRATEGY.append('blstobuy')
                elif "bts" in STRATEGY and "point_select_buy1" not in CKLOSS:
                    bot.sendMessage(chat_id, 'Enter [BTS]CutLoss(%):')
                    CKLOSS.append('point_select_buy1')
                    STRATEGY.clear()
                elif "bts" not in STRATEGY and "point_select_buy1" not in CKLOSS:
                    bot.sendMessage(chat_id, "Do you want to apply [BTS] Strategy or Not ?\
                        \n[/YES]|\n[/NO]")
                    BX.remove('BUY')
                    BX.append('RES_ACT_BUY')


            elif msg['text'] == "/YES" and 'RES_ACT_BUY' in BX  or msg['text'] == "YES" and 'RES_ACT_BUY' in BX:
                bot.sendMessage(chat_id,'Enter [BTS]CutLoss(%):')
                CKLOSS.append('point_select_buy1')
            elif 'point_select_buy1' in CKLOSS and is_number(msg['text'] == True):
                STOPPOINT.clear()
                if "blstobuy" in STRATEGY:
                    StopRisk = msg['text']
                    if is_number(StopRisk) != True:
                        bot.sendMessage(chat_id, 'Enter Number Only!! \n Enter [BLS]StopRisk(%):')
                    else:
                        print("Buy =>" + str(Buy))
                        Buy1 = float(Buy)
                        Rate = int(Rate)
                        print("Buy >" + str(Buy1))
                        rate_StopRisk = (Rate - (Rate * (int(StopRisk) / 100)))
                        profit_StopRisk = (Buy1 - (Buy1 * (int(StopRisk) / 100)))
                        bot.sendMessage(chat_id, "StopRisk Price " + str(StopRisk) + "[%]\
                            \n >" + str(rate_StopRisk) + "\
                            \n >" + str(profit_StopRisk) + " Bath")  ## TOV DEV

                        bot.sendMessage(chat_id, "\
                            \n [StopBuy Mode] \
                            \n[/Auto] \
                            \n[/Custom]\
                            \n ------------")
                        COUNT = 0
                        BX.clear()
                        CKLOSS.remove('point_select_buy1')
                        CKLOSS.append("bls_mode")
                else:
                    CutLoss = msg['text']
                    if is_number(CutLoss) != True:
                        bot.sendMessage(chat_id, 'Enter Number Only!! \n Enter [BTS]CutLoss(%):')
                    else:
                        print("Buy =>"+str(Buy))
                        Buy1=float(Buy)
                        Rate=int(Rate)
                        print("Buy >"+str(Buy1))
                        rate_cutloss=(Rate - (Rate * (int(CutLoss) / 100)))
                        profit_cutloss=(Buy1 - (Buy1*(int(CutLoss) /100)))
                        bot.sendMessage(chat_id,"CutLoss Price "+str(CutLoss)+"[%]\
                        \n >"+str(rate_cutloss)+"\
                        \n >"+str(profit_cutloss)+" Bath") ## TOV DEV

                        bot.sendMessage(chat_id, "\
                        \n [StopPoint Mode] \
                        \n[/Auto] \
                        \n[/Custom]\
                        \n ------------")
                        COUNT = 0
                        BX.clear()
                        CKLOSS.remove('point_select_buy1')
                        CKLOSS.append("buy_mode")
            elif msg['text'] == "/Auto" and "buy_mode" in CKLOSS:
                if is_number(CutLoss) == True:
                    bot.sendMessage(chat_id, "Enter BTS StopPoint(%):")
                    CKLOSS.append('stoploss_buy1')
                    msg['text'] = ""
                else:
                    bot.sendMessage(chat_id, 'Enter number only !! \
                        \nEnter StopLoss(%):')
            ### BLS MODE ##
            elif msg['text'] == "/Auto" and "bls_mode" in CKLOSS:
                if is_number(StopRisk) == True:
                    bot.sendMessage(chat_id, "Enter [BLS]StopBuy(%):")
                    CKLOSS.append('blsstop_buy')
                    msg['text'] = ""
                else:
                    bot.sendMessage(chat_id, 'Enter number only !! \
                        \nEnter [BLS]StopBuy(%):')
            elif 'buy_insert_point1' in CKLOSS:
                point = msg['text']
                print("Debug> " + str(point) + ":" + str(COUNT) + "->" + str(STOPPOINT))
                if COUNT == 1 and is_number(point) == True:
                    STOPPOINT.append(point)
                elif is_number(point) == True and int(STOPPOINT[int(COUNT) - 2]) > int(point):
                    bot.sendMessage(chat_id, "Point less than previous value !\
                    \n")
                elif is_number(point) == True and int(STOPPOINT[int(COUNT) - 2]) < int(point):
                    STOPPOINT.append(point)
                    COUNT += 1
                if COUNT == 1 and is_number(point) == True:
                    COUNT += 1
                if COUNT > 5 and is_number(point) == True:
                    CKLOSS.remove('buy_insert_point1')
                    CKLOSS.append('stoploss_buy1')
                    bot.sendMessage(chat_id, "Enter [/Apply] For Continue ..")
                else:
                    if is_number(CutLoss) == True and COUNT <= 5 and is_number(point) == True:
                        bot.sendMessage(chat_id, "Enter Price StopPoint(" + str(COUNT) + "):")
                    else:
                        # COUNT+= 1
                        bot.sendMessage(chat_id, "Enter number only !! \
                        \nEnter Price StopPoint(""" + str(COUNT) + "):")
            elif msg['text'] == "/Custom" and "buy_mode" in CKLOSS:
                COUNT += 1
                if is_number(CutLoss) == True and COUNT < 5:
                    bot.sendMessage(chat_id, "Enter Price StopPoint(" + str(COUNT) + "):")
                    CKLOSS.append('buy_insert_point1')
                    msg['text'] = ""
                else:
                    bot.sendMessage(chat_id, 'Enter number only !! \
                        \nEnter [BTS]CutLoss(%):')
            ## BLS MODE ##
            elif 'buy_insert_stopbuy' in CKLOSS:
                point = msg['text']
                print("Debug> " + str(point) + ":" + str(COUNT) + "->" + str(STOPPOINT))
                if COUNT == 1 and is_number(point) == True:
                    STOPPOINT.append(point)
                elif is_number(point) == True and int(STOPPOINT[int(COUNT) - 2]) < int(point):
                    bot.sendMessage(chat_id, "Point more than previous value !!\
                    \n")
                elif is_number(point) == True and int(STOPPOINT[int(COUNT) - 2]) > int(point):
                    STOPPOINT.append(point)
                    COUNT += 1
                if COUNT == 1 and is_number(point) == True:
                    COUNT += 1
                if COUNT > 5 and is_number(point) == True:
                    CKLOSS.remove('buy_insert_stopbuy')
                    CKLOSS.append('blsstop_buy')
                    bot.sendMessage(chat_id, "Enter [/Apply] For Continue ..")
                else:
                    if is_number(StopRisk) == True and COUNT <= 5 and is_number(point) == True:
                        bot.sendMessage(chat_id, "Enter Price StopBuy(" + str(COUNT) + "):")
                    else:
                        # COUNT+= 1
                        bot.sendMessage(chat_id, "Enter number only !! \
                        \nEnter Price StopBuy(""" + str(COUNT) + "):")
            elif msg['text'] == "/Custom" and "buy_mode" in CKLOSS:
                COUNT += 1
                if is_number(CutLoss) == True and COUNT < 5:
                    bot.sendMessage(chat_id, "Enter Price StopPoint(" + str(COUNT) + "):")
                    CKLOSS.append('buy_insert_point1')
                    msg['text'] = ""
                else:
                    bot.sendMessage(chat_id, 'Enter number only !! \
                        \nEnter [BTS]CutLoss(%):')

            elif msg['text'] == "/Custom" and "bls_mode" in CKLOSS:
                COUNT += 1
                if is_number(StopRisk) == True and COUNT < 5:
                    bot.sendMessage(chat_id, "Enter Price StopBuy(" + str(COUNT) + "):")
                    CKLOSS.append('buy_insert_stopbuy')
                    msg['text'] = ""
                else:
                    bot.sendMessage(chat_id, 'Enter number only !! \
                        \nEnter [BTS]StopRisk(%):')

            elif 'bxinth' in BX and 'RES_ACT_BUY' in BX and msg['text'] == "/NO" or msg['text'] == "NO" and 'RES_ACT_BUY' in BX :
                bot.sendChatAction(chat_id, 'typing')
                Coin = COINTEMP[0]
                if "/" in str(Rate):
                    Rate=str(Rate).split("/")[1]
                print("BuyRate:"+Rate)
                print("DEBUG1:Rate price" + str(Rate))
                if is_number(Rate) == True and Rate != "0" and is_number(Rate) == True:
                    BL = Update_Balance_Exc('bxinth', 'THB', 'THB', float(Buy), 'buy', "O", str(chat_id))
                    if BL[0] != True:
                        bot.sendMessage(chat_id, BL[1])
                    else:
                        bot.sendMessage(chat_id, "" + emoji.emojize(':hourglass:') + " Buy under Processing .. ")
                        if simtest != "yes":
                            Oid = buy_coin(bxin, Coin, float(Buy), float(Rate))  ##Dev112t
                            time.sleep(3)
                        else:
                            Oid = buy_coin_sim(Coin, float(Buy), float(Rate))  ##Dev112t
                            time.sleep(3)
                    if Oid == None:
                        Oid = 0

                    if is_number(Oid) == True and BL[0] == True:  ## Tes
                        Qty = (float(Buy) / float(Rate))
                        ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), Coin, 'buy', Rate,Qty, Buy, \
                                               'open', 'bxinth', 'normal')
                        if ST == "OK":
                            bot.sendMessage(chat_id, "" + emoji.emojize(':heavy_check_mark:') + "Open Order " + str(
                               Oid) + " --> Successfully")
                            bot.sendMessage(chat_id, "" + emoji.emojize(':clipboard:') + "[= Normal Result =]\
                               \nOrder:" + str(Oid) + "\
                               \nBuy:" + Coin + "\
                               \nPrice:" + str(float(Buy)) + " Bath \
                               \nRate:" + str(float(Rate)) + " Bath \
                               \nQuality:" + str(format_floatc((float(Buy) / float(Rate)),4)))
                        CKCOMMAND.clear()
                        BX.clear()
                    else:
                        bot.sendMessage(chat_id, Oid)
                        CKCOMMAND.clear()
                        BX.clear()
                else:
                    bot.sendMessage(chat_id, "!! Enter number only and don't using rate by zero ")
                    lastprice=(get_lastprice(bxin, Coin))
                    if is_number(lastprice) == True:
                        bot.sendMessage(chat_id, "Now[Last]:/" + str(lastprice) + "\
                       \nNow [Asks]:/" + str(get_coin_lastorder(bxin, Coin, 'sell')[0]) + "\
                       \nNow[Bids]:/" + str(get_coin_lastorder(bxin, Coin, 'buy')[0]) + "")
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                    else:
                        bot.sendMessage(chat_id,str(lastprice))
                BX.clear()
                COINTEMP.insert(0, "")
            #################################
            elif 'stoploss_buy1' in CKLOSS:
                bot.sendChatAction(chat_id, 'typing')
                point=True
                Oid = ""
                Bal = ""
                Coin = COINTEMP[0]
                #Rate = msg['text']
                if len(STOPPOINT) == 0:
                    StopLoss = msg['text']
                    if is_number(StopLoss) != True:
                        bot.sendMessage(chat_id,"Enter Number Only!! \nEnter [BTS]StopPoint(%)")
                        point=False
                    if simtest == "yes" and point == True:
                        lastprice = get_lastprice_sim(Coin,'bxinth')
                        bot.sendMessage(chat_id, "Start[StopLoss] " + str(StopLoss) + "[%]\n >" + str(
                        lastprice + (lastprice * (int(StopLoss) / 100))) + " Bath")  ## TOV D
                    elif simtest != "yes" and point == True:
                        lastprice = get_lastprice(bxin,Coin)
                        if is_number(lastprice) == True:
                            bot.sendMessage(chat_id, "Start[StopLoss] " + str(StopLoss) + "[%]\n >" + str(
                            lastprice + (lastprice * (int(StopLoss) / 100))) + " Bath")  ## TOV D
                        else:
                            bot.sendMessage(chat_id,str(lastprice))
                if "/" in str(Rate):
                    Rate=str(Rate).split("/")[1]
                print("Rate Debug" + str(Rate))
                if is_number(Rate) == True and Rate != "0" and point == True:
                    print("Rate1 " + str(Rate))
                    print("Coin1 " + str(Coin))
                    print("Buy" + str(Buy))
                    BL = Update_Balance_Exc('bxinth', 'THB', 'THB', float(Buy), 'buy',"O", str(chat_id))
                    if BL[0] != True:
                        bot.sendMessage(chat_id,BL[1])
                        BX.clear()
                        ORDERBUY.clear()
                        #STRATEGY.clear()
                        ## Return 201 if balance avireble
                    if simtest == "yes" and BL[0] == True:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Buy under Processing .. ")
                        Oid = (buy_coin_sim(Coin, float(Buy), float(Rate)))
                        time.sleep(3)
                    elif simtest != "yes" and BL[0] == True:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Buy under Processing .. ")
                        Oid = (buy_coin(bxin, Coin, float(Buy), float(Rate)))
                        time.sleep(3)
                        if is_number(Oid) == True and is_number(Oid) != None:  ## Sync Balance coin only ###
                            INFO = sync_balance_coin(bxin,'bxinth',Coin, str(chat_id))
                            print(INFO)
                            if INFO != "":  ## Return Error ##
                                print(INFO)
                                bot.sendMessage(chat_id,INFO)
                    print("Order ID:" + str(Oid))
                    if is_number(Oid) == True and BL[0] == True:  ## Test
                        Qty = (float(Buy) / float(Rate))
                        ST=Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), Coin, 'buy', Rate,Qty, Buy,'open', 'bxinth', 'bts')
                        ### Insert CKLOSS ###
                        if len(STOPPOINT) != 0:
                            StopLoss=""
                            COUNT=0
                            print(str(STOPPOINT))
                            for P in STOPPOINT:
                                StopLoss+=P
                                if COUNT >= (len(STOPPOINT)-1):
                                    break
                                else:
                                    StopLoss +=","
                                    COUNT += 1
                            SK=Insert_ckloss(Oid,'bxinth',str(StopLoss),CutLoss,'0')
                            print("Insert Database ID>"+str(Oid)+"\nStopLoss >"+str(StopLoss)+"\nCutLoss>"+str(CutLoss))
                            #SK="OK"
                        else:
                            print("Insert Database ID>" +str(Oid)+ "\nStopLoss >" +str(StopLoss)+ "\nCutLoss>" +str(CutLoss))
                            SK=Insert_ckloss(Oid, 'bxinth', StopLoss, CutLoss, '0')
                            #SK="OK"

                        if ST == "OK" and SK == "OK":
                            #bot.sendMessage(chat_id, "" + emoji.emojize(':heavy_check_mark:') + "Open Order " + str(
                            #Oid) + " --> Successfully")
                            bot.sendMessage(chat_id, ""+emoji.emojize(':clipboard:')+"[= Result =]\
                                \nOrder:" +str(Oid) + "\
                                \nBuy:" + Coin + "\
                                \nPrice:" +str(float(Buy)) + " Bath \
                                \nRate:" + str(float(Rate)) + " Bath \
                                \nQuality:" +str(format_floatc((float(Buy) / float(Rate)),4))\
                                )
                        ORDERBUY.append(Coin)
                        ORDERBUY.append(Buy)
                        ORDERBUY.append(Rate)
                        ORDERBUY.append(str(format_float(float(Buy) / float(Rate))))
                        ###############
                        BX.clear()
                        CKLOSS.clear()
                        COINTEMP.insert(0, "")
                        NT == "Noti"
                    elif Oid != "":
                         bot.sendMessage(chat_id,"Exchange Error =>"+str(Oid))
                    if BL[0] == True and is_number(Oid) == True:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Open Order " + str(Oid) + " is Successfully")
                        BX.clear()
                    else:
                        BX.clear()
                elif is_number(Rate) != True or float(Rate) <= 0:
                    bot.sendMessage(chat_id, "!! Enter number only and don't using rate by zero ")
                    lastprice=(get_lastprice(bxin, Coin))
                    if is_number(lastprice) == True:
                        bot.sendMessage(chat_id, "Now[Last]:/" + str(lastprice)+"\
                        \nNow [Asks]:/"+str(get_coin_lastorder(bxin,Coin,'sell')[0])+"\
                        \nNow[Bids]:/" + str(get_coin_lastorder(bxin, Coin, 'buy')[0]) + "")
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                    else:
                        bot.sendMessage(chat_id,str(lastprice))

            ### BLS STOPBUY ###
            elif 'blsstop_buy' in CKLOSS:
                bot.sendChatAction(chat_id, 'typing')
                point = True
                Oid = ""
                Bal = ""
                Coin = COINTEMP[0]
                StopBuy = ""
                # Rate = msg['text']
                if len(STOPPOINT) == 0:
                    StopBuy = msg['text']
                    if is_number(StopBuy) != True:
                        bot.sendMessage(chat_id, "Enter Number Only!! \nEnter [BLS]StopRisk(%)")
                        point = False
                    if simtest == "yes" and point == True:
                        lastprice = get_lastprice_sim(Coin, 'bxinth')
                        bot.sendMessage(chat_id, "Start[StopBuy] " + str(StopBuy) + "[%]\n >" + str(
                            lastprice + (lastprice * (int(StopBuy) / 100))) + " Bath")  ## TOV D
                    elif simtest != "yes" and point == True:
                        lastprice = get_lastprice(bxin, Coin)
                        if is_number(lastprice) == True:
                            bot.sendMessage(chat_id, "Start[StopBuy] " + str(StopBuy) + "[%]\n >" + str(
                            lastprice + (lastprice * (int(StopBuy) / 100))) + " Bath")  ## TOV D
                        else:
                            bot.sendMessage(chat_id,str(lastprice))

                if "/" in str(Rate):
                    Rate = str(Rate).split("/")[1]
                print("Rate Debug" + str(Rate))
                if is_number(Rate) == True and Rate != "0" and point == True:
                    print("Rate1 " + str(Rate))
                    print("Coin1 " + str(Coin))
                    print("Buy" + str(Buy))
                    BL = Update_Balance_Exc('bxinth', 'THB', 'THB', float(Buy), 'buy', "O", str(chat_id))
                    if BL[0] != True:
                        bot.sendMessage(chat_id, BL[1])
                        BX.clear()
                        ORDERBUY.clear()
                    if simtest == "yes" and BL[0] == True:
                        bot.sendMessage(chat_id, "" + emoji.emojize(':hourglass:') + " Buy under Processing .. ")
                        Oid = (buy_coin_bss_sim(Coin, float(Buy), float(Rate)))
                        time.sleep(3)
                    elif simtest != "yes" and BL[0] == True:
                        bot.sendMessage(chat_id, "" + emoji.emojize(':hourglass:') + " Buy under Processing .. ")
                        Oid = (buy_coin_bss(bxin, Coin, float(Buy), float(Rate)))
                    print("Order ID:" + str(Oid))
                    if is_number(Oid) == True and BL[0] == True:  ## Test
                        Qty = (float(Buy) / float(Rate))
                        ST = Insert_OpenOrder(Oid, time.strftime('%Y-%m-%d %H:%M:%S'), Coin, 'buy', Rate,Qty, Buy, \
                                            'open', 'bxinth', 'bls')
                        ### Insert CKLOSS ###
                        if len(STOPPOINT) != 0:
                            COUNT = 0
                            print(str(STOPPOINT))
                            for P in STOPPOINT:
                                StopBuy += P
                                if COUNT >= (len(STOPPOINT) - 1):
                                    break
                                else:
                                    StopBuy += ","
                                    COUNT += 1
                            SK = Insert_ckstopbuy(Oid, 'bxinth',str(StopRisk),str(StopBuy),'0')
                            print("Insert Database ID>" + str(Oid) + "\nStopLoss >" + str(StopBuy) + "\nCutLoss>" + str(
                                    StopRisk))
                        else: ## Dev7042561
                            print(
                                "Insert Database ID>" + str(Oid) + "\nStopLoss >" + str(StopBuy) + "\nCutLoss>" + str(
                                    StopRisk))
                            SK = Insert_ckstopbuy(Oid, 'bxinth', str(StopRisk), str(StopBuy), '0')

                        if ST == "OK" and SK == "OK":
                            bot.sendMessage(chat_id, "" + emoji.emojize(':clipboard:') + "[= Result =]\
                                \nOrder:" + str(Oid) + "\
                                \nBuy:" + Coin + "\
                                \nPrice:" + str(float(Buy)) + " Bath \
                                \nStart[Rate]:" + str(float(Rate)) + " Bath \
                                \nQuality:" + str(format_floatc((float(Buy) / float(Rate)), 4)) \
                                )
                        #ORDERBUY.append(Coin)
                        #ORDERBUY.append(Buy)
                        #ORDERBUY.append(Rate)
                        #ORDERBUY.append(str(format_float(float(Buy) / float(Rate))))
                        ###############
                        BX.clear()
                        CKLOSS.clear()
                        COINTEMP.insert(0, "")
                        NT == "Noti"
                    elif Oid != "":
                        bot.sendMessage(chat_id, "Exchange Error =>" + str(Oid))
                    if BL[0] == True and is_number(Oid) == True:
                        bot.sendMessage(chat_id, "" + emoji.emojize(':heavy_check_mark:') + "Open Order " + str(
                            Oid) + " is Successfully")
                        BX.clear()
                    else:
                        BX.clear()
                elif is_number(Rate) != True or float(Rate) <= 0:
                    bot.sendMessage(chat_id, "!! Enter number only and don't using rate by zero ")
                    lastprice=(get_lastprice(bxin, Coin))
                    if is_number(lastprice) == True:
                        bot.sendMessage(chat_id, "Now[Last]:/" + str(lastprice) + "\
                        \nNow [Asks]:/" + str(get_coin_lastorder(bxin, Coin, 'sell')[0]) + "\
                        \nNow[Bids]:/" + str(get_coin_lastorder(bxin, Coin, 'buy')[0]) + "")
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?", reply_markup=cancelmarkup)
                    else:
                        bot.sendMessage(chat_id,str(lastprice))

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
            ## POW BX ## 
            elif msg['text'] == '/POW' and 'bxinth' in BX or msg['text'] == 'POW' and 'bxinth' in BX:
                COINTEMP.insert(0, "POW/THB")
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

            if msg['text'] == '/asicdash' and chat_id not in setmail:
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
               # self.clear_state()
                self.clear_state()
                self.clear_strategy()
                bot.sendMessage(chat_id,"[ STRATEGY ] \
                   \n/BTS \
                   \n/BLS \
                   \n/CTS",reply_markup=selectst)

            elif msg['text'] == "/BTS" or msg['text'] == "/BLS" or msg['text'] == "/CTS" or \
                msg['text'] == "BTS" or msg['text'] == "BLS" or msg['text'] == "CTS":
                bot.sendChatAction(chat_id, 'typing')
                global SellStopLoss
                global SellCutLoss
                global BuyStopLoss
                global BuyCutLoss
                NT == ""
                BL=""
                self.clear_strategy()
                if msg['text'] == '/BTS' or msg['text'] == 'BTS':
                    bot.sendMessage(chat_id, "[ BTS MENU ] \
                        \n/NEW\
                        \n/CLOSE\
                        \n/UPDATE",reply_markup=mainmenust)
                    STRATEGY.append("bts")
                if msg['text'] == "/BLS" or msg['text'] == "BLS":
                    bot.sendMessage(chat_id, "[ BLS MENU ] \
                        \n/NEW\
                        \n/CLOSE\
                        \n/UPDATE",reply_markup=mainmenust)
                    STRATEGY.append("bls")
                if msg['text'] == "/CTS" or msg['text'] == "CTS":
                    bot.sendMessage(chat_id, "[ CTS MENU ] \
                        \n/NEW\
                        \n/CLOSE\
                        \n/UPDATE",reply_markup=mainmenust)
                    STRATEGY.append("cts")

                ## BTS,STS NEW ORDER ##
            elif msg['text'] == "/NEW" and "bts" in STRATEGY or msg[\
                'text'] == "/NEW" and "cts" in STRATEGY or msg['text'] == "/NEW" and "bls" in STRATEGY or \
                msg['text'] == "NEW" and "bts" in STRATEGY or msg[ 'text'] == "NEW" and "cts" in STRATEGY \
                or msg['text'] == "NEW" and "bls" in STRATEGY:
                if "bts" in STRATEGY:
                    #bot.sendMessage(chat_id, 'Enter BTS StopLoss(%):')
                    bot.sendMessage(chat_id, 'You Shoos [BTS] Strategy,BTS Strategy is Buy and Sell Coin to expensive !')
                    #CKLOSS.append('ckloss_buy')
                    #CKLOSS.append('point_select')
                    self.exchangemenu(chat_id, "BUY")
                if "cts" in STRATEGY:
                    #bot.sendMessage(chat_id, 'Enter CTS StopLoss(%):')
                    bot.sendMessage(chat_id, 'You Shoos [CTS] Strategy,CTS Strategy is Sell Coin to expensive !')
                    self.exchangemenu(chat_id, "SELL")
                    #CKLOSS.append('ckloss_sell')
                if "bls" in STRATEGY:
                    #bot.sendMessage(chat_id, 'Enter BLS StopRisk(%):')
                    #CKSTOPBUY.append('ckstop_risk')
                    bot.sendMessage(chat_id,'You Shoos [BLS] Strategy,BLS Strategy is Buy Coin to inexpensive !')
                    self.exchangemenu(chat_id, "BUY")

            ##BTS,STS UPDATE ORDER ##
            elif "UPDATE_NOW" in STRATEGY:
                INFO = ""
                #print("3.Check Strategy income" + str(STRATEGY))
                COUNT = 0
                Order = msg['text']
                if "/" in str(Order):
                    Uid=str(Order).split("/")[1]
                print("Order ID " + Uid)
                if is_number(Uid) == True:
                    if "stoploss_sell" in STRATEGY:
                        INFO = ""
                        ST1 = Update_StopLoss(Uid, 'bxinth', SellStopLoss)
                        ST2 = Update_CutLoss(Uid, 'bxinth', SellCutLoss)
                        if ST1 == "OK" and ST2 == "OK":
                            bot.sendMessage(chat_id,emoji.emojize(':heavy_check_mark:')+"Update New value Completed !!\
                             \n as information below", reply_markup=mainmenu)
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
                                    COUNT += 1
                                    INFO += ("\n(" + str(COUNT) + ")Update Trader [CTS] New!!")
                                    INFO += ("\n" + Time + "\
                                        \nOrder:[/" + str(order_id) + "]\
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
                                    STRATEGY.clear()
                        else:
                            bot.sendMessage(chat_id, "Update New value Failed !!", reply_markup=mainmenu)
                    elif "stoploss_buy" in STRATEGY:
                        INFO = ""
                        ST1 = Update_StopLoss(Uid, 'bxinth', BuyStopLoss)
                        ST2 = Update_CutLoss(Uid, 'bxinth', BuyCutLoss)
                        if ST1 == "OK" and ST2 == "OK":
                            bot.sendMessage(chat_id,emoji.emojize(':heavy_check_mark:')+"Update New value Completed !!", reply_markup=mainmenu)
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
                                    print("Order ID Update " + Uid)
                                    COUNT += 1
                                    INFO += ("\n(" + str(COUNT) + ")Update Trader [BTS] New!!")
                                    INFO += ("\n" + Time + "\
                                            \nOrder:[/" + str(order_id) + "]\
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
                                    STRATEGY.clear()
                    elif "ckstop_buy" in STRATEGY:
                        INFO = ""
                        ST1 = Update_StopRisk(Uid, 'bxinth', BuyStopRisk)
                        ST2 = Update_StopBuy(Uid, 'bxinth', BuyStopBuy)
                        if ST1 == "OK" and ST2 == "OK":
                            bot.sendMessage(chat_id, "Update (BLS)New value Completed !!", reply_markup=mainmenu)
                            SS = Get_OrderStopBuy('bxinth', 'buy')
                            for order in list(SS):
                                Time = (order[1])
                                order_id = (order[0])
                                coin = (order[2])
                                rate = (order[4])
                                qty = (order[3])
                                if order_id != Uid:
                                    continue
                                else:
                                    print("Order ID Update " + Uid)
                                    COUNT += 1
                                    INFO += ("\n(" + str(COUNT) + ")Update Trader [BLS] New!!\nCoin:" + coin)
                                    INFO += ("\n" + Time + "\
                                                    \nOrder:[/" + str(order_id) + "]\
                                                    \nCoin:" + coin + "\
                                                    \nQty:" + str(qty) + "\
                                                    \nRate:" + str(rate))
                                    volumn = format_float(qty / rate)
                                    INFO += ("\nVolumn:" + volumn)
                                    BuyStopRisk = Get_BittrexDB(order_id, 'bxinth', 'ckstopbuy', 'StopRisk')
                                    BuyStopBuy = Get_BittrexDB(order_id, 'bxinth', 'ckstopbuy', 'StopBuy')
                                    INFO += ("\nStopRisk:" + str(BuyStopRisk) + " %")
                                    INFO += ("\nStopBuy:" + str(BuyStopBuy) + " %")
                                    INFO += ("\n-------------------")
                                    bot.sendMessage(chat_id, INFO)
                                    STRATEGY.clear()
                    else:
                        bot.sendMessage(chat_id, "Update New value Failed !!", reply_markup=mainmenu)

                else:
                    bot.sendMessage(chat_id, "Error Not found Uid !!")


            elif msg['text'] == "/UPDATE" and "bts" in STRATEGY or msg['text'] == "/UPDATE" and "cts" in STRATEGY \
                    or msg['text'] == "/UPDATE" and "bls" in STRATEGY or msg['text'] == "UPDATE" and "bts" in STRATEGY \
                    or msg['text'] == "UPDATE" and "cts" in STRATEGY or msg['text'] == "UPDATE" and "bls" in STRATEGY:


                if "bts" in STRATEGY:
                    SS = Get_OrderBuy('bxinth', 'buy')
                    print("OrderBuy => " + str(SS))
                    if str(SS) == "()":
                        bot.sendMessage(chat_id, "Not Found Order For Update !!! ..", reply_markup=mainmenu)
                        time.sleep(2)
                        self.coinmenu(chat_id)
                        STRATEGY.clear()
                    else:
                        bot.sendMessage(chat_id, 'Enter [BTS] CutLoss(%)',reply_markup=mainmenu)
                        CKLOSS.append('ckloss_buy')
                        #STRATEGY.clear()
                        STRATEGY.append('bts_update')
                if  "cts" in STRATEGY:
                    SS = Get_OrderSale('bxinth', 'sell')
                    print("OrderSell =>" + str(SS))
                    if str(SS) == "()":
                        bot.sendMessage(chat_id, "Not Found Order For Update !!! ..", reply_markup=mainmenu)
                        time.sleep(2)
                        self.coinmenu(chat_id)
                        STRATEGY.clear()

                    else:
                        bot.sendMessage(chat_id, 'Enter [CTS] CutLoss(%)',reply_markup=mainmenu)
                        CKLOSS.append('ckloss_sell')
                        #STRATEGY.clear()
                        STRATEGY.append('cts_update')
                if "bls" in STRATEGY:
                    SS = Get_OrderStopBuy('bxinth', 'buy')
                    print("OrderBLS =>" + str(SS))
                    if str(SS) == "()":
                        bot.sendMessage(chat_id, "Not found Order for update !!! ..", reply_markup=mainmenu)
                        time.sleep(2)
                        self.coinmenu(chat_id)
                        STRATEGY.clear()
                    else:
                        bot.sendMessage(chat_id, 'Enter [BLS] StopRisk(%)',reply_markup=mainmenu)
                        CKSTOPBUY.append('ckstop_risk')
                       # STRATEGY.clear()
                        STRATEGY.append('bls_update')

############### END OF UPDATE ###############

            ##BTS,STS CLOSE ORDER ##
            elif "CLOSE_NOW" in STRATEGY or msg['text'] == "/NO":
                COUNT=0
                Order = msg['text']
                if "/" in str(Order):
                    Uid=str(Order).split("/")[1]
                if is_number(Uid) == True and 'close_bls' in CKSTOPBUY:
                    CKBL = Get_OrderStopBuy('bxinth', 'buy')
                    for order in list(CKBL):
                        order_id = (order[0])
                        coin = (order[2])
                        qty = (order[3])
                        if order_id == Uid:
                            #DEV113
                            BL = Update_Balance_Exc('bxinth','THB', 'THB', float(qty), 'buy', "C", str(chat_id))
                            break
                    if BL[0] == True:
                        CK = Update_OrderStopBuy(Uid, 'bxinth', 'close')
                    if CK == "OK":
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Close Order BLS\nOrder:" + str(Uid) + "\nStatus is Completed !!",
                                        reply_markup=cancelmarkup)
                        bot.sendMessage(chat_id, "Continue  to Close Order or,not?\
                        \n/YES\
                        \n/NO")
                        STRATEGY.clear()
                        CLOSECON.clear()
                        STRATEGY.append('bls')
                        CLOSECON.append("YES")
                    else:
                        bot.sendMessage(chat_id, "Update database to close order " +str(order_id) + " " + CK + "")
                        STRATEGY.clear()
                        CLOSECON.clear()
                elif is_number(Uid) == True and 'close_bts' in CKSTOPBUY:
                    CKBL = Get_OrderBuy('bxinth', 'buy')
                    for order in list(CKBL):
                        order_id = (order[0])
                        coin = (order[2])
                        qty = (order[3])
                        if order_id == Uid:
                            #DEV113
                            BL = Update_Balance_Exc('bxinth','THB', 'THB', float(qty), 'buy', "C", str(chat_id))
                            break
                    if BL[0] == True:
                        CK = Update_OrderBuy(Uid, 'bxinth', 'close')
                    if CK == "OK":
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Close Order BTS\nOrder: " +str(Uid) + "\nStatus is Completed !!",
                                        reply_markup=cancelmarkup)
                        bot.sendMessage(chat_id, "Continue to Close Order or,not?\n[/YES]||[/NO]")
                        STRATEGY.clear()
                        CLOSECON.clear()
                        STRATEGY.append('bts')
                        CLOSECON.append("YES")
                    else:
                        bot.sendMessage(chat_id, "Update database to close order " +str(order_id) + " " + CK + "")
                        STRATEGY.clear()
                        CLOSECON.clear()
                elif is_number(Uid) == True and 'close_cts' in CKSTOPBUY:
                    CKBL = Get_OrderSale('bxinth', 'sell')
                    for order in list(CKBL):
                        # Time = (order[1])
                        order_id = (order[0])
                        coin = (order[2])
                        rate = (order[4])
                        qty = (order[3])
                        if order_id == Uid:
                            #DEV113
                            volumn_st = format_floatc((qty/rate), 4)
                            BL = Update_Balance_Exc('bxinth', coin, 'THB', float(volumn_st), 'sell', "C", str(chat_id))
                            break
                    if BL[0] == True:
                        CK = Update_OrderSale(Uid, 'bxinth', 'close')
                    if CK == "OK":
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Close Order CTS\nOrder:" +str(Uid) + "\nStatus is Completed !!",
                                        reply_markup=cancelmarkup)
                        bot.sendMessage(chat_id, "Continue to Close Order or,not?\n[/YES]||[/NO]")
                        STRATEGY.clear()
                        CLOSECON.clear()
                        CLOSECON.append("YES")
                        STRATEGY.append('cts')
                    else:
                        bot.sendMessage(chat_id, "Update database to close order " + str(order_id) + " " + CK + "")
                        STRATEGY.clear()
                        CLOSECON.clear()

                elif 'cts' in STRATEGY and msg['text'] == "/YES":
                    # CLOSECON.clear()
                    CLOSECON.append("YES")
                    CLOSECON.append('cts')
                elif 'bts' in STRATEGY and msg['text'] == "/YES":
                    CLOSECON.append("YES")
                    CLOSECON.append('bts')
                elif 'bls' in STRATEGY and msg['text'] == "/YES":
                    CLOSECON.append("YES")
                    CLOSECON.append('bls')
                elif 'cts' in STRATEGY and msg['text'] == "/NO" or 'bls' in STRATEGY and msg['text'] == "/NO" \
                        or 'bts' in STRATEGY and msg['text'] == "/NO":
                    CLOSECON.clear()
                    STRATEGY.clear()
                    bot.sendMessage(chat_id, ""+emoji.emojize(':ok_hand_sign:')+"OK !!", reply_markup=mainmenu)


            elif msg['text'] == "/CLOSE" and "bts" in STRATEGY or msg['text'] == "/CLOSE" \
                    and "cts" in STRATEGY or msg['text'] == "/CLOSE" and "bls" in STRATEGY \
                    or "YES" in CLOSECON or msg['text'] == "CLOSE" and "bts" in STRATEGY \
                    or msg[ 'text'] == "CLOSE" and "cts" in STRATEGY or msg['text'] == "CLOSE" \
                    and "bls" in STRATEGY or "YES" in CLOSECON:

                if "bts" in STRATEGY:
                    COUNT+=1
                    INFO=""
                    SS = Get_OrderBuy('bxinth', 'buy')
                    print("OrderBuy => " + str(SS))
                    if str(SS) == "()":
                        bot.sendMessage(chat_id, "Not found Orde to close !!! ..", reply_markup=mainmenu)
                        time.sleep(3)
                        self.coinmenu(chat_id)
                        STRATEGY.clear()

                    else:
                        COUNT=0
                        COUNT+=1
                        bot.sendMessage(chat_id, 'Close Order BTS as Below !!', reply_markup=cancelmarkup)
                        SS = Get_OrderBuy('bxinth', 'buy')
                        for order in list(SS):
                            Time = (order[1])
                            order_id = (order[0])
                            coin = (order[2])
                            rate = (order[4])
                            qty = (order[3])
                            StopLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Stoploss')
                            CutLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Cutloss')
                            INFO += ("\n("+str(COUNT)+")Trader BTS " + coin)
                            INFO += ("\n" + Time + "\
                                            \nOrder:[/" + str(order_id) + "]\
                                            \nCoin:" + coin + "\
                                            \nQty:" + str(qty) + "\
                                            \nRate:" + str(rate))
                            volumn = format_float(qty / rate)
                            INFO += ("\nVolumn: " + volumn)
                            INFO += ("\nStopLoss" + str(StopLoss) + " %")
                            INFO += ("\nCutLoss:" + str(CutLoss) + " %")
                            bot.sendMessage(chat_id,INFO)
                            INFO=""
                            COUNT += 1
                        #STRATEGY.clear()
                        STRATEGY.append("CLOSE_NOW")
                        bot.sendMessage(chat_id, "Enter Order ID:")
                        CKSTOPBUY.clear()
                        CKSTOPBUY.append('close_bts')
                        ORDERBUY.clear()

                if "cts" in STRATEGY:
                    COUNT+=1
                    INFO=""
                    SS = Get_OrderSale('bxinth', 'sell')
                    print("OrderSell =>" + str(SS))
                    if str(SS) == "()":
                        bot.sendMessage(chat_id, "Not found Order to close !!! ..", reply_markup=mainmenu)
                        time.sleep(3)
                        self.coinmenu(chat_id)
                        STRATEGY.clear()

                    else:
                        bot.sendMessage(chat_id, 'Close Order CTS as Below !!', reply_markup=cancelmarkup)
                        SS = Get_OrderSale('bxinth', 'sell')
                        for order in list(SS):
                            Time = (order[1])
                            order_id = (order[0])
                            coin = (order[2])
                            rate = (order[4])
                            qty = (order[3])
                            StopLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Stoploss')
                            CutLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Cutloss')
                            INFO += ("\n("+str(COUNT)+")Trader CTS " + coin)
                            INFO += ("\n" + Time + "\
                                        \nOrder:[/" + str(order_id) + "]\
                                        \nCoin:" + coin + "\
                                        \nQty:" + str(qty) + "\
                                        \nRate:" + str(rate))
                            volumn = format_float(qty / rate)
                            INFO+= ("\nVolumn: " + volumn)
                            INFO+=("\nStopLoss:"+str(StopLoss)+" %")
                            INFO += ("\nCutLoss:" +str(CutLoss)+" %")
                            bot.sendMessage(chat_id, INFO)
                            INFO=""
                            COUNT += 1
                       # STRATEGY.clear()
                        STRATEGY.append("CLOSE_NOW")
                        bot.sendMessage(chat_id, "Enter Order ID:")
                        CKSTOPBUY.clear()
                        CKSTOPBUY.append('close_cts')
                        ORDERBUY.clear()
                print("Close Now" + str(STRATEGY))

                if "bls" in STRATEGY:
                    COUNT +=1
                    INFO=""
                    SS = Get_OrderStopBuy('bxinth', 'buy')
                    print("OrderBLS =>" + str(SS))
                    if str(SS) == "()":
                        bot.sendMessage(chat_id, "Not Found Order to Close !!! ..", reply_markup=mainmenu)
                        time.sleep(3)
                        self.coinmenu(chat_id)
                        STRATEGY.clear()
                    else:
                        bot.sendMessage(chat_id, 'Close Order BLS as Below !!', reply_markup=cancelmarkup)
                        SS = Get_OrderStopBuy('bxinth', 'buy')
                        for order in list(SS):
                            Time = (order[1])
                            order_id = (order[0])
                            coin = (order[2])
                            rate = (order[4])
                            qty = (order[3])
                            INFO += ("\n("+str(COUNT)+")Trader BLS " + coin)
                            INFO += ("\n" + Time + "\
                                    \nOrder:[/" + str(order_id) + "]\
                                    \nCoin:" + coin + "\
                                    \nQty:" + str(qty) + "\
                                    \nRate:" + str(rate))
                            volumn = format_float(qty / rate)
                            INFO += ("\nVolumn: " + volumn)
                            ##DEV113
                            BuyStopRisk = Get_BittrexDB(order_id, 'bxinth', 'ckstopbuy', 'StopRisk')
                            BuyStopBuy = Get_BittrexDB(order_id, 'bxinth', 'ckstopbuy', 'StopBuy')
                            INFO += ("\nStopRisk:" + str(BuyStopRisk) + " %")
                            INFO += ("\nStopBuy:" + str(BuyStopBuy) + " %")
                            INFO += ("\n----------------------")
                            bot.sendMessage(chat_id, INFO)
                            INFO=""
                            COUNT += 1
                        #STRATEGY.clear()
                        STRATEGY.append("CLOSE_NOW")
                        bot.sendMessage(chat_id, "Enter Order ID:")
                        CKSTOPBUY.clear()
                        CKSTOPBUY.append('close_bls')
                        ORDERBUY.clear()

            ### END CLOSE NOW ###


            ####### BLS ##########
            elif 'ckstop_risk' in CKSTOPBUY:
                StopRisk = msg['text']
                if is_number(StopRisk) == True:
                    bot.sendMessage(chat_id, "Enter BLS StopBuy(%):", reply_markup=cancelmarkup)
                    CKSTOPBUY.remove('ckstop_risk')
                    CKSTOPBUY.append('ckstop_buy')
                else:
                    bot.sendMessage(chat_id, 'Enter number only !! \
                        \nEnter StopRisk(%):', reply_markup=cancelmarkup)
                    #STRATEGY.clear()
                    ## Dev112
            elif "ckstop_buy" in CKSTOPBUY and "bls_update" in STRATEGY:  ## Update value
                INFO = ""
                StopBuy=msg['text']
                if is_number(StopBuy) == True:
                    BuyStopRisk = StopRisk
                    BuyStopBuy = StopBuy
                    bot.sendMessage(chat_id, "[Apply BLS to New Order] \
                               \n(%)StopRisk:" + str(BuyStopRisk) + " \
                               \n(%)StopBuy:" + str(BuyStopBuy) + " \
                               \n --------------- \
                               \n Next Step Update to BLS Order as below!!!")
                    # self.exchangemenu(chat_id, "ORDER BUY")
                SS = Get_OrderStopBuy('bxinth', 'buy')
                for order in list(SS):
                    Time = (order[1])
                    order_id = (order[0])
                    coin = (order[2])
                    rate = (order[4])
                    qty = (order[3])
                    INFO += ("\n("+str(COUNT)+")Trader BLS " + coin)
                    INFO += ("\n" + Time + "\
                        \nOrder:[/" + str(order_id) + "]\
                        \nCoin:" + coin + "\
                        \nQty:" + str(qty) + "\
                        \nRate:" + str(rate))
                    volumn = format_float(qty / rate)
                    INFO += ("\nVolumn: " + volumn)
                    ##DEV113
                    OStopRisk = Get_BittrexDB(order_id, 'bxinth', 'ckstopbuy', 'StopRisk')
                    OStopBuy = Get_BittrexDB(order_id, 'bxinth', 'ckstopbuy', 'StopBuy')
                    INFO += ("\nStopRisk:" + str(OStopRisk) + " %")
                    INFO += ("\nStopBuy:" + str(OStopBuy) + " %")
                    INFO += ("\n----------------------")
                    COUNT+=1
                bot.sendMessage(chat_id, INFO)
                STRATEGY.append("UPDATE_NOW")
                STRATEGY.append("ckstop_buy")
                bot.sendMessage(chat_id, "Enter Order ID:")
                CKSTOPBUY.clear()
                ORDERBUY.clear()

            elif 'ckstop_buy' in CKSTOPBUY: ##
                StopBuy = msg['text']
                if is_number(StopBuy) == True:
                    BuyStopRisk = StopRisk
                    BuyStopBuy = StopBuy
                    # CKCOMMAND.append("ORDER BUY")
                    bot.sendMessage(chat_id, "[Apply Order Buy to New Order] \
                              \n(%)StopRisk:" + str(BuyStopRisk) + " \
                              \n(%)StopBuy:" + str(BuyStopBuy) + " \
                              \n --------------- \
                              \n Next Step Create New order foy buy !!!")
                    self.exchangemenu(chat_id, "BUY")
                    CKSTOPBUY.clear()
                    ORDERBUY.clear()
                    #STRATEGY.clear()
                else:
                    bot.sendMessage(chat_id, 'Enter number only !! \
                            \nEnter BLS StopRisk(%):')

            ##### ## BTS ###########
           # elif 'point_select' in CKLOSS and is_number(msg['text'] == True):
           #     STOPPOINT.clear()
           #     CutLoss=msg['text']
           #     bot.sendMessage(chat_id,"\
           #     \n [StopPoint Mode] \
           #     \n[/Auto] \
           #     \n[/Custom]\
           #     \n ------------")
           #     COUNT = 0
           #     CKLOSS.remove('point_select')
           # elif msg['text'] == "/Auto":
           #     if is_number(CutLoss) == True:
           #         bot.sendMessage(chat_id, "Enter [BTS]StopPoint(%):")
           #         CKLOSS.append('stoploss_buy')
           #     else:
           #         bot.sendMessage(chat_id, 'Enter number only !! \
           #             \nEnter StopLoss(%):')
           # elif 'insert_point' in CKLOSS:
           #     point = msg['text']
           #     print("Debug> " + str(point) + ":" + str(COUNT) + "->" + str(STOPPOINT))
           #     if COUNT == 1 and is_number(point) == True:
           #         STOPPOINT.append(point)
           #     elif is_number(point) == True and int(STOPPOINT[int(COUNT)-2]) > int(point):
           #         bot.sendMessage(chat_id,"Point less than previous value !\
           #         \n")
           #     elif is_number(point) == True and int(STOPPOINT[int(COUNT)-2]) < int(point):
           #         STOPPOINT.append(point)
           #         COUNT += 1
           #     if COUNT == 1 and is_number(point) == True :
           #         COUNT += 1
           #     if COUNT > 5 and is_number(point) == True :
           #         CKLOSS.remove('insert_point')
           #         CKLOSS.append('stoploss_buy')
           #         bot.sendMessage(chat_id,"Enter [/Apply] For Continue ..")
           #     else:
            #        if is_number(CutLoss) == True and COUNT <= 5 and is_number(point) == True:
            #            bot.sendMessage(chat_id, "Enter Price StopPoint(" + str(COUNT) + "):")
            #        else:
                        #COUNT+= 1
            #            bot.sendMessage(chat_id,"Enter number only !! \
            #            \nEnter Price StopPoint("""+str(COUNT)+"):")



           # elif msg['text'] == "/Custom":
           #     COUNT+=1
           #     if is_number(CutLoss) == True and COUNT < 5:
           #         bot.sendMessage(chat_id, "Enter Price StopPoint("+str(COUNT)+"):")
           #         CKLOSS.append('insert_point')
           #     else:
           #         bot.sendMessage(chat_id, 'Enter number only !! \
           #             \nEnter Price StopLoss(%):')

            ######### CTS ###########
            #elif 'ckloss_sell' in CKLOSS:
            #    CutLoss = msg['text']
            #    if is_number(CutLoss) == True:
            #       bot.sendMessage(chat_id, "Enter CTS CutLoss(%):")
            #       CKLOSS.remove('ckloss_sell')
            #        CKLOSS.append('stoploss_sell')
            #    else:
            #        bot.sendMessage(chat_id, 'Enter number only !! \
            #                    \nEnter CTS CutLoss(%):')

            elif 'stoploss_buy' in CKLOSS and "bts_update" in STRATEGY: ## Update value
                COUNT+=1
                INFO = ""
                StopLoss = msg['text']
                # Coin = COINTEMP[0]
                if is_number(StopLoss) == True:
                    BuyStopLoss = StopLoss
                    BuyCutLoss = CutLoss
                    # CKCOMMAND.append("ORDER BUY")
                    bot.sendMessage(chat_id, "[Apply BTS to New Order] \
                               \n(%)StopLoss:" + str(BuyStopLoss) + " \
                               \n(%)CutLoss:" + str(BuyCutLoss) + " \
                               \n --------------- \
                               \n Next Step Update to BTS order as below!!!")
                    # self.exchangemenu(chat_id, "ORDER BUY")
                SS = Get_OrderBuy('bxinth', 'buy')
                for order in list(SS):
                    Time = (order[1])
                    order_id = (order[0])
                    coin = (order[2])
                    rate = (order[4])
                    qty = (order[3])
                    INFO += ("\n("+str(COUNT)+")Trader[BTS] " + coin)
                    INFO += ("\n" + Time + "\
                        \nOrder:[/" + str(order_id) + "]\
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
                    COUNT+=1
                bot.sendMessage(chat_id, INFO)
                STRATEGY.append("UPDATE_NOW")
                STRATEGY.append("stoploss_buy")
                bot.sendMessage(chat_id, "Enter Order ID:")
                CKLOSS.clear()
                ORDERBUY.clear()
                # STRATEGY.clear()

            elif 'stoploss_sell' in CKLOSS and "cts_update" in STRATEGY: ## Update CTS Value
                INFO = ""
                StopLoss = msg['text']
                if is_number(StopLoss) == True:
                    SellStopLoss = StopLoss
                    SellCutLoss = CutLoss
                    # CKCOMMAND.append("ORDER SELL")
                    bot.sendMessage(chat_id, "[Apply CTS to new Order] \
                               \n(%)StopLoss:" + str(SellStopLoss) + " \
                               \n(%)CutLoss:" + str(SellCutLoss) + " \
                               \n --------------- \
                               \n Next step,Update to CTS Order as below !!!")
                    # self.exchangemenu(chat_id, "ORDER SELL")
                SS = Get_OrderSale('bxinth', 'sell')
                for order in list(SS):
                    Time = (order[1])
                    order_id = (order[0])
                    coin = (order[2])
                    rate = (order[4])
                    qty = (order[3])
                    INFO += ("\n("+str(COUNT)+")Trader[CTS]" + coin)
                    INFO += ("\n" + Time + "\
                        \nOrder:[/" + str(order_id) + "]\
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
                    COUNT+=1
                bot.sendMessage(chat_id, INFO)
                STRATEGY.append("UPDATE_NOW")
                STRATEGY.append("stoploss_sell")
                bot.sendMessage(chat_id, "Enter Order ID:")
                CKLOSS.clear()
                ORDERBUY.clear()
                # STRATEGY.clear()
            #---------------------------------#


                #ORDERBUY.clear()
                #STRATEGY.clear()
            #elif 'stoploss_buy' in CKLOSS and "bts_update" not in STRATEGY: ## New Value
            ### Update to open order database ##
            #    print("Update database Stoppoint 11")
            #    if len(STOPPOINT) == 0:
            #        StopLoss = msg['text']
            #        if is_number(StopLoss) == True:
            #            BuyStopLoss = StopLoss
            #            BuyCutLoss = CutLoss
            #            bot.sendMessage(chat_id, "[Apply Order Buy to New Order] \
            #            \n(%)StopPoint:" + str(BuyStopLoss) + " % \
            #            \n(%)CutLoss:" + str(BuyCutLoss) + " %\
            #            \n --------------- \
            #           \n Next Step Create New order  !!!")
            #        else:
            #            bot.sendMessage(chat_id, 'Enter number only !! \
            #                \nEnter BTS Stop loss(%)', reply_markup=cancelmarkup)
            #    elif msg['text'] == "/Apply":
            #        BuyStopLoss = ""
            #        COUNT = 0
            #        for point in STOPPOINT:
            #            COUNT += 1
            #            print("Point=" + str(point) + "\n")
            #            BuyStopLoss += "\n>>" + str(point) + ""
                    # if COUNT != 6:
                    #    BuyStopLoss += ","
            #        bot.sendMessage(chat_id, "[Apply Custom Point to New Order] \
            #            \n[(Value)StopPoint]" + str(BuyStopLoss) + " \
            #            \n(%)CutLoss:" + str(BuyCutLoss) + " % \
            #            \n --------------- \
            #            \n Next Step Create New order  !!!")
            #    self.exchangemenu(chat_id, "BUY")
            #    CKLOSS.clear()
            #    ORDERBUY.clear()
            # STRATEGY.clear()
            #elif 'stoploss_sell' in CKLOSS and "cts_update" not in STRATEGY:
            #    StopLoss = msg['text']
            #    if is_number(StopLoss) == True:
            #        SellStopLoss = StopLoss
            #        SellCutLoss = CutLoss
                    # CKCOMMAND.append("ORDER SELL")
            #        bot.sendMessage(chat_id, "[Apply Order Sell to New Order] \
            #               \n(%)StopLoss:" + str(SellStopLoss) + " \
            #               \n(%)CutLoss:" + str(SellCutLoss) + " \
            #               \n --------------- \
            #               \n Next step,Create New Order to Sell !!!")
            #        self.exchangemenu(chat_id, "SELL")
            #        CKLOSS.clear()
            #        ORDERBUY.clear()
            #        STRATEGY.clear()
            #    else:
            #        bot.sendMessage(chat_id, 'Enter number only !! \
            #                \nEnter OrderSell Stop loss(%)', reply_markup=cancelmarkup)




                    ####### END STRATEGY ###
                    # if STRATEGY_CHECK == "ON":
                    #simtest="yes"
                    #    print("Strategy Check Working --> Now")
                    #    self.bts('bxinth', chat_id)
                    #    self.sts('bxinth',chat_id)
                    #    self.check_close_order('bxinth',chat_id)

                    ## Algorithm Statigy ###

    def sellorder(self, exchange, order_sell, chat_id):
        order_id = ""
        CK_BUY=""
        CK_SELL=""

        ST = Get_OrderBuy(exchange, 'buy')
        if str(ST) != "()":
            for order in list(ST):
                Time = (order[1])
                order_id = (order[0])
                coin = (order[2])
                rate = (order[4])
                qty = (order[3])
                if order_sell == order_id:
                    CK_BUY = True
                    break
                else:
                    continue
        if CK_BUY != True:
            ST = Get_OrderSale(exchange, 'sell')
            if str(ST) != "()":
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
            if is_number(lastprice) == True and lastprice != None and order_id != 0 and order_id != None:
                if simtest == "yes":  ## for sim test only
                    fee = 0.0025
                    volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                    bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                    ST = sale_coin_sim(coin, float(volumn), float(lastprice))
                    time.sleep(3)
                    if is_number(ST) == True and CK_BUY != True:
                        CK1 = Update_OrderSale(order_id, exchange, 'trading')
                        CK2 = Update_OrderSale_Rate(order_id, exchange, lastprice) ## Update last price to sell
                        if CK1 == "OK" and CK2 == "OK":
                           bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update OrderSell to Trading status => Completed")
                        else:
                            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update OrderSell to Trading status => Completed")
                    else:
                        CK1 = Update_OrderBuy(order_id, exchange, 'trading')
                        CK2 = Update_OrderBuy_Rate(order_id, exchange, lastprice) ## Update last price to sell
                        if CK1 == "OK" and CK2 == "OK":
                            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update OrderBuy to Trading status => Completed")
                        else:
                            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update OrderBuy Trading status => Completed")

                elif simtest != "yes":  ## Real trading
                    fee = 0.0025
                    volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                    bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                    ST = sale_coin(bxin, coin, float(volumn), float(lastprice))
                    time.sleep(3)
                    if ST != "" and is_number(ST) != True and ST != "" and CK_BUY != True:
                        CK = Update_OrderSale(order_id, exchange, 'close')
                        if CK == "OK":
                            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                        else:
                            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                        ## report Error to user ##
                        bot.sendMessage(chat_id, "Exchange Error =>" + str(ST))
                    elif ST != "" and is_number(ST) != True and ST != "" and CK_BUY == True: ## Close Order BTSOrderBuy only
                        CK = Update_OrderBuy(order_id, exchange, 'close')
                        if CK == "OK":
                            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                        else:
                            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                        ## report Error to user ##
                        bot.sendMessage(chat_id, "Exchange Error =>" + str(ST))
                        ## Update balance coin##
                    if is_number(ST) == True:
                        INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                        print(INFO)
                        if INFO != "":  ## Return Error ##
                            bot.sendMessage(chat_id, INFO)
                    time.sleep(1)
                #both simtest and real test
                if is_number(ST) == True:
                    profit = (((lastprice / rate) * qty) - qty)
                    profit_fee = (profit - (profit * fee))
                    bot.sendMessage(chat_id, "!!Trading Sell Direct Completed !!\
                             \nCoin:" + coin + "\
                             \nOrder:" + str(order_id) + "\
                             \nBuy:" + str(qty) + "\
                             \nSold:" + str(format_float(((lastprice / rate) * qty))) + "\
                             \nChange Fee " + str(fee) + "\
                             \nProfit " + str(format_float(profit_fee)) + " Bath" \
                                        , reply_markup=mainmenu)
                    CK1 = Update_OrderSale(order_id, exchange, 'trading')
                    CK2 = Update_OrderSale_Rate(order_id,exchange,lastprice)
                    if CK1 == "OK" and CK2 == "OK":
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Out => Completed")
                    else:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Out => Completed")
                    return True
        else:
            bot.sendMessage(chat_id, "Not Found OrderBuy " + order_id + ",Please verify !!",reply_markup=mainmenu)
            return False

    def buyorder(self, exchange, order_buy, chat_id):
        order_id = ""
        CK_BUY = ""
        ST = Get_OrderStopBuy(exchange, 'buy')
        if str(ST) != "()":
            for order in list(ST):
                Time = (order[1])
                order_id = (order[0])
                coin = (order[2])
                rate = (order[4])
                qty = (order[3])
                if order_buy == order_id:
                    break
                else:
                    continue

        if order_buy == order_id:
            print("Buy Coin Order ! " + coin)
            print("" + Time + \
                  "\nOid:" + str(order_id) + \
                  "\nCoin" + coin + \
                  "\nQty" + str(qty) + \
                  "\nRate:" + str(rate))
            if simtest == "yes":
                lastprice = get_lastprice_sim(str(coin), exchange)
            else:
                lastprice = get_lastprice(bxin, str(coin))

            fee = 0.0025
            if is_number(lastprice) == True and lastprice != None and order_id != 0 and order_id != None:
                volumn_lt = format_float(qty / lastprice)
                volumn_coin = format_float(float(volumn_lt) - (float(volumn_lt) * fee))
                if simtest == "yes":
                    bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Buy under Processing .. ")
                    ST = (buy_coin_bss_sim(coin, float(qty), float(lastprice)))
                    time.sleep(3)
                    if is_number(ST) == True:
                        INFO = sync_balance_coin(bxin, exchange, coin, str(chat_id))
                        if INFO != "":  ## Return Error ##
                            bot.sendMessage(chat_id, INFO)

                elif simtest != "yes":
                    bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Buy under Processing .. ")
                    ST = (buy_coin_bss(bxin, coin, float(qty), float(lastprice)))
                    time.sleep(3)
                    if is_number(ST) == True:
                        INFO = sync_balance_coin(bxin, exchange, coin, str(chat_id))
                        if INFO != "":  ## Return Error ##
                            bot.sendMessage(chat_id, INFO)
                    if ST != "": ### Return Error and close Order ##
                        CK = Update_OrderSale(order_id, exchange, 'close')
                        if CK == "OK" and is_number(ST) != True:
                            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                            if INFO != "":  ## Return Error ##
                                bot.sendMessage(chat_id, INFO)
                        else:
                            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                        ## Error Report ###
                        bot.sendMessage(chat_id, "Exchange Error =>" + str(ST))
                if is_number(ST) == True and simtest == "yes" or simtest != "yes":
                    bot.sendMessage(chat_id, "!! Trading Buy Coin Direct Completed !!\
                             \nCoin:" + coin + "\
                             \nOrder:" + str(order_id) + "\
                             \nBuy:" + str(qty) + "\
                             \nChange Fee " + str(fee) + "\
                             \nVolumn:" + str(format_floatc(float(volumn_coin),4)), reply_markup=mainmenu)
                            ##############
                    CK1 = Update_OrderStopBuy(order_id, exchange, 'trading')
                    CK2 = Update_OrderStopBuy_Rate(order_id, exchange,lastprice)
                    if CK1 == "OK" and CK2 == "OK":
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Bought => Completed")
                    else:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Bought => Completed")
                    return True
        else:
            bot.sendMessage(chat_id, "Not Found Order " +order_id+ ",Please verify !!",reply_markup=mainmenu)
            return False

    def taskorder(self, exchange, chat_id):
        order_id = ""
        StopBuyPrice=""
        bts = True
        cts = True
        bls = True
        BL=""
        INFO = ""
        fee = 0.00025
        COUNT = 1
        #---------------#
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
                StopLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Stoploss')
                CutLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Cutloss')
                if simtest == "yes":
                    lastprice = get_lastprice_sim(str(coin), exchange)
                else:
                    lastprice = get_lastprice(bxin, str(coin))
                if is_number(lastprice) == True:
                    StopLoss_Point = lastprice - (lastprice * (StopLoss / 100))
                    CutLossPrice = (rate - (rate * (CutLoss / 100)))
                    MinProfit = (rate + (rate * (StopLoss / 100)))
                    print("Start Cost =>" + str(rate) + " Price Up =>" + str(format_floatc((lastprice - rate),4)) + " \n(+/-) =>" \
                    + str(format_floatc(((100 * (lastprice - rate)) / rate),4)) + "%")
                    profit = (((StopLoss_Point / rate) * qty) - qty)
                    profit_last = (((lastprice / rate) * qty) - qty)
                    profit_fee = (profit - (profit * fee))
                    profit_lastfee = (profit_last - (profit_last * fee))
                    INFO += ("(" + str(COUNT) + "):BTS Strategy Running\
                          \nCoin:" + coin + \
                         "\nStopLoss:" + str(StopLoss) + \
                         " %\nCutLoss:" + str(CutLoss) + \
                         " %\nCutLossPrice:" + str(format_floatc(CutLossPrice,4)) + \
                         "\nMiniProfit:" + str(format_floatc(MinProfit,4)) + \
                         "\nStartRate =>" + str(rate) + \
                         "\nPriceUp =>" + str(format_floatc((lastprice - rate),4)) + "\
                          \n(+/-) =>" + str( format_floatc((100 * (lastprice - rate) / rate), 4)) + \
                         "%\n------------------- \
                          \nOrder:/" + str(order_id) + \
                         "\nBuy:" + str(qty) + \
                         "\nRate:" + str(rate) + \
                         "\nNowLastPrice:" + str(lastprice) + \
                         "\nNowStopLoss(" + str(StopLoss) + " %):" + str(format_floatc(StopLoss_Point,4)) + \
                         "\nChangeFee:" + str(fee) + \
                         "\nProfit(StopLoss):" + str(format_floatc(profit_fee, 4)) + "  \
                          \nProfit(LastPrice):" + str(format_floatc(profit_lastfee, 4)) + " \
                          \n----------------------")
                    COUNT += 1
                    print(INFO)
                    bot.sendMessage(chat_id, INFO, reply_markup=mainmenu)
                    INFO = ""
                else:
                    bot.sendMessage(str(lastprice))

        else:
            bts = False
    ### BLS strategy ###
        ST = Get_OrderStopBuy(exchange, 'buy')
        if str(ST) != "()":
            for order in list(ST):
                Time = (order[1])
                order_id = (order[0])
                coin = (order[2])
                rate = (order[4])
                qty = (order[3])
                # --------#
                print("--------------------------")

                StopRisk = Get_BittrexDB(order_id,exchange, 'ckstopbuy', 'StopRisk')
                StopBuy = Get_BittrexDB(order_id,exchange, 'ckstopbuy', 'StopBuy')
                if simtest == "yes":
                    lastprice = get_lastprice_sim(str(coin), exchange)
                else:
                    lastprice = get_lastprice(bxin, str(coin))
                if is_number(lastprice) == True:
                    INFO+=("(" + str(COUNT) + "):BLS Strategy Running")
                    INFO+=("\nStartRate:" + str(rate))
                    INFO+=('\nStopRisk(%UP):' + str(StopRisk))
                    INFO+=(' %\nStopBuy(%DOWN):' + str(StopBuy))
                    INFO+=('\nLastPrice:' + str(lastprice))
                    StopRiskPrice = (rate + (rate * (StopRisk / 100)))
                    StopBuyPrice =(lastprice + (lastprice * (StopBuy / 100)))
                    volumn_st=format_floatc((qty / StopBuyPrice),4)
                    volumn_ls=format_floatc((qty / lastprice),4)
                    INFO+=('\nStopRisk:' + str(format_floatc(StopRiskPrice,4)))
                    INFO+=("\nStartRate:" + str(rate) + \
                       "\n Price Down:" + str(format_floatc((lastprice - rate),4)) + "\
                        \n(+/-) =>" + str(format_floatc((100 * (lastprice - rate)) / rate),4) + "%")
                    INFO+=("\n - ------------------ \
                        \nOrder: /" + str(order_id) + \
                        "\nBuy:" + str(qty) + \
                        "\nRate:" + str(rate) + \
                        "\nNowLastPrice:" + str(lastprice) + \
                        "\nNowStopBuy(" + str(StopBuy) + " %):" + str(StopBuyPrice) + \
                        "\nChangeFee:" + str(fee) + \
                        "\nVolumn(StopBuy):" + str(volumn_st) + " \
                         \nVolumn(LastPrice):" + str(volumn_ls) + " \
                         \n - ---------------------")
                    COUNT += 1
                    #bot.sendMessage(chat_id,INFO)
                    print(INFO)
                    bot.sendMessage(chat_id, INFO, reply_markup=mainmenu)
                    INFO = ""
                else:
                    bot.sendMessage(str(lastprice))
        else:
            bls = False

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
                if is_number(lastprice) == True:
                    StopLoss_Point = lastprice - (lastprice * (StopLoss / 100))
                    CutLossPrice = (rate - (rate * (CutLoss / 100)))
                    MinProfit = (rate + (rate * (StopLoss / 100)))
                    print("Start Cost =>" + str(rate) + " Price Up =>" + str(format_floatc((lastprice - rate),4)) + " \
                    (+/-) =>"+ str(format_floatc(((100 * (lastprice - rate)) / rate),4)) + "%")
                    profit = (((StopLoss_Point / rate) * qty) - qty)
                    profit_last = (((lastprice / rate) * qty) - qty)
                    profit_fee = (profit - (profit * fee))
                    profit_lastfee = (profit_last - (profit_last * fee))
                    INFO += ("(" + str(COUNT) + "):CTS Strategy Running \
                          \nCoin:" + coin + \
                         "\nStopLoss:" + str(StopLoss) + \
                         " %\nCutLoss:" + str(CutLoss) + \
                         " %\nCutLossPrice:" + str(format_floatc(CutLossPrice,4)) + \
                         "\nMiniProfit:" + str(format_floatc(MinProfit,4)) + \
                         "\nStartCost =>" + str(rate) + \
                         "\nPriceUp =>" + str(format_floatc((lastprice - rate),4)) + "\
                              \n(+/-) =>" + str(format_floatc(((100 * (lastprice - rate)) / rate), 4)) + \
                         "%\n---------------------- \
                          \nOrder:/" + str(order_id) + \
                         "\nSale Volumn:" + str(volumn) + \
                         "\nStartRate " + str(rate) + \
                         "\nNowLastPrice:" + str(lastprice) + \
                         "\nNowStopPoint(" + str(StopLoss) + " %):" + str(StopLoss_Point) + \
                         "\nChangeFee:" + str(fee) + \
                         "\nProfit(StopLoss):" + str(format_floatc(profit_fee, 4)) + "\
                             \nProfit(LastPrice):" + str(format_floatc(profit_lastfee, 4)) + "\
                             ")
                    COUNT += 1
                    #bot.sendMessage(chat_id, INFO)
                    print(INFO)
                    bot.sendMessage(chat_id, INFO, reply_markup=mainmenu)
                    INFO = ""
                else:
                    bot.sendMessage(str(lastprice))
        else:
            cts = False
            #bot.sendMessage(chat_id,"No Task Order STS !!")
        if bts == False and cts == False and bls == False:
            bot.sendMessage(chat_id, "Not Found Task Order Running !!",reply_markup=mainmenu)
            #- Init balance --- ##
            print("Start Init Balance ")
            if simtest != "yes" or simtest == "":
                print("Start Sync with BX")
                sync_balance_all(bxin,'bxinth',str(chat_id))
            ACT = ""



        #### Buy Low and sell expensive 1!!

    def taskorder(self, exchange, chat_id):
        order_id = ""
        bts = True
        cts = True
        bls = True
        StopLoss=""
        CutLoss=""
        BL = ""

        INFO = ""
        fee = 0.00025
        COUNT = 1
        # ---------------#
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
                #StopLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Stoploss')
                #CutLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Cutloss')

                StopLoss = Get_BittrexDB(order_id,exchange, 'ckloss', 'Stoploss')
                StopLoss = (list(StopLoss.split(',')))
                if len(StopLoss) > 1:
                    print("Using Custom Mode !!")
                    HaveCustom = True
                else:
                    HaveCustom = False
                    StopLoss = int(StopLoss[0])
                    print("Debug StopLoss >"+str(StopLoss))
                CutLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Cutloss')
                if simtest == "yes":
                    lastprice = get_lastprice_sim(str(coin), exchange)
                    if lastprice == "failed":
                        bts = False
                else:
                    lastprice = get_lastprice(bxin, str(coin))
                    if is_number(lastprice) != True:
                        bts = False

                if HaveCustom == False and is_number(lastprice) == True:
                    StopLoss_Point = lastprice - (lastprice * (StopLoss / 100))
                    MinProfit = (rate + (rate * (StopLoss / 100)))
                elif HaveCustom == True and is_number(lastprice) == True:
                    StopLoss_Point = Get_BittrexDB(order_id, exchange, 'ckloss', 'StoplossPoint')
                    if StopLoss_Point == 0.0:
                        StopLoss_Point=int(StopLoss[0])
                ####################

                if HaveCustom == True and is_number(lastprice) == True:
                    CutLossPrice = (rate - (rate * (CutLoss / 100)))
                    print("Start Rate =>" + str(rate) + " Price Up =>" + str(
                        format_floatc((lastprice - rate), 4)) + " \n(+/-) =>" \
                          + str(format_floatc(((100 * (lastprice - rate)) / rate), 4)) + "%")
                    profit = (((StopLoss_Point / rate) * qty) - qty)
                    profit_last = (((lastprice / rate) * qty) - qty)
                    profit_fee = (profit - (profit * fee))
                    profit_lastfee = (profit_last - (profit_last * fee))

                    INFO += ("(" + str(COUNT) + "):Mode[Custom] BTS Strategy\
                          \nCoin:" + coin+"")
                    INFO+=("\nStopLossPrice:")
                    for stoppoint in StopLoss:
                        INFO += ("\n>" + stoppoint)
                    INFO+=("\nCutLoss >[" + str(CutLoss) + \
                         "]%\nCutLossPrice >" + str(format_floatc(CutLossPrice, 4)) + \
                         "\nStartRate =>" + str(rate) + \
                         "\nPriceUp =>" + str(format_floatc((lastprice - rate), 4)) + "\
                          \n(+/-) =>" + str(format_floatc((100 * (lastprice - rate) / rate), 4)) + \
                         "%\n------------------- \
                          \nOrder:/" + str(order_id) + \
                         "\nBuy:" + str(qty*rate) + \
                         "\nRate:" + str(rate) + \
                         "\nNowLastPrice:" + str(lastprice) + \
                         "\nNext[StopPoint]:" + str(format_floatc(StopLoss_Point,4)) + \
                         "\nChangeFee:" + str(fee) + \
                         "\nProfit(StopPoint):" + str(format_floatc(profit_fee, 4)) + "  \
                          \nProfit(LastPrice):" + str(format_floatc(profit_lastfee, 4)) + " \
                          \n----------------------")
                elif HaveCustom != True and is_number(lastprice) == True:
                    CutLossPrice = (rate - (rate * (CutLoss / 100)))
                    print("Start Rate =>" + str(rate) + " Price Up =>" + str(
                        format_floatc((lastprice - rate), 4)) + " \n(+/-) =>" \
                          + str(format_floatc(((100 * (lastprice - rate)) / rate), 4)) + "%")
                    profit = (((StopLoss_Point / rate) * qty) - qty)
                    profit_last = (((lastprice / rate) * qty) - qty)
                    profit_fee = (profit - (profit * fee))
                    profit_lastfee = (profit_last - (profit_last * fee))
                    INFO += ("(" + str(COUNT) + "):Mode[Auto] BTS Strategy\
                        \nCoin:" + coin + \
                         "\nStopLoss:[" + str(StopLoss) + \
                         "]%\nCutLoss:[" + str(CutLoss) + \
                         "]%\nCutLossPrice >" + str(format_floatc(CutLossPrice, 4)) + \
                         "\nMiniProfit >" + str(format_floatc(MinProfit, 4)) + \
                         "\nStartRate =>" + str(rate) + \
                         "\nPriceUp =>" + str(format_floatc((lastprice - rate), 4)) + "\
                          \n(+/-) =>" + str(format_floatc((100 * (lastprice - rate) / rate), 4)) + \
                         "%\n------------------- \
                         \nOrder:/" + str(order_id) + \
                         "\nBuy:" + str(qty*rate) + \
                         "\nRate:" + str(rate) + \
                         "\nNowLastPrice:" + str(lastprice) + \
                         "\nNext[StopPoint(" + str(StopLoss) + " %)]:" + str(format_floatc(StopLoss_Point, 4)) + \
                         "\nChangeFee:" + str(fee) + \
                         "\nProfit(StopLoss):" + str(format_floatc(profit_fee, 4)) + "  \
                         \nProfit(LastPrice):" + str(format_floatc(profit_lastfee, 4)) + " \
                         \n----------------------")

                COUNT += 1
                #bot.sendMessage(chat_id,INFO)
                print(INFO)
                bot.sendMessage(chat_id, INFO, reply_markup=mainmenu)
                INFO = ""
        else:
            bts = False
            #bot.sendMessage(chat_id,"No task Order BTS")

        ##### BLS ######
        ST = Get_OrderStopBuy(exchange, 'buy')
        if str(ST) != "()":
            for order in list(ST):
                Time = (order[1])
                order_id = (order[0])
                coin = (order[2])
                rate = (order[4])
                qty = (order[3])
                # --------#
                print("--------------------------")

                StopBuy = Get_BittrexDB(order_id, exchange, 'ckstopbuy', 'StopBuy')
                StopBuy = (list(StopBuy.split(',')))
                if len(StopBuy) > 1:
                    print("Using Custom Mode !!")
                    HaveCustom = True
                else:
                    HaveCustom = False
                    StopBuy = int(StopBuy[0])
                    print("Debug StopBuy >" + str(StopBuy))
                StopRisk = Get_BittrexDB(order_id, exchange, 'ckstopbuy', 'StopRisk')

                if simtest == "yes":
                    lastprice = get_lastprice_sim(str(coin), exchange)
                    if lastprice == "failed":
                        bls = False
                else:
                    lastprice = get_lastprice(bxin, str(coin))
                    if is_number(lastprice) != True:
                        bls = False

                if HaveCustom == False and is_number(lastprice) == True:
                    StopBuyPoint = lastprice - (lastprice * (StopBuy / 100))
                else:
                    StopBuyPoint = Get_BittrexDB(order_id, exchange, 'ckstopbuy', 'StopBuyPoint')
                    if StopBuyPoint == 0.0:
                        StopBuyPoint = int(StopBuy[0])
                        ####################
                if HaveCustom == True and is_number(lastprice) == True:
                    INFO += ("(" + str(COUNT) + "):Mode[Custom] BLS Strategy")
                    INFO += ("\nStartRate:" + str(rate))
                    INFO += ('\nStopRisk(%UP):' + str(StopRisk))
                    INFO += (' %\nStopBuyPrice(DOWN):')
                    for stoppoint in StopBuy:
                        INFO += ("\n>" + stoppoint)
                    INFO += ('\nLastPrice:' + str(lastprice))
                    StopRiskPrice = (rate + (rate * (StopRisk / 100)))
                    StopBuyPrice=StopBuyPoint
                    volumn_st = format_floatc((qty / StopBuyPrice), 4)
                    volumn_ls = format_floatc((qty / lastprice), 4)
                    INFO += ('\nStopRisk:' + str(format_floatc(StopRiskPrice, 4)))
                    INFO += ("\nStartRate:" + str(rate) + \
                         "\n Price Down:" + str(format_floatc((lastprice - rate), 4)) + "\
                        \n(+/-) =>" + str(format_floatc(((100 * (lastprice - rate)) / rate), 4)) + "%")
                    INFO += ("\n - ------------------ \
                        \nOrder: /" + str(order_id) + \
                         "\nBuy:" + str(qty) + \
                         "\nRate:" + str(rate) + \
                         "\nNowLastPrice:" + str(lastprice) + \
                         "\nNext[StopBuy]:" + str(StopBuyPrice) + \
                         "\nChangeFee:" + str(fee) + \
                         "\nVolumn(StopBuy):" + str(volumn_st) + " \
                         \nVolumn(LastPrice):" + str(volumn_ls) + " \
                         \n - ---------------------")
                    COUNT += 1
                    print(INFO)
                    bot.sendMessage(chat_id, INFO, reply_markup=mainmenu)
                    INFO = ""
                elif HaveCustom != True and is_number(lastprice) == True:
                    INFO += ("(" + str(COUNT) + "):Mode[Auto] BLS Strategy")
                    INFO += ("\nStartRate:" + str(rate))
                    INFO += ('\nStopRisk(%UP):' + str(StopRisk))
                    INFO += ('\nStopBuy(%DOWN):' + str(StopBuy))
                    INFO += ('\nLastPrice:' + str(lastprice))
                    StopRiskPrice = (rate + (rate * (StopRisk / 100)))
                    StopBuyPrice = (lastprice + (lastprice * (StopBuy / 100)))
                    volumn_st = format_floatc((qty / StopBuyPrice), 4)
                    volumn_ls = format_floatc((qty / lastprice), 4)
                    INFO += ('\nStopRisk:' + str(format_floatc(StopRiskPrice, 4)))
                    INFO += ("\nStartRate:" + str(rate) + \
                             "\n Price Down:" + str(format_floatc((lastprice - rate), 4)) + "\
                            \n(+/-) =>" + str(format_floatc(((100 * (lastprice - rate)) / rate), 4)) + "%")
                    INFO += ("\n - ------------------ \
                            \nOrder: /" + str(order_id) + \
                             "\nBuy:" + str(qty) + \
                             "\nRate:" + str(rate) + \
                             "\nNowLastPrice:" + str(lastprice) + \
                             "\nNowStopBuy(" + str(StopBuy) + " %):" + str(StopBuyPrice) + \
                             "\nChangeFee:" + str(fee) + \
                             "\nVolumn(StopBuy):" + str(volumn_st) + " \
                             \nVolumn(LastPrice):" + str(volumn_ls) + " \
                             \n - ---------------------")
                    COUNT += 1
                    # bot.sendMessage(chat_id,INFO)
                    print(INFO)
                    bot.sendMessage(chat_id, INFO, reply_markup=mainmenu)
                    INFO = ""
        else:
            bls = False

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
                #StopLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Stoploss')
                #CutLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Cutloss')
                StopLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Stoploss')
                StopLoss = (list(StopLoss.split(',')))
                if len(StopLoss) > 1:
                    print("Using Custom Mode !!")
                    HaveCustom = True
                else:
                    HaveCustom = False
                    print("Debug StopLoss1 > "+StopLoss[0])
                    StopLoss = int(StopLoss[0])
                CutLoss = Get_BittrexDB(order_id, exchange, 'ckloss', 'Cutloss')
                if simtest == "yes":
                    print("Debug Coin >"+coin)
                    lastprice = get_lastprice_sim(str(coin), exchange)
                    print("Debug Lastprice >" + str(lastprice))
                    if lastprice == "failed":
                        cts = False
                else:
                    lastprice = get_lastprice(bxin, str(coin))
                    if is_number(lastprice) != True:
                        cts=False
                    print("Debug Lastprice >"+str(lastprice))
                if HaveCustom == False:
                    StopLoss_Point = ((rate) + ((rate) * (StopLoss / 100)))
                    MinProfit = (qty + (qty * (int(StopLoss) / 100)))
                else:
                    StopLoss_Point = Get_BittrexDB(order_id, exchange, 'ckloss', 'StoplossPoint')
                    if StopLoss_Point == 0.0:
                        StopLoss_Point=rate


                if HaveCustom == True and is_number(lastprice) == True:
                    CutLossPrice = (rate - (rate * (CutLoss / 100)))
                    print("Start Cost =>" + str(rate) + " Price Up =>" + str(format_floatc((lastprice - rate), 4)) + " \
                       (+/-) =>" + str(format_floatc(((100 * (lastprice - rate)) / rate), 4)) + "%")
                    profit = (((StopLoss_Point / rate) * qty) - qty)
                    profit_last = (((lastprice / rate) * qty) - qty)
                    profit_fee = (profit - (profit * fee))
                    profit_lastfee = (profit_last - (profit_last * fee))
                    INFO += ("(" + str(COUNT) + "):Mode[Custom] CTS Strategy\
                          \nCoin:" + coin +"")
                    INFO+=("\nStopLossPrice:")
                    for stoppoint in StopLoss:
                        INFO+=("\n>"+stoppoint)
                    INFO+=("\nCutLoss:" + str(CutLoss) + \
                         " %\nCutLossPrice:" + str(format_floatc(CutLossPrice, 4)) + \
                         "\nStartCost =>" + str(qty) + \
                         "\nPriceUp =>" + str(format_floatc((lastprice - rate), 4)) + "\
                              \n(+/-) =>" + str(format_floatc(((100 * (lastprice - rate)) / rate), 4)) + \
                         "%\n---------------------- \
                          \nOrder:/" + str(order_id) + \
                         "\nSale Volumn:" + str(volumn) + \
                         "\nStartRate " + str(rate) + \
                         "\nNowLastPrice:" + str(lastprice) + \
                         "\nNext[StopPoint]:" + str(StopLoss_Point) + \
                         "\nChangeFee:" + str(fee) + \
                         "\nProfit(StopLoss):" + str(format_floatc(profit_fee, 4)) + "\
                          \nProfit(LastPrice):" + str(format_floatc(profit_lastfee, 4)))
                elif HaveCustom != True and is_number(lastprice) == True:
                    CutLossPrice = (rate - (rate * (CutLoss / 100)))
                    print("Start Cost =>" + str(rate) + " Price Up =>" + str(format_floatc((lastprice - rate), 4)) + " \
                       (+/-) =>" + str(format_floatc(((100 * (lastprice - rate)) / rate), 4)) + "%")
                    profit = (((StopLoss_Point / rate) * qty) - qty)
                    profit_last = (((lastprice / rate) * qty) - qty)
                    profit_fee = (profit - (profit * fee))
                    profit_lastfee = (profit_last - (profit_last * fee))
                    INFO += ("(" + str(COUNT) + "):Mode[Auto] CTS Strategy \
                        \nCoin:" + coin + \
                             "\nStopLoss:" + str(StopLoss) + \
                             " %\nCutLoss:" + str(CutLoss) + \
                             " %\nCutLossPrice:" + str(format_floatc(CutLossPrice, 4)) + \
                             "\nMiniProfit:" + str(format_floatc(MinProfit, 4)) + \
                             "\nStartCost =>" + str(qty) + \
                             "\nPriceUp =>" + str(format_floatc((lastprice - rate), 4)) + "\
                            \n(+/-) =>" + str(format_floatc(((100 * (lastprice - rate)) / rate), 4)) + \
                             "%\n---------------------- \
                              \nOrder:/" + str(order_id) + \
                             "\nSale Volumn:" + str(volumn) + \
                             "\nStartRate " + str(rate) + \
                             "\nNowLastPrice:" + str(lastprice) + \
                             "\nNext[StopPoint(" + str(StopLoss) + " %)]:" + str(StopLoss_Point) + \
                             "\nChangeFee:" + str(fee) + \
                             "\nProfit(StopLoss):" + str(format_floatc(profit_fee, 4)) + "\
                           \nProfit(LastPrice):" + str(format_floatc(profit_lastfee, 4)) + "\
                           ")

                COUNT += 1
                #bot.sendMessage(chat_id, INFO)
                print(INFO)
                bot.sendMessage(chat_id, INFO, reply_markup=mainmenu)
                INFO = ""
        else:
            cts = False
            #bot.sendMessage(chat_id,"No Task Order STS !!")
        if bts == False and cts == False and bls == False:
            bot.sendMessage(chat_id, "Not found Task Order Running !!",reply_markup=mainmenu)
            #- Init balance --- ##
            print("Start Init Balance ")
            if simtest != "yes" or simtest == "":
                print("Start Sync with BX")
                sync_balance_all(bxin, 'bxinth', str(chat_id))
            ACT = ""



            #### Buy Low and sell expensive 1!!

    def orderwait(self, exchange, chat_id):
        order_id = ""
        bts = True
        cts = True
        bls = True
        BL = ""

        INFO = ""
        fee = 0.00025
        COUNT = 1
        # ---------------#
        INFO += ("[= ORDER WAIT =]\n\
                |Rank|Rate|Volumn|Coin|Type\n")
        ST = Get_OrderBuy(exchange, 'trading')
        if str(ST) != "()":
            for order in list(ST):
                Time = (order[1])
                order_id = (order[0])
                coin = (order[2])
                rate = (order[4])
                qty = (order[3])
                #--------#
                volumn_st = format_floatc((float(qty) /float(rate)), 4)
                CHECK=check_coin_list(bxin,coin,str(format_floatc(rate,4)),str(format_floatc(volumn_st,4)),'sell')
                if CHECK != None and CHECK[0] == True:
                    INFO+=(INFO+"|"+coin+"|asks")
                elif CHECK != None and CHECK[0] == False:
                    bot.sendMessage(chat_id, CHECK[1], reply_markup=mainmenu)
            if INFO != "":
                bot.sendMessage(chat_id, INFO, reply_markup=mainmenu)
            INFO = ""
        else:
            bts = False

        ST = Get_OrderStopBuy(exchange, 'trading')
        if str(ST) != "()":
            for order in list(ST):
                Time = (order[1])
                order_id = (order[0])
                coin = (order[2])
                rate = (order[4])
                qty = (order[3])
                # --------#
                volumn_st = format_floatc((float(qty) / float(rate)), 4)
                CHECK = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn_st,4)), 'buy')
                if CHECK != None and CHECK[0] == True:
                    INFO += (INFO + "|" + coin + "|bids")
                elif CHECK != None and CHECK[0] == False:
                    bot.sendMessage(chat_id, CHECK[1], reply_markup=mainmenu)
            if INFO != "":
                bot.sendMessage(chat_id, INFO, reply_markup=mainmenu)
            INFO = ""
        else:
            bls = False
            #bot.sendMessage(chat_id,"No task Order BTS")

            #------STS------#
        ST = Get_OrderSale(exchange, 'trading')
        if str(ST) != "()":
            for order in list(ST):
                Time = (order[1])
                order_id = (order[0])
                coin = (order[2])
                rate = (order[4])
                qty = (order[3])

                volumn_st = format_floatc((float(qty) / float(rate)), 4)
                CHECK = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn_st,4)), 'buy')
                if CHECK != None and CHECK[0] == True:
                    INFO += (INFO + "|" + coin + "|asks")
                elif CHECK != None and CHECK[0] == False:
                    bot.sendMessage(chat_id, CHECK[1], reply_markup=mainmenu)
            if INFO != "":
                bot.sendMessage(chat_id, INFO, reply_markup=mainmenu)
            INFO=""
        else:
            cts = False
            #bot.sendMessage(chat_id,"No Task Order STS !!")




            #### Buy Low and sell expensive 1!!

    def bls(self, exchange, chat_id):
        global noti_bss
        global allow_stopbuy_bss
        global allow_stoprisk_bss
        global allow_update_bss
        global allow_update_point_bss
        global allow_close_bss
        global NOTIBSS_INFO
        global ORDER
        COUNT = 1
        ST=""
        result = ""
        BL=""
        if exchange == 'bxinth':
            fee = 0.0025
        ODL = Get_OrderStopBuy(exchange, 'buy')
        if ODL == "()":
            return False
        for order in list(ODL):
            Time = (order[1])
            order_id = (order[0])
            coin = (order[2])
            rate = (order[4])
            qty = (order[3])
            print("---------------------\n")
            print("Starting trader[BLS] " + coin)
            print("" + Time + \
                  "\nOid:" + str(order_id) + \
                  "\nCoin" + coin + \
                  "\nQty" + str(qty) + \
                  "\nRate:" + str(rate))
            volumn = format_float(qty / rate)
            print("Volumn: " + volumn)
            print("### Start Trailling Stop BLS " + coin + " ###")
            ## Lastprice for test ###
            if simtest == "yes":
                lastprice = get_lastprice_sim(str(coin), exchange)
            else:
                lastprice = get_lastprice(bxin, str(coin))
            if is_number(lastprice) == True and lastprice != None and order_id != 0 and order_id != None:
                if simtest == "yes":
                    fee = 0.0025
                    #volumn = format_float(float(volumn) - (float(volumn) * fee))
                    # print("Real Volume Sell Update" + str(float(volumn) - (float(volumn) * fee)))
                    if noti_bss == "ON" and allow_update_bss != "YES":
                        NT = "Noti"
                    elif noti_bss == "ON" and allow_update_point_bss == "YES":
                        bot.sendMessage(chat_id, "Update Order:/" + str(order_id) + "\n")
                    elif noti_bss == "OFF" or allow_update_bss == "YES" and ORDER == order_id:
                        #ST = buy_coin_sim(coin, float(volumn), float(lastprice), exchange)
                        bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Buy under Processing .. ")
                        ST = (buy_coin_bss_sim(Coin, float(qty), float(lastprice)))
                        time.sleep(3)

                else:
                    fee = 0.0025
                    #volumn = format_float(float(volumn) - (float(volumn) * fee))
                    # print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))
                    if noti_bss == "ON" and allow_update_bss != "YES":
                        NT = "Noti"
                    elif noti_bss == "ON" and allow_update_point_bss == "YES":
                        bot.sendMessage(chat_id, "Update Order:/" + str(order_id) + "\n")
                    elif noti_bss == "OFF" or allow_update_bss == "YES" and ORDER == order_id:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Buy under Processing .. ")
                        ST = (buy_coin_bss(bxin,Coin, float(qty), float(lastprice)))
                        time.sleep(3)
                        if is_number(ST) == True:
                            INFO = sync_balance_coin(bxin, exchange,coin,str(chat_id))
                            if INFO != "":  ## Return Error ##
                                bot.sendMessage(chat_id, INFO)

                ## DEV##
                print("Buy update at " + str(lastprice) + " !!!")
                if is_number(ST) == True and allow_update_bss == "YES" and ORDER == order_id:
                    noti_bss = "ON"
                    # allow_cutloss = "NO" ## DEv112
                    CK1 = Update_OrderStopBuy(order_id, exchange, 'trading')
                    CK2 = Update_OrderStopBuy_Rate(order_id, exchange,lastprice)
                    if CK1 == "OK" and CK2 == "OK":
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Bought => Completed")
                    else:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status trading Bought => Completed" )
                if is_number(ST) == True and allow_update_bss == "YES" and ORDER == order_id:
                    fee = 0.0025
                    volumn = format_float(qty / lastprice)
                    volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                    bot.sendMessage(chat_id, "!!Action Update StopBuy Completed \
                         \nCoin:" + coin + "\
                         \nOrder:" + str(order_id) + "\
                         \nBuy:" + str(float(qty)) + "\
                         \nvolumn:" + str(volumn), reply_markup=mainmenu)
                    allow_update_bss = "NO"
                    NOTIBSS_INFO = ""
                    ORDER=""
                    ACT=""
                    continue
                elif ST != "" and is_number(ST) != True:
                    CK = Update_OrderStopBuy(order_id, exchange, 'close')
                    if CK == "OK":
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                    else:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                    bot.sendMessage(chat_id, 'Exchange Error =>'+str(ST))
                    allow_update_bss = "NO"
                    NOTIBSS_INFO = ""
                    ORDER = ""
                    ACT = ""
                    continue
                print("Debug allow update =>"+allow_update_bss)
                if allow_update_bss != "YES":
                    result = buy_StopBuy_shadow(order_id, exchange, lastprice, rate)
                    print("Status StopBuy =>" + str(result))
                if result != None and len(result) == 3:
                    if result[0] == "StopBuyUpdate":
                        StopBuy_Point = result[1]
                        NOTIBSS_INFO += ("\
                              \n(" + str(COUNT) + ")[ Update(BLS) Point ]\
                              \nOrder:/" + order_id + "\
                              \nCoin:" + coin + "\
                              \nPrice:" + str(float(StopBuy_Point)))
                        if NT == "Noti" and allow_update_bss == "NO":
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('bls_update')
                            print("!!! Update StopBuy Point at " + str(StopBuy_Point))
                            volumn_st = format_floatc((qty / StopBuy_Point),4)
                            volumn_ls = format_floatc((qty / lastprice),4)
                            NOTIBSS_INFO += ("\n"+emoji.emojize(':rocket:')+"UpdateStopPoint(BLS)" + coin +" "\
                                             "\nOrder:/" + str(order_id) + \
                                             "\nBuy:" +str(float(qty)) + \
                                             "\nRate:" +str(float(rate)) + \
                                             "\nNow[LastPrice]:" + str(lastprice) + \
                                             "\nNext[StopBuyPoint]:" + str(StopBuy_Point) + \
                                             "\nChange Fee:" + str(fee) + \
                                             "\nVolumn(StopBuy):" + str(volumn_st) + \
                                             "\nVolumn(LastPrice):" + str(volumn_ls) + " \
                                              \nAccept this Action or not?\n-->"+emoji.emojize(':rocket:')+" "+emoji.emojize(':rocket:')+" "+emoji.emojize(':rocket:')+"<--\
                                              \n"+emoji.emojize(':blue_circle:')+"/OK_" + order_id + "\
                                              \n"+emoji.emojize(':black_circle:')+"/UPDATE_" + order_id + "\
                                              \n"+emoji.emojize(':red_circle:')+"/CLOSE_" + order_id \
                                )
                            bot.sendMessage(chat_id, NOTIBSS_INFO, reply_markup=mainmenu)
                            COUNT += 1
                            NOTIBSS_INFO = ""
                            time.sleep(2)

                    ##

                    if result[0] == "StopBuy":
                        StopBuy_Price = result[1]
                        #time.sleep(2)
                        if "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTIBSS_INFO += ("\n----------------------\
                                 \n(" + str(COUNT) + ")"+emoji.emojize(':clipboard:')+"[= StopBuy(BLS) =] \
                                 \nOrder:/" + order_id + "\
                                 \nCoin:" + coin + "\
                                 \nPrice:" + str(float(StopBuy_Price)))
                        if simtest == "yes":
                            if noti_bss == "ON" and allow_stopbuy_bss != "YES":
                                NT = "Noti"
                            elif noti_bss == "OFF" or allow_stopbuy_bss == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+"Buy under Processing .. ")
                                ST = (buy_coin_bss_sim(coin, float(qty), float(StopBuy_Price)))
                                time.sleep(3)
                        else:
                            fee = 0.0025
                            if noti_bss == "ON" and allow_stopbuy_bss != "YES":
                                NT = "Noti"
                            elif noti_bss == "OFF" or allow_stopbuy_bss == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Buy under Processing .. ")
                                ST = (buy_coin_bss(bxin,coin, float(qty), float(StopBuy_Price)))
                                time.sleep(3)
                                if is_number(ST) == True:
                                    INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                                    if INFO != "":  ## Return Error ##
                                        bot.sendMessage(chat_id, INFO)

                        if NT == "Noti" and allow_stopbuy_bss == "NO" and "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('bls_stopbuy')
                            volumn_st = format_floatc((qty / StopBuy_Price),4)
                            volumn_ls = format_floatc((qty / lastprice),4)
                            NOTIBSS_INFO += ("\n ----------- \
                                     \n"+emoji.emojize(':star2:')+""+emoji.emojize(':star2:')+""+emoji.emojize(':star2:')+"\
                                     \n"+emoji.emojize(':exclamation:')+"Please Take Action StopBuy(BLS) Now!! \
                                     \nCoin:" + coin + "\
                                     \nStopBuy Percent:" + str(result[2]) + " % \
                                     \nBuy " + str(float(qty)) + "\
                                     \nVolumn " + str(volumn_st) + "\
                                     \nAccept this Action or not?\n----\
                                     \n"+emoji.emojize(':blue_circle:')+"/OK_" + order_id + "\
                                     \n"+emoji.emojize(':black_circle:')+"/UPDATE_" + order_id + "\
                                     \n"+emoji.emojize(':red_circle:')+"/CLOSE_" + order_id \
                                )
                            if Pause == "NO":
                                bot.sendMessage(chat_id, NOTIBSS_INFO)
                                COUNT += 1
                                NOTIBSS_INFO = ""
                                time.sleep(10)
                                print("Buy StopBuy at " + str(StopBuy_Price) + " !!!")
                            else:
                                NOTIBSS_INFO=""
                        if is_number(ST) == True and allow_stopbuy_bss == "YES" and order_id == ORDER:
                            noti_bss = "ON"
                            CK1 = Update_OrderStopBuy(order_id, exchange, 'trading')
                            CK2 = Update_OrderStopBuy_Rate(order_id, exchange,StopBuy_Price)
                            if CK1 == "OK" and CK2 == "OK":
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Action Trading StopBuy Status => Completed")
                            else:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Action Trading StopBuy Status => Completed")

                            allow_close_bss = "NO"
                            NOTIBSS_INFO = ""
                        ## Real Sale ###
                        if is_number(ST) == True and allow_stopbuy_bss == "YES" and order_id == ORDER:
                            volumn_st = format_floatc((qty / StopBuy_Price),4)
                            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"\
                             Action StopBuy(BLS) at " + str(result[2]) + " % Completed \
                            \nCoin:" + coin + "\
                            \nOrder:" + str(order_id) + "\
                            \nBuy:" + str(float(qty)) + "\
                            \nVolumn:" + str(volumn_st) + "\
                            \nChange Fee " + str(fee) + "", reply_markup=mainmenu)
                            print("Sale StopBuy at " + str(StopBuy_Price) + " !!!")
                            ### Update balance after buy ##
                            #DevBalance
                            ## Auto STS SellCoin By default StopLoss and CutLoss ##
                            BL = Update_Balance_Exc('bxinth', coin, 'THB', float(volumn_st), 'sell',"O", str(chat_id))
                            if BL[0] != True:
                                bot.sendMessage(chat_id, BL[1])
                            else:
                                Oid = (sale_coin_res(coin,float(volumn_st),float(lastprice),exchange))  ## Open order sell temporary
                            if Oid == None:
                                Oid = 0
                            if is_number(Oid) == True and BL[0] == True:  ## Test
                                NOTIBSS_INFO+=(""+emoji.emojize(':heavy_check_mark:')+"\
                                 Auto Continue Start(CTS) to Sell \
                                \nSell:"+coin + "\
                                \nAmount:"+str(volumn_st)+ " \
                                \nRate:"+str(float(lastprice))+"Bath")
                                NOTIBSS_INFO+=("\nAuto Open Order Sell "+str(Oid) + " Completed")
                                bot.sendMessage(chat_id,NOTIBSS_INFO)
                            else:
                                bot.sendMessage(chat_id,"Can't Auto continue Start(CTS) to sell coin..")
                            allow_stopbuy_bss = "NO"
                            NOTIBSS_INFO = ""
                            ORDER = ""
                            ACT = ""
                        elif ST != "" and is_number(ST) != True:
                            CK = Update_OrderStopBuy(order_id, exchange, 'close')
                            if CK == "OK": 
                               bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                            else:
                               bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                            bot.sendMessage(chat_id,"Exchange Error =>"+str(ST)) 
                            allow_stopbuy_bss = "NO"
                            NOTIBSS_INFO = ""
                            ORDER = ""
                            ACT = ""
                            continue


                    elif result[0] == "StopRisk":
                        LastPrice = result[1]
                        time.sleep(2)
                        if "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTIBSS_INFO += ("\n---------------------- \
                                \n(" + str(COUNT) + ")[== StopRisk(BLS) ==]\
                                \nOrder:/" + order_id + "\
                                \nCoin:" + coin + "\
                                \nPrice:" + str(float(LastPrice)))
                        if simtest == "yes":
                            fee = 0.0025
                            if noti_bss == "ON" and allow_stoprisk_bss != "YES":
                                NT = "Noti"
                            elif noti_bss == "OFF" or allow_stoprisk_bss == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+ " Buy under Processing .. ")
                                ST = (buy_coin_bss_sim(coin, float(qty), float(LastPrice)))
                                time.sleep(3)

                        else:
                            if noti_bss == "ON" and allow_stoprisk_bss != "YES":
                                NT = "Noti"
                            elif noti_bss == "OFF" or allow_stoprisk_bss == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Buy under Processing .. ")
                                ST = (buy_coin_bss(bxin,coin, float(qty), float(LastPrice)))
                                time.sleep(3)
                                if is_number(ST) == True:
                                    INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                                    if INFO != "":  ## Return Error ##
                                        bot.sendMessage(chat_id, INFO)

                        if NT == "Noti" and allow_stoprisk_bss == "NO" and "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append("bls_stoprisk")
                            volumn_st = format_floatc((qty / LastPrice),4)
                            NOTIBSS_INFO += ("\n--------------------- \
                            \n"+emoji.emojize(':exclamation:')+"Please Take Action StopRisk Now!!! \
                            \nCoin:" + coin + \
                            "\nBuy:" + str(float(qty)) + \
                            "\nVolumn:" + str(volumn_st) + "\
                             \nAccept this Action or not?\n----\
                             \n"+emoji.emojize(':blue_circle:')+"/OK_" + order_id + "\
                             \n"+emoji.emojize(':black_circle:')+"/UPDATE_" + order_id + "\
                             \n"+emoji.emojize(':red_circle:')+"/CLOSE_" + order_id \
                             )
                            bot.sendMessage(chat_id, NOTIBSS_INFO)
                            NOTIBSS_INFO = ""
                            time.sleep(6)
                            print("Buy StopRisk at " + str(LastPrice) + " !!!")
                        time.sleep(1)
                        if is_number(ST) == True and allow_stoprisk_bss == "YES" and order_id == ORDER:
                            noti_bss = "ON"
                            CK1 = Update_OrderStopBuy(order_id, exchange, 'trading')
                            CK2 = Update_OrderStopBuy_Rate(order_id, exchange,LastPrice)
                            if CK1 == "OK" and CK2 == "OK":
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Trading StopRisk => Completed")
                            else:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Trading StopRisk => Completed")
                            allow_close_bss = "NO"
                            NOTIBSS_INFO = ""

                        if is_number(ST) == True and allow_stoprisk_bss == "YES" and order_id == ORDER:
                            volumn_st = format_floatc((qty / LastPrice),4)
                            bot.sendMessage(chat_id,
                                            ""+emoji.emojize(':heavy_check_mark:')+\
                                            "Action StopRisk Completed\
                                            \nOrder:" + str(order_id) + "\
                                            \nCoin:" + coin + "\
                                            \nBuy:" + str(float(qty)) + "\
                                            \nVolumn:" + str(volumn_st), reply_markup=mainmenu)
                            print("Sale StopRisk at " + str(LastPrice) + " !!!")
                            ## Auto STS SellCoin By default StopLoss and CutLoss ##
                            BL = Update_Balance_Exc('bxinth', coin, 'THB', float(volumn_st), 'sell',"O", str(chat_id))
                            if BL[0] != True:
                                bot.sendMessage(chat_id, BL[1])
                            else:
                                Oid = (sale_coin_res(coin, float(volumn_st), float(LastPrice),exchange))  ## Open order sell temporary
                            if Oid == None:
                                Oid = 0
                            if is_number(Oid) == True and BL[0] == True:  ## Test
                                NOTIBSS_INFO += (""+emoji.emojize(':heavy_check_mark:')+"\
                                    Auto Continue Start(CTS) to Sell \
                                    \nSell:" + coin + "\
                                    \nAmount:" + str(volumn_st) + " \
                                    \nRate:" + str(LastPrice) + "Bath")
                                NOTIBSS_INFO += ("\nAuto Open Order(CTS Sell " + str(Oid) + " Completed")
                                bot.sendMessage(chat_id, NOTIBSS_INFO)
                            else:
                                bot.sendMessage(chat_id, "Can't Auto continue Start(CTS) to sell coin..")
                            allow_stoprisk_bss = "NO"
                            NOTIBSS_INFO = ""
                            COUNT += 1
                            ORDER = ""
                            ACT = ""
                        elif ST != "":
                            CK = Update_OrderStopBuy(order_id, exchange, 'close')
                            if CK == "OK":
                                bot.sendMessage(chat_id, 'Close StopRisk =>' + CK)
                            else:
                                bot.sendMessage(chat_id, 'Close StopRisk =>' + CK)
                            bot.sendMessage(chat_id,"Exchange Error =>"+str(ST))
                            allow_stoprisk_bss = "NO"
                            NOTIBSS_INFO = ""
                            COUNT += 1
                            ORDER = ""
                            ACT = ""
                            continue
                else:
                    print("Not Found Result trailling  !!")
                    continue

            else:
                print("Last Price is Null")
                continue

                ##################################################

    def bts(self, exchange, chat_id):

        global noti_bts
        global noti_sts
        global allow_cutloss_bts
        global allow_stoploss_bts
        global allow_update_bts
        global allow_update_point_bts
        global allow_close_bts
        global NOTIBTS_INFO
        global ORDER
        COUNT = 1
        BL=""
        ST=""
        result = ""
        #global NOTISTATE_ACTION
        if exchange == 'bxinth':
            fee = 0.0025
        ODL = Get_OrderBuy(exchange, 'buy')
        if str(ODL) == "()":
            return False
        for order in list(ODL):
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
                  "\nQty" + str(float(qty)) + \
                  "\nRate:" + str(float(rate)))
            volumn = format_floatc((qty / rate),2)
            print("Volumn: " + volumn)
            print("### Start Trailling Stop BTS " + coin + " ###")
            ## Lastprice for test ###
            if simtest == "yes":
                lastprice = get_lastprice_sim(str(coin), exchange)
            else:
                lastprice = get_lastprice(bxin, str(coin))
            if is_number(lastprice) == True and lastprice != None and order_id != 0 and order_id != None:
                if simtest == "yes":
                    fee = 0.0025
                    volumn = format_float(float(volumn) - (float(volumn) * fee))
                    # print("Real Volume Sell Update" + str(float(volumn) - (float(volumn) * fee)))
                    if noti_bts == "ON" and allow_update_bts != "YES":
                        NT = "Noti"
                    elif noti_bts == "ON" and allow_update_point_bts == "YES":
                        bot.sendMessage(chat_id, "Update Order:/" + str(order_id) + "\n")
                    elif noti_bts == "OFF" or allow_update_bts == "YES" and ORDER == order_id:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                        ST = sale_coin_sim(coin, float(volumn), float(lastprice))
                        time.sleep(3)
                else:
                    fee = 0.0025
                    volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                    # print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))
                    if noti_bts == "ON" and allow_update_bts != "YES":
                        NT = "Noti"
                    elif noti_bts == "ON" and allow_update_point_bts == "YES":
                        bot.sendMessage(chat_id, "Update Order:/" + str(order_id) + "\n")
                    elif noti_bts == "OFF" or allow_update_bts == "YES" and ORDER == order_id:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                        ST = sale_coin(bxin, coin, float(volumn), float(lastprice))
                        time.sleep(3)
                        if is_number(ST) == True:
                            INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                            if INFO != "":  ## Return Error ##
                                bot.sendMessage(chat_id, INFO)

                ## DEV##
                print("Sale update at " + str(lastprice) + " !!!")
                if is_number(ST)== True and allow_update_bts == "YES" and ORDER == order_id:
                    noti_bts = "ON"
                    # allow_cutloss = "NO"
                    CK1 = Update_OrderBuy(order_id, exchange, 'trading')
                    CK2 = Update_OrderBuy_Rate(order_id, exchange,lastprice)
                    #if CK1 == "OK" and CK2 == "OK":
                    #    bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Out => Completed")
                    #else:
                    #   bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Out => Completed")

                ## Real Sale ###
                if is_number(ST) == True and allow_update_bts == "YES" and ORDER == order_id:
                    profit = (((lastprice / rate)* qty) - (qty))
                    profit_fee = (profit - (profit * fee))
                    bot.sendMessage(chat_id, "!!Action Sell Trading Update Completed \
                         \nCoin:" + coin + "\
                         \nOrder:" + str(order_id) + "\
                         \nBuy:" + str(float(qty)) + "\
                         \nSold:" + str(format_floatc(((lastprice / rate) * qty), 2)) + "\
                         \nChange Fee " + str(fee) + "\
                         \nProfit " + str(format_floatc(profit_fee, 2)) + "Bath" \
                                    , reply_markup=mainmenu)

                    Insert_Profit(order_id, time.strftime('%Y-%m-%d %H:%M:%S'), exchange, coin, volumn, qty,
                                  format_floatc(((lastprice / rate) * qty), 3), format_floatc(profit_fee, 3))
                    ORDER=""
                    allow_update_bts = "NO"
                    NOTIBTS_INFO = ""
                    continue
                elif ST != "" and is_number(ST) != True:
                     CK =Update_OrderBuy(order_id, exchange, 'close')
                     if CK == "OK":
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                     else:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                     bot.sendMessage(chat_id,"Exchange Error =>"+str(ST))
                     continue

                if allow_update_bts != "YES":
                    result = buy_trailling_stop_shadow(order_id, exchange, lastprice, rate)
                    print("Status trailling =>" + str(result))
                if result != None and len(result) == 3:
                    if result[0] == "StopLossUpdate":
                        StopLoss_Point = result[1]
                        NOTIBTS_INFO += ("\n\
                              \n(" + str(COUNT) + ")[= Update Point(BTS) =]\
                              \nOrder:/" + order_id + "\
                              \nCoin:" + coin + "\
                              \nPrice:" + str(float(StopLoss_Point)))
                        if NT == "Noti" and allow_update_bts == "NO":
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('bts_update')
                            print("!!! Update StopLoss Point at " + str(StopLoss_Point))
                            profit = (((StopLoss_Point / rate) * qty) - qty)
                            profit_last = (((lastprice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            profit_lastfee = (profit_last - (profit_last * fee))
                            NOTIBTS_INFO += ("\n"+emoji.emojize(':rocket:')+"Update StopPoint(BTS) " + coin +" "\
                                             "\nOrder:/" + str(order_id) + \
                                             "\nBuy " + str(float(qty)) + \
                                             "\nRate " + str(float(rate)) + \
                                             "\nNow[LastPrice]:" + str(float(lastprice)) + \
                                             "\nNext[StopPoint]:" + str(float(StopLoss_Point)) + \
                                             "\nProfit(StopLoss):" + str(format_floatc(profit_fee, 2)) + \
                                             "\nProfit(LastPrice):" + str(format_floatc(profit_lastfee, 2)) + \
                                             "\nAccept this Action or not?\n-->"+emoji.emojize(':rocket:')+" "+emoji.emojize(':rocket:')+" "+emoji.emojize(':rocket:')+"<--\
                                             \n"+emoji.emojize(':blue_circle:')+"/OK_" + order_id + "\
                                             \n"+emoji.emojize(':black_circle:')+"/UPDATE_" + order_id + "\
                                             \n"+emoji.emojize(':red_circle:')+"/CLOSE_" + order_id \
                                )
                        bot.sendMessage(chat_id,NOTIBTS_INFO, reply_markup=mainmenu)
                        COUNT += 1
                        NOTIBTS_INFO = ""

                       ##

                    elif result[0] == "CutLoss":
                        CutLossPrice = result[1]
                        time.sleep(2)
                        if "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTIBTS_INFO += (
                                "(" + str(COUNT) + ")[= CutLoss(BTS) =] \
                                        \nOrder:/" + order_id + " \
                                        \nCoin:" + coin + " \
                                        \nNowLastPrice:" + str(float(lastprice)) + " \
                                        \nRateOrder:" + str(rate) + " \
                                        \nCutLossPrice:" + str(float(CutLossPrice)))
                        if simtest == "yes":
                            fee = 0.0025
                            volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                            print("Real Sim Volume Sell CutLoss " + str(float(volumn) - (float(volumn) * fee)))
                            # time.sleep(4)
                            if noti_bts == "ON" and allow_cutloss_bts != "YES":
                                NT = "Noti"
                            elif noti_bts == "OFF" or allow_cutloss_bts == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                                ST = sale_coin_sim(coin, float(volumn), float(CutLossPrice))
                                time.sleep(3)
                        else:
                            fee = 0.0025
                            volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                            print("Real Volume Sell CutLoss " + str(float(volumn) - (float(volumn) * fee)))
                            # time.sleep(4)
                            if noti_bts == "ON" and allow_cutloss_bts != "YES":
                                NT = "Noti"
                            elif noti_bts == "OFF" or allow_cutloss_bts == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                                ST = sale_coin(bxin, coin, float(volumn), float(CutLossPrice))
                                time.sleep(3)
                                if is_number(ST) == True:
                                    INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                                    if INFO != "":  ## Return Error ##
                                        bot.sendMessage(chat_id, INFO)

                        if NT == "Noti" and allow_cutloss_bts == "NO" and "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('bts_cutloss')
                            profit = (((CutLossPrice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            NOTIBTS_INFO += ("\
                                     \nPlease Take Action(BTS) CutLoss Now!! \
                                     \nCoin:" + coin + "\
                                     \nCutLoss Percent:" + str(result[2]) + " % \
                                     \nBuy " + str(float(qty)) + " \
                                     \nRate:" + str(float(rate)) + " \
                                     \nSold " + str(format_floatc(((CutLossPrice / rate) * qty), 2)) + "\
                                     \nChange Fee " + str(fee) + "\
                                     \nProfit " + str(format_floatc(profit_fee, 2)) + "\
                                     \nAccept this Action or not?\n----\
                                     \n"+emoji.emojize(':blue_circle:')+"/OK_" + order_id + "\
                                     \n"+emoji.emojize(':black_circle:')+"/UPDATE_" + order_id + "\
                                     \n"+emoji.emojize(':red_circle:')+"/CLOSE_" + order_id \
                                )
                            time.sleep(1)
                            if Pause == "NO":
                                bot.sendMessage(chat_id, NOTIBTS_INFO)
                                COUNT += 1
                                NOTIBTS_INFO = ""
                                time.sleep(10)
                                print("Sale Cut loss at " + str(CutLossPrice) + " !!!")
                            else:
                                NOTIBTS_INFO=""
                        if is_number(ST) == True and allow_cutloss_bts == "YES" and order_id == ORDER:
                            noti_bts = "ON"
                            #allow_cutloss = "NO"
                            CK1 = Update_OrderBuy(order_id, exchange, 'Close')
                            CK2 = Update_OrderBuy_Rate(order_id, exchange,CutLossPrice)
                            if CK1 == "OK" and CK2 == "OK":
                                bot.sendMessage(chat_id, 'Update Action CutLoss Trading Status => Completed')
                            else:
                                bot.sendMessage(chat_id, 'Update Action CutLoss Trading Status => Completed')

                            allow_close_bts = "NO"
                            NOTIBTS_INFO = ""
                        ## Real Sale ###
                        if is_number(ST) == True and allow_cutloss_bts == "YES" and order_id == ORDER:
                            profit = (((CutLossPrice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            bot.sendMessage(chat_id, "!! Action Cut Loss(BTS) trading at " + str(result[2]) + " % Completed \
                            \nCoin:" + coin + "\
                            \nOrder:" + str(order_id) + "\
                            \nBuy:" + str(float(qty)) + "\
                            \nSold:" + str(format_floatc(((CutLossPrice / rate) * qty), 2)) + "\
                            \nChange Fee " + str(fee) + "\
                            \nProfit " + str(format_floatc(profit_fee, 2)) + " Bath",
                                            reply_markup=mainmenu)

                            Insert_Profit(order_id, time.strftime('%Y-%m-%d %H:%M:%S'), exchange, coin,volumn,qty,format_floatc(((CutLossPrice / rate) * qty),3),format_floatc(profit_fee, 2))
                            allow_cutloss_bts = "NO"
                            NOTIBTS_INFO = ""
                            time.sleep(2)
                        elif ST != "" and is_number(ST) != True:
                             CK = Update_OrderBuy(order_id, exchange, 'close')
                             if CK == "OK":
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                             else:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                             bot.sendMessage(chat_id,"Exchange Error =>"+str(ST))
                             continue
                             

                    elif result[0] == "StopLoss":
                        LastPrice = result[1]
                        time.sleep(2)
                        if "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTIBTS_INFO += (
                                "\n(" + str(COUNT) + ")[== StopLoss(BTS) ==]\
                                        \nOrder:/" + order_id + "\
                                        \nCoin:" + coin + "\
                                        \nPrice:" + str(float(LastPrice)))
                        if simtest == "yes":
                            fee = 0.0025
                            volumn = format_float(float(volumn) - (float(volumn) * fee))
                            print("Real Volume Sell StopLoss " + str(float(volumn) - (float(volumn) * fee)))
                            # time.sleep(4)
                            if noti_bts == "ON" and allow_stoploss_bts != "YES":
                                print("NT=>Noti,simtest => yes")
                                NT = "Noti"
                            elif noti_bts == "OFF" or allow_stoploss_bts == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                                ST = sale_coin_sim(coin, float(volumn), float(LastPrice))
                                time.sleep(3)
                        elif simtest != "yes":
                            fee = 0.0025
                            volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                            print("Real Volume Sell StopLoss" + str(float(volumn) - (float(volumn) * fee)))
                            #time.sleep(4)
                            if noti_bts == "ON" and allow_stoploss_bts != "YES":
                                print("NT=>Noti,simtest => No")
                                NT = "Noti"
                                # time.sleep(4)
                            elif noti_bts == "OFF" or allow_stoploss_bts == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                                ST = sale_coin(bxin, coin, float(volumn), float(LastPrice))
                                time.sleep(3)
                                if is_number(ST) == True:
                                    INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                                    if INFO != "":  ## Return Error ##
                                        bot.sendMessage(chat_id, INFO)

                        if NT == "Noti" and allow_stoploss_bts != "YES" and "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append("bts_stoploss")
                            profit = (((LastPrice / rate) * qty) - qty)
                            fee = 0.0025
                            profit_fee = (profit - (profit * fee))
                            NOTIBTS_INFO += ("\n--------------------- \
                            \n"+emoji.emojize(':star2:')+""+emoji.emojize(':star2:')+""+emoji.emojize(':star2:')+"\
                            \n"+emoji.emojize(':exclamation:')+"Please Take Action StopLoss Now!!! \
                            \nCoin:" + coin + \
                            "\nBuy:" + str(float(qty)) + \
                            "\nSold:" + str(format_floatc(((LastPrice / rate) * qty), 2)) + "\
                            \nChange Fee " + str(fee) + "\
                            \nProfit " + str(format_floatc(profit_fee, 2)) + "Bath \
                            \nAccept this Action or not?\n----\n\
                            \n"+emoji.emojize(':blue_circle:')+"/OK_" + order_id + "\
                            \n"+emoji.emojize(':black_circle:')+"/UPDATE_" + order_id + "\
                            \n"+emoji.emojize(':red_circle:')+"/CLOSE_" + order_id \
                                )
                            if Pause == "NO":
                                bot.sendMessage(chat_id, NOTIBTS_INFO)
                                COUNT += 1
                                NOTIBTS_INFO = ""
                                print("Sale Stop loss at " + str(LastPrice) + " !!!")
                                print("Change fee" + str(fee))
                                print('Profit is ' + str(profit_fee))
                                time.sleep(10)
                            else:
                                NOTIBTS_INFO=""
                        if is_number(ST) == True and allow_stoploss_bts == "YES" and order_id == ORDER:
                            noti_bts = "ON"
                            #allow_stoploss = "NO"
                            CK1 = Update_OrderBuy(order_id, exchange, 'trading')
                            CK2 = Update_OrderBuy_Rate(order_id, exchange,LastPrice)
                            if CK1 == "OK" and CK2 == "OK":
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Out => Completed")
                            else:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Out => Completed")

                            allow_close_bts = "NO"
                            NOTIBTS_INFO = ""

                        if is_number(ST) == True and allow_stoploss_bts == "YES" and order_id == ORDER:
                            profit = (((LastPrice / rate) * qty) - qty)
                            fee = 0.0025
                            profit_fee = (profit - (profit * fee))

                            bot.sendMessage(chat_id,
                                            ""+emoji.emojize(':heavy_check_mark:')+" Action Trading StopLoss(BTS) Completed\
                                            \nOrder:" + str(order_id) + "\
                                            \nCoin:" + coin + "\
                                            \nBuy:" + str(float(qty)) + "\
                                            \nSold:" + str(format_floatc(((LastPrice / rate) * qty), 2)) + "\
                                            \nChange Fee:" + str(fee) + "\
                                            \nProfit:" + str(format_floatc(profit_fee, 2)) + " Bath",
                                            reply_markup=mainmenu)

                            Insert_Profit(order_id, time.strftime('%Y-%m-%d %H:%M:%S'), exchange, coin, volumn, qty,
                                          format_floatc(((LastPrice / rate) * qty), 3), format_floatc(profit_fee, 3))
                            print("Sale Stop loss at " + str(float(LastPrice)) + " !!!")
                            print("Change fee" + str(fee))
                            print('Profit is ' + str(profit_fee))
                            #CK = Update_coinbalance(exchange, coin, chat_id)
                            #if CK != False:
                            #    bot.sendMessage(chat_id, CK)
                            allow_stoploss_bts = "NO"
                            NOTIBTS_INFO = ""
                        elif ST != "" and is_number(ST) != True:
                             CK = Update_OrderBuy(order_id, exchange, 'close')
                             if CK == "OK":
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                             else:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                             bot.sendMessage(chat_id,"Exchange Error =>"+str(ST))
                             continue
                else:
                    print("Not Found Result trailling  !!")
                    continue
            else:
                print("Last Price is Null")
                continue

                ##################################################

    def cts(self, exchange, chat_id):
        global noti_bts
        global noti_sts
        global allow_cutloss_sts
        global allow_stoploss_sts
        global allow_update_sts
        global allow_update_point_sts
        global allow_close_sts
        global NOTISTS_INFO
        global ORDER
        COUNT = 1
        BL=""
        ST=""
        result = ""
        if exchange == 'bxinth':
            fee = 0.0025
        ODL = Get_OrderSale(exchange, 'sell')
        if str(ODL) == "()":
            return False
        for order in list(ODL):
            Time = (order[1])
            order_id = (order[0])
            coin = (order[2])
            rate = (order[4])
            qty = (order[3])
            print("---------------------\n")
            print("Starting trader CTS " + coin)
            print("" + Time + \
                  "\nOid:" + str(order_id) + \
                  "\nCoin:" + coin + \
                  "\nQty:" + str(float(qty)) + \
                  "\nRate:" + str(float(rate)))
            volumn = format_floatc((qty / rate),4)
            print("Volumn: " + volumn)
            print("### Start Trailling Stop CTS " + coin + " ###")
            ## Lastprice for test ###
            if simtest == "yes":
                lastprice = get_lastprice_sim(str(coin), exchange)
            else:
                lastprice = get_lastprice(bxin, str(coin))
            if lastprice == None and order_id == 0 and order_id == None and is_number(lastprice) != True:
               continue
            
            if is_number(lastprice) == True and lastprice != None and order_id != 0 and order_id != None:
                if simtest == "yes":
                    fee = 0.0025
                    volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                    # print("Real Volume Sell Update" + str(float(volumn) - (float(volumn) * fee)))
                    if noti_sts == "ON" and allow_update_sts != "YES":
                        NT = "Noti"
                    elif noti_sts == "OFF" or allow_update_sts == "YES" and ORDER == order_id:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                        ST = sale_coin_sim(coin, float(volumn), float(lastprice))
                        time.sleep(3)
                else:
                    fee = 0.0025
                    volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                    # print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))
                    if noti_sts == "ON" and allow_update_sts != "YES":
                        NT = "Noti"
                    elif noti_sts == "OFF" or allow_update_sts == "YES" and ORDER == order_id:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                        ST = sale_coin(bxin, coin, float(volumn), float(lastprice))
                        time.sleep(3)
                        if is_number(ST) == True:  ## Sync balance
                            INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                            if INFO != "":  ## Return Error ##
                                bot.sendMessage(chat_id, INFO)

                ## DEV##
                print("Sale update at " + str(lastprice) + " !!!")
                if is_number(ST) == True and allow_update_sts == "YES" and ORDER == order_id:
                    noti_sts = "ON"
                    # allow_cutloss = "NO"
                    CK1 = Update_OrderSale(order_id, exchange, 'trading')
                    CK2 = Update_OrderSale_Rate(order_id, exchange,lastprice)
                    if CK1 == "OK" and CK2 == "OK":
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Out => Completed")
                    else:
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Out => Completed")
                elif allow_close_sts == "YES" and order_id == ORDER:
                    noti_sts = "ON"
                    # allow_cutloss = "NO"
                    CK = Update_OrderSale(order_id, exchange, 'Close')
                    if CK == "OK":
                        bot.sendMessage(chat_id, "Close Order " + order_id + " =>" + CK)
                    else:
                        bot.sendMessage(chat_id, "Close Order " + order_id + " =>" + CK)

                        ## Real Sale ###
                if is_number(ST) == True and ST != None and allow_update_sts == "YES" and  ORDER == order_id:
                    profit = format_floatc((((float(lastprice) / float(rate)) * float(qty)) - float(qty)),4)
                    print("Profit is "+str(profit))
                    profit_fee = format_floatc((float(profit) - (float(profit) * float(fee))),4)
                    Sold=format_floatc(((float(lastprice) / float(rate)) * float(qty)), 4)
                    bot.sendMessage(chat_id, "!!Action Trading Sell(CTS) Update Completed \
                         \nCoin:" + coin + "\
                         \nOrder:" + str(order_id) + "\
                         \nBuy:" + str(float(qty)) + "\
                         \nSold:" + str(Sold) + "\
                         \nChange Fee:" + str(fee) + "\
                         \nProfit:" + str(format_floatc(float(profit_fee), 4)) + "Bath" \
                                    , reply_markup=mainmenu)

                    #else:
                    #    CK = Update_OrderSale(order_id, exchange, 'sold')
                    #    if CK == "OK":
                    #        bot.sendMessage(chat_id, "" + emoji.emojize( \
                    #            ':heavy_check_mark:') + "Update Status Sold Out =>" + CK)
                    #    else:
                    #        bot.sendMessage(chat_id, "" + emoji.emojize( \
                    #            ':heavy_check_mark:') + "Update Status Sold Out =>" + CK)

                    Insert_Profit(order_id, time.strftime('%Y-%m-%d %H:%M:%S'), exchange, coin, volumn, qty,
                                  format_floatc((float(lastprice / rate) * qty), 4), format_floatc(float(profit_fee), 4))
                    # print("Sale Update to Lastprice at " + str(lastprice) + " !!!")
                    #CK = Update_coinbalance(exchange, coin, chat_id)
                    #if CK != False:
                    #    bot.sendMessage(chat_id, CK)
                    ORDER=""
                    allow_update_sts = "NO"
                    NOTISTS_INFO = ""
                    continue
                elif ST != "" and is_number(ST) != True:
                     CK = Update_OrderSale(order_id, exchange, 'close')
                     if CK == "OK":
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                     else:
                       bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                     bot.sendMessage(chat_id,"Exchange Error =>"+str(ST))
                     continue

                if allow_update_sts != "YES":
                    result = sell_trailling_stop_shadow(order_id, exchange, lastprice, rate)
                    print("Status trailling =>"+str(result))
                if result != None and len(result) == 3:
                    if result[0] == "StopLossUpdate":
                        StopLoss_Point = result[1]
                        if "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTS_INFO += ("\
                              \n(" + str(COUNT) + ")[= Update Point(CTS) =]\
                              \nOrder:/" + order_id + "\
                              \nCoin:" + coin + "\
                              \nPrice:" + str(float(StopLoss_Point)) + "\
                              \n---------------")
                        if simtest == "yes":
                            fee = 0.0025
                            volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                            # print("Real Volume Sell Update" + str(float(volumn) - (float(volumn) * fee)))
                            if noti_sts == "ON" and allow_update_sts != "YES":
                                NT = "Noti"
                            elif noti_sts == "OFF" or allow_update_sts == "YES" and ORDER == order_id:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                                ST = sale_coin_sim(coin, float(volumn), float(lastprice))
                                time.sleep(3)
                        else:
                            fee = 0.0025
                            volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                            #print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))
                            if noti_sts == "ON" and allow_update_sts != "YES":
                                NT = "Noti"
                            elif noti_sts == "OFF" or allow_update_sts == "YES" and ORDER == order_id:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                                ST = sale_coin(bxin, coin, float(volumn), float(lastprice))
                                time.sleep(3)
                                if is_number(ST) == True:
                                    INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                                    if INFO != "":  ## Return Error ##
                                        bot.sendMessage(chat_id, INFO)

                        ## DEV##
                        if NT == "Noti" and allow_update_sts == "NO":
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('cts_update')
                            print("!!! Update Point CTS to " + str(StopLoss_Point))
                            profit = (((StopLoss_Point / rate) * qty) - qty)
                            profit_last = (((lastprice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            profit_lastfee = (profit_last - (profit_last * fee))
                            NOTISTS_INFO += ("\n"+emoji.emojize(':rocket:')+"UpdateStopPoint(CTS) " + coin +" "\
                                             "\nOrder:/" + order_id + \
                                             "\nSaleVolumn:" + str(float(volumn)) + \
                                             "\nRateStart:" + str(float(rate)) + \
                                             "\nQty:" + str(float(qty)) + \
                                             "\nNow[LastPrice]:" + str(float(lastprice)) + \
                                             "\nNext[StopPoint]:" + str(float(StopLoss_Point)) + \
                                             "\nChange Fee:" + str(fee) + \
                                             "\nProfit(StopLoss):" + str(format_floatc(float(profit_fee), 2)) + " \
                                         \nProfit(LastPrice):" + str(format_floatc(float(profit_lastfee), 2)) + "\
                                         \nAccept this Action or not?\n-->"+emoji.emojize(':rocket:')+" "+emoji.emojize(':rocket:')+" "+emoji.emojize(':rocket:')+"<--\
                                         \n"+emoji.emojize(':blue_circle:')+"/OK_" + order_id + "\
                                         \n"+emoji.emojize(':black_circle:')+"/UPDATE_" + order_id + "\
                                         \n"+emoji.emojize(':red_circle:')+"/CLOSE_" + order_id \
                                )
                            bot.sendMessage(chat_id, NOTISTS_INFO, reply_markup=mainmenu)
                            COUNT += 1
                            NOTISTS_INFO = ""
                            time.sleep(2)
                        print("Action Close Status" + allow_close_sts)
                        if is_number(ST) == True and allow_update_sts == "YES" and ORDER == order_id:
                            noti_sts = "ON"
                            # allow_stoploss = "NO"
                            CK1 = Update_OrderSale(order_id, exchange, 'trading')
                            CK2 = Update_OrderSale_Rate(order_id, exchange,lastprice)
                            if CK1 == "OK" and CK2 == "OK":
                                bot.sendMessage(chat_id,""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading Out => Completed")
                            else:
                                bot.sendMessage(chat_id, 'Update Status Trading Out => Completed')
                        elif allow_update_point_sts == "YES":
                            bot.sendMessage(chat_id, "Update New Point to Order:/" + str(order_id) + "\n")

                        if is_number(ST) == True and allow_update_sts == "YES" and ORDER == order_id:
                            profit = (((lastprice / rate) * qty) - qty)
                            fee = 0.0025
                            profit_fee = format_floatc(float(profit - (profit * fee)),4)
                            bot.sendMessage(chat_id,
                                            "!! Action Sale(CTS) Trading Update Completed \
                                            \nCoin:" + coin + \
                                            "\nOrder:/" + order_id + \
                                            "\nSale Volumn:" + str(float(volumn)) + \
                                            "\nRate Start:" + str(float(rate)) + \
                                            "\nQty:" + str(float(qty)) + \
                                            "\nSold:" + str(format_floatc(float((lastprice / rate) * qty), 2)) + \
                                            "\nChange Fee:" + str(fee) + \
                                            "\nProfit:" + str(format_floatc(float(profit_fee), 2)) + " Bath",
                                            reply_markup=mainmenu)

                            INFO = check_coin_list(bxin, coin, str(lastprice), str(volumn), 'sell')
                            if INFO != None:
                                if INFO[0] == True:
                                    bot.sendMessage(chat_id, "\nLAST ORDER \
                                                                        \nRank |Rate |volume\
                                                                         \n" + INFO)

                            Insert_Profit(order_id, time.strftime('%Y-%m-%d %H:%M:%S'), exchange, coin, volumn, qty,
                                          format_floatc(float((CutLossPrice / rate) * qty), 3), format_floatc(profit_fee, 2))
                            print("Sale Update at " + str(lastprice) + " !!!")
                            print("Change fee:" + str(fee))
                            print('Profit:' + str(profit_fee))
                            #CK = Update_coinbalance(exchange, coin, chat_id)
                            #if CK != False:
                            #    bot.sendMessage(chat_id, CK)
                            ORDER ==""
                            allow_update_sts = "NO"
                            NOTISTS_INFO = ""
                        elif ST != "" and is_number(ST) != True:
                            CK = Update_OrderSale(order_id, exchange, 'close')
                            if CK == "OK":
                               bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                            else:
                               bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                            bot.sendMessage(chat_id,"Exchange Error =>"+str(ST))
                            continue

                    if result[0] == "CutLoss":
                        CutLossPrice = result[1]
                        time.sleep(2)
                        if "UpdateAct" not in UPDATE_ACT:
                            NOTISTS_INFO += (
                                "(" + str(COUNT) + ")[= CutLoss(CTS) =]\
                                         \nOrder:/" + order_id + "\
                                         \nCoin:" + coin + "\
                                        \nNowLastPrice:" + str(float(lastprice)) + "\
                                         \nRateOrder:" + str(float(rate)) + "\
                                         \nCutLossPrice:" + str(float(CutLossPrice)))
                        if simtest == "yes":
                            fee = 0.0025
                            volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                            print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))

                            if noti_sts == "ON" and allow_cutloss_sts != "YES":
                                NT = "Noti"

                            elif noti_sts == "OFF" or allow_cutloss_sts == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                                ST = sale_coin_sim(coin, float(volumn), float(CutLossPrice))
                                time.sleep(3)
                        else:
                            fee = 0.0025
                            volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                            print("Real Volume Sell CutLoss" + str(float(volumn) - (float(volumn) * fee)))

                            if noti_sts == "ON" and allow_cutloss_sts != "YES":
                                NT = "Noti"

                            elif noti_sts == "OFF" or allow_cutloss_sts == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                                ST = sale_coin(bxin, coin, float(volumn), float(CutLossPrice))
                                time.sleep(3)
                                if is_number(ST) == True:
                                    INFO = sync_balance_coin(bxin, exchange,coin,str(chat_id))
                                    if INFO != "":  ## Return Error ##
                                        bot.sendMessage(chat_id, INFO)

                        if NT == "Noti" and allow_cutloss_sts == "NO" and "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('cts_cutloss')
                            profit = (((CutLossPrice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            NOTISTS_INFO += ("\n---------------\
                                            \nTake Action to CutLoss(CTS),Now!\
                                            \n|- CutLoss " + coin + " -| \
                                            \nOrder:/" + order_id + \
                                             "\nSale(VL):" + str(float(volumn)) + \
                                             "\nStart(Rate):" + str(float(rate)) + \
                                             "\nQty:" + str(float(qty)) + \
                                             "\nSold:" + str(format_floatc(float((CutLossPrice / rate) * qty), 2)) + \
                                             "\nFee:" + str(fee) + \
                                             "\nProfit:" + str(format_floatc(float(profit_fee), 2)) + " Bath\
                                             \nAccept this Action or not?\n----\
                                              \n"+emoji.emojize(':blue_circle:')+"/OK_" + order_id + "\
                                             \n"+emoji.emojize(':black_circle:')+"/UPDATE_" + order_id + "\
                                             \n"+emoji.emojize(':red_circle:')+"/CLOSE_" + order_id \
                                )
                            if Pause == "NO":
                                bot.sendMessage(chat_id, NOTISTS_INFO)
                                COUNT += 1
                                NOTISTS_INFO = ""
                                print("Sale Cut loss at " + str(CutLossPrice) + " !!!")
                                time.sleep(10)
                            else:
                                NOTISTS_INFO = ""

                        if is_number(ST) == True and allow_cutloss_sts == "YES" and order_id == ORDER:
                            noti_sts = "ON"
                            #allow_cutloss = "NO"
                            CK1 = Update_OrderSale(order_id, exchange, 'trading')
                            CK2 = Update_OrderSale_Rate(order_id, exchange,CutLossPrice)
                            if CK1 == "OK" and CK2 == "OK":
                                bot.sendMessage(chat_id, 'Update Action CutLoss trading Status => Completed')
                            else:
                                bot.sendMessage(chat_id, 'Update Action CutLoss trading Status => Completed')
                            allow_close_sts = "NO"
                            NOTISTS_INFO = ""

                        if is_number(ST) == True and allow_cutloss_sts == "YES" and order_id == ORDER:
                            profit = (((CutLossPrice / rate) * qty) - qty)
                            profit_fee = (profit - (profit * fee))
                            bot.sendMessage(chat_id,
                                            "!! Action CutLoss(CTS) Trading Completed \
                                             \nCoin:" + coin + \
                                            "\nOrder:/" + order_id + \
                                            "\nSale Volumn:" + str(float(volumn)) + \
                                            "\nRate Start:" + str(float(rate)) + \
                                            "\nQty:" + str(float(qty)) + \
                                            "\nSold:" + str(format_floatc(float((CutLossPrice / rate) * qty), 2)) + \
                                            "\nChange Fee:" + str(fee) + \
                                            "\nProfit:" + str(format_floatc(float(profit_fee), 2)) + " Bath",
                                            reply_markup=mainmenu)

                            Insert_Profit(order_id, time.strftime('%Y-%m-%d %H:%M:%S'), exchange, coin, volumn, qty,
                                          format_floatc(float((CutLossPrice / rate) * qty), 3), format_floatc(float(profit_fee), 2))
                            print("Sale Cut loss at " + str(CutLossPrice) + " !!!")
                            allow_cutloss_sts = "NO"
                            NOTIISTS_INFO = ""

                        elif ST != "" and is_number(ST) != True:
                             CK = Update_OrderSale(order_id, exchange, 'close')
                             if CK == "OK":
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                             else:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                             bot.sendMessage(chat_id,"Exchange Error =>"+str(ST))
                             continue

                    elif result[0] == "StopLoss":
                        LastPrice = result[1]
                        time.sleep(2)
                        if "UpdateAct" not in UPDATE_ACT:
                            NOTISTS_INFO += (
                                "(" + str(COUNT) + ")[= StopLoss(CTS) =]\
                                         \nOrder:/" + order_id + "\
                                         \nCoin:" + coin + "\
                                         \nPrice:" + str(float(LastPrice)))
                        if simtest == "yes":
                            fee = 0.0025
                            volumn = format_floatc(float(float(volumn) - (float(volumn) * fee)),4)
                            print("Real Volume Sell" + str(float(volumn) - (float(volumn) * fee)))
                            if noti_sts == "ON" and allow_stoploss_sts != "YES":
                                NT = "Noti"

                            elif noti_sts == "OFF" or allow_stoploss_sts == "YES" and order_id == ORDER:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                                ST = sale_coin_sim(coin, float(volumn), float(LastPrice))
                                time.sleep(3)
                        else:
                            fee = 0.0025
                            volumn = format_floatc((float(volumn) - (float(volumn) * fee)),4)
                            print("Real Volume Sell" + str(float(volumn) - (float(volumn) * fee)))
                            print("Sale Coin Stop Loss !! at " + str(LastPrice) + " " + coin)
                            #time.sleep(4)
                            if noti_sts == "ON" and allow_stoploss_sts != "YES":
                                NT = "Noti"
                                time.sleep(2)
                            elif noti_sts == "OFF" or allow_stoploss_sts == "YES" and order_id == ORDER:
                                # bot.sendMessage(chat_id,"")
                                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                                ST = sale_coin(bxin, coin, float(volumn), float(LastPrice))
                                time.sleep(3)
                                if is_number(ST) == True:
                                    INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                                    if INFO != "":  ## Return Error ##
                                        bot.sendMessage(chat_id, INFO)

                            # ST=False
                            print("Status Sale Order " + str(ST))
                        if NT == "Noti" and allow_stoploss_sts == "NO" and "UpdateAct" not in UPDATE_ACT and "CloseOrder" not in NOTISTATE_ACTION:
                            NOTISTATE_ACTION.clear()
                            NOTISTATE_ACTION.append('cts_stoploss')
                            profit = (((LastPrice / rate) * qty) - qty)
                            fee = 0.0025
                            profit_fee = (profit - (profit * fee))
                            NOTISTS_INFO += ("\n---------------------\
                                            \n"+emoji.emojize(':exclamation:')+"Please Take Action StopLoss(CTS) Noww !!\
                                            \n|--StopLoss " + coin + " --| \
                                            \nOrder:/" + order_id + \
                                             "\nSale Volumn:" + str(float(volumn)) + \
                                             "\nRate Start:" + str(float(rate)) + \
                                             "\nQty:" + str(float(qty)) + \
                                             "\nSold:" + str(format_floatc(float((LastPrice / rate) * qty), 2)) + \
                                             "\nChange Fee:" + str(fee) + \
                                             "\nProfit:" + str(format_floatc(profit_fee, 2)) + " Bath\
                                             \nAccept this Action or not?\n----\
                                              \n"+emoji.emojize(':blue_circle:')+"/OK_" + order_id + "\
                                             \n"+emoji.emojize(':black_circle:')+"/UPDATE_" + order_id + "\
                                             \n"+emoji.emojize(':red_circle:')+"/CLOSE_" + order_id \
                                )
                            if Pause == "NO":
                                bot.sendMessage(chat_id, NOTISTS_INFO)
                                NOTISTS_INFO = ""
                                COUNT += 1
                                print("Sale Stop loss at " + str(LastPrice) + " !!!")
                                print("Change fee:" + str(fee))
                                print('Profit:' + str(profit_fee))
                                time.sleep(10)
                            else:
                                NOTISTS_INFO=""
                        if is_number(ST) == True and allow_stoploss_sts == "YES" and order_id == ORDER:
                            noti_sts = "ON"
                            #allow_stoploss = "NO"
                            CK1 = Update_OrderSale(order_id, exchange, 'trading')
                            CK2 = Update_OrderSale_Rate(order_id, exchange,LastPrice)
                            if CK1 == "OK" and CK2 == "OK":
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading out => Completed")
                            else:
                                bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status Trading out => Completed")

                        if is_number(ST) == True and allow_stoploss_sts == "YES" and order_id == ORDER:
                            profit = (((LastPrice / rate) * qty) - qty)
                            fee = 0.0025
                            profit_fee =(profit - (profit * fee))
                            bot.sendMessage(chat_id,
                                            ""+emoji.emojize(':heavy_check_mark:')+"Action StopLoss(CTS) Trading Completed\
                                            \nCoin:" + coin + \
                                            "\nOrder:/" + order_id + \
                                            "\nSale Volumn:" + str(float(volumn)) + \
                                            "\nRate Start:" + str(float(rate)) + \
                                            "\nQty:" + str(float(qty)) + \
                                            "\nSold:" + str(format_floatc(float((LastPrice / rate) * qty), 2)) + \
                                            "\nChange Fee:" + str(fee) + \
                                            "\nProfit:" + str(format_floatc(float(profit_fee), 2)) + " Bath",
                                            reply_markup=mainmenu)

                            Insert_Profit(order_id, time.strftime('%Y-%m-%d %H:%M:%S'), exchange, coin, volumn, qty,
                                          format_floatc(float((LastPrice / rate) * qty), 3), format_floatc(profit_fee, 2))
                            print("Sale Stop loss at " + str(LastPrice) + " !!!")
                            print("Change fee:" + str(fee))
                            print('Profit:' + str(profit_fee))
                            #CK = Update_coinbalance(exchange, coin, chat_id)
                            #if CK != False:
                            #    bot.sendMessage(chat_id, CK)
                            allow_stoploss_sts = "NO"
                            NOTISTS_INFO = ""
                        elif ST != "" and is_number(ST) != True:
                            CK = Update_OrderSale(order_id, exchange, 'close')
                            if CK == "OK":
                               bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                            else:
                               bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Update Status close =>" + CK)
                            bot.sendMessage(chat_id,"Exchange Error =>"+str(ST))
                            continue
                else:
                    print("Not Found Result trailling  !!")
                    continue

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
                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                ST = sale_coin_sim(coin, float(vl), float(lastprice))
                time.sleep(3)
            else:
                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                ST = sale_coin(bxin, coin, float(vl), float(lastprice))
                time.sleep(3)
                if is_number(ST) == True:
                    INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                    if INFO != "":  ## Return Error ##
                        bot.sendMessage(chat_id, INFO)

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
                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                ST = sale_coin_sim(coin, float(vl), float(lastprice))
                time.sleep(3)
            else:
                bot.sendMessage(chat_id, ""+emoji.emojize(':hourglass:')+" Sell under Processing .. ")
                ST = sale_coin(bxin, coin, float(vl), float(lastprice))
                time.sleep(3)
                if is_number(ST) == True:
                    INFO = sync_balance_coin(bxin, exchange,coin, str(chat_id))
                    if INFO != "":  ## Return Error ##
                        bot.sendMessage(chat_id, INFO)

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
        #print("2.Check Strategy income" + str(STRATEGY))
        ST = Get_OpenOrder(exchange, 'open')
        if str(ST) == "()":
            return False
        print("[= Remaining Open Order  =]")
        for order in list(ST):
            Time = (order[2])
            order_id = (order[1])
            coin = (order[3])
            Type = (order[4])
            rate = (order[5])
            volumn = (order[6])
            qty = (order[7])
            strategy = (order[10])
            print("" + Time + "\nO:/" + order_id + "\nC:" + coin + "\nR:" + str(rate) + "\nQ:" + str(
                qty) + "\nVolumn:" + str(volumn) + "\nType " + Type)
            print("---------------------")
            if Type == "buy" and strategy != 'bls' and strategy != 'cts':
                if simtest == "yes":
                    ST = ck_close_order_sim(order_id, coin, 'buy', exchange)
                else:
                    ST = ck_close_order(bxin, order_id, coin, 'buy', exchange)
            elif Type == "sell" and strategy != 'bls' and strategy != 'cts':
                if simtest == "yes":
                    ST = ck_close_order_sim(order_id, coin, 'sell', exchange)
                else:
                    ST = ck_close_order(bxin, order_id, coin, 'sell', exchange)
            elif strategy == 'bls' or strategy == 'cts':
                ST = Update_OpenOrder(order_id, exchange, 'close')
                if ST == "OK":
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to closed ..")
                    ST=(True, "close")
                else:
                    print("Update Open Order " + order_id + " Type \"" + Type + "\" to failed")
                    ST=(False, "close")

            if ST[0] == True and ST[1] == "close" and Type == "buy" and strategy == "bts":  ## Dev112
                #ST = Insert_ckloss(order_id, 'bxinth', BuyStopLoss, BuyCutLoss, 0) ## TOR_DEV
                StopLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Stoploss')
                StopLoss=(list(StopLoss.split(',')))
                if len(StopLoss) > 1:
                    BuyStopLoss = ""
                    for P in StopLoss:
                        BuyStopLoss+=("\n>"+P+"")
                else:
                    BuyStopLoss=StopLoss[0]
                CutLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Cutloss')
                BuyCutLoss=CutLoss
                ST="OK"
                if ST == "OK":
                    print("Debug123 ==>"+coin+""+str(qty)+""+str(rate))
                    ST = Insert_OrderBuy(order_id, exchange, time.strftime('%Y-%m-%d %H:%M:%S'), coin, qty, rate, 'buy')
                    print("DEBUG Status Insert OrderBuy " + ST)
                    if ST == "OK":
                        NT == "Noti"
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Order buy have been closed !!")
                        print("StopLoss Count>"+str(len(StopLoss)))
                        if len(StopLoss) > 1:
                            bot.sendMessage(chat_id,
                                        ""+emoji.emojize(':heavy_check_mark:')+"Mode Custom,Apply BTS \
                                        \nOrder ID:/" + str(order_id) + "\
                                        \nCutLoss:" + str(BuyCutLoss) + " % \
                                        \nStopLoss:" + str(BuyStopLoss) + "\
                                        \nApply --> Completed ", reply_markup=mainmenu)
                            STRATEGY.clear()
                            CKLOSS.clear()
                        else:
                            bot.sendMessage(chat_id,
                                            "" + emoji.emojize(':heavy_check_mark:') + "Mode Auto,Apply BTS \
                                \nOrder ID:/" + str(order_id) + "\
                                \nCutLoss:" + str(BuyCutLoss) + " % \
                                \nStopLoss:" + str(BuyStopLoss) + "% \
                                \nApply --> Completed ", reply_markup=mainmenu)
                        ## Sync Balance with Exchange ##
                        STRATEGY.clear()
                        CKLOSS.clear()
                    else:
                        bot.sendMessage(chat_id,
                                        "!! Apply Strategy Trailing Stop to Order Buy " + order_id + "--> Failed !! ")
                        STRATEGY.clear()
                        CKLOSS.clear()
                else:
                    STRATEGY.clear()

            elif ST[0] == True and ST[1] == "trading" and Type == "buy" and strategy == "bts":   ## Dev112
                 fee=0.0025
                 volumn=volumn-(volumn*fee)
                 INFO = check_coin_list(bxin, coin, str(format_floatc(rate,4)), str(format_floatc(volumn,4)), 'buy')
                 if INFO[0] == True:
                     bot.sendMessage(chat_id, "[= Wait Order Trading =]\
                        \nCoin:" + coin + "\
                        \nRank|Rate|volumn\
                        \n" + INFO[1])

            elif ST[0] == True and ST[1] == "close" and Type == "buy" and strategy == "bls":   ## Dev112
                # CKCLOSE.append('ckclose_buy_apply')
                #print("DEBUG Insert StopRisk =>" + str(BuyStopRisk) + "StopBuy =>" + str(BuyStopBuy))
                StopBuy = Get_BittrexDB(order_id, 'bxinth', 'ckstopbuy', 'StopBuy')
                StopBuy = (list(StopBuy.split(',')))

                if len(StopBuy) > 1:
                    BuyStopBuy = ""
                    for P in StopBuy:
                        BuyStopBuy += ("\n>" + P + "")
                else:
                    BuyStopBuy = StopBuy[0]
                BuyStopRisk = Get_BittrexDB(order_id, 'bxinth', 'ckstopbuy', 'StopRisk')
                print("StopBuy is" + str(StopBuy)+" StopRisk is"+str(BuyStopRisk))
               # BuyStopRisk = CutLoss
                ST="OK"
                if ST == "OK":
                    ST = Insert_OrderStopBuy(order_id, exchange, time.strftime('%Y-%m-%d %H:%M:%S'),coin,qty,rate,
                                             'buy')
                    print("DEBUG Status Insert OrderStopBuy " + ST)
                    if ST == "OK":
                        bot.sendMessage(chat_id,
                                        "" + emoji.emojize(':heavy_check_mark:') + "Order buy have been closed !!")
                        NT == "Noti"
                        if len(StopBuy) > 1:
                            bot.sendMessage(chat_id,
                                        ""+emoji.emojize(':heavy_check_mark:')+"Auto Apply BLS !! \
                                        \nOrder ID:" + str(order_id) + "\
                                        \nStopBuy:" + str(BuyStopBuy) + " % \
                                        \nStopRisk:" + str(BuyStopRisk) + "% \
                                        \nApply --> Completed ", reply_markup=mainmenu)
                            STRATEGY.clear()
                            CKLOSS.clear()
                        else:
                            bot.sendMessage(chat_id,
                                            "" + emoji.emojize(':heavy_check_mark:') + "Auto Apply BLS !! \
                                            \nOrder ID:" + str(order_id) + "\
                                            \nStopBuy:" + str(BuyStopBuy) + " % \
                                            \nStopRisk:" + str(BuyStopRisk) + "% \
                                            \nApply --> Completed ", reply_markup=mainmenu)
                            STRATEGY.clear()
                            CKLOSS.clear()

                    else:
                        bot.sendMessage(chat_id,
                                        "!! Apply Strategy BLS  to Order Buy " + order_id + "--> Failed !! ")
                        STRATEGY.clear()
                else:
                    STRATEGY.clear()
            elif ST[0] == True and ST[1] == "trading" and Type == "sell":  ## Dev112
                #fee = 0.0025
                #volumn = volumn - (volumn * fee)
                print("Action check sell wait order trading !!!")
                INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'sell')
                print(str(INFO))
                if INFO[0] == True:
                    bot.sendMessage(chat_id, "[= Wait Order Trading =]\
                        \nCoin:" + coin + "\
                        \nRank|Rate|volumn\
                        \n" + INFO[1])

            elif ST[0] == True  and ST[1] == "close" and Type == "sell" and strategy == "cts":
                print("DEBUG Insert Ckloss StopLoss " + str(SellStopLoss) + " CutLoss " + str(SellCutLoss))
                #ST = Insert_ckloss(order_id, exchange, SellStopLoss, SellCutLoss, 0)
                StopLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Stoploss')
                StopLoss = (list(StopLoss.split(',')))
                if len(StopLoss) > 1:
                    BuyStopLoss = ""
                    for P in StopLoss:
                        BuyStopLoss += ("\n>" + P + "")
                else:
                    BuyStopLoss = StopLoss[0]
                CutLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Cutloss')
                BuyCutLoss = CutLoss
                ST="OK"
                #########
                if ST == "OK":
                    ST = Insert_OrderSale(order_id, exchange, time.strftime('%Y-%m-%d %H:%M:%S'), coin, qty, rate,
                                          'sell')
                    print("DEBUG Status Insert OrderSell " + ST)
                    if ST == "OK":
                        NT == "Noti"
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Order Sell have been closed !!")
                        if len(StopLoss) > 1:
                            bot.sendMessage(chat_id,
                                            "" + emoji.emojize(':heavy_check_mark:') + "Mode Custom,Apply CTS \
                                        \nOrder ID:/" + str(order_id) + "\
                                        \nCutLoss:" + str(BuyCutLoss) + " % \
                                        \nStopLoss:" + str(BuyStopLoss) + "\
                                        \nApply --> Completed ", reply_markup=mainmenu)
                            STRATEGY.clear()
                            CKLOSS.clear()
                        else:
                            bot.sendMessage(chat_id,
                                            "" + emoji.emojize(':heavy_check_mark:') + "Mode Auto,Apply CTS \
                                \nOrder ID:/" + str(order_id) + "\
                                \nCutLoss:" + str(BuyCutLoss) + " % \
                                \nStopLoss:" + str(BuyStopLoss) + "% \
                                \nApply --> Completed ", reply_markup=mainmenu)

                        STRATEGY.clear()
                        CKLOSS.clear()
                    else:
                        bot.sendMessage(chat_id,
                                        "!! Apply Strategy Trailing Stop to Order Sell " + order_id + "--> Failed !! ")

                        STRATEGY.clear()

            else:
                STRATEGY.clear()

    def check_close_openorder_trading(self,exchange, chat_id):
        #print("2.Check Strategy income" + str(STRATEGY))
        ST = Get_OpenOrder(exchange, 'trading')
        if str(ST) == "()":
            return False
        print("[= Remaining Open Order trading  =]")
        for order in list(ST):
            Time = (order[2])
            order_id = (order[1])
            coin = (order[3])
            Type = (order[4])
            rate = (order[5])
            volumn = (order[6])
            exchange=(order[9])
            strategy=(order[10])
            qty = (order[7])
            print("" + Time + "\nO:/" + order_id + "\nC:" + coin + "\nR:" + str(rate) + "\nQ:" + str(
                qty) + "\nVolumn:" + str(volumn) + "\nType " + Type)
            print("---------------------")
            if Type == "buy":
                if simtest != "yes":
                    ST = ck_close_order(bxin, order_id, coin, 'buy', exchange)
                    if ST == None:
                       continue
                else:
                    ST = ck_close_order_sim(order_id, coin, 'buy', exchange)
                    if ST == None:
                        continue
            elif Type == "sell":
                if simtest != "yes":
                    ST = ck_close_order(bxin, order_id, coin, 'sell', exchange)
                    if ST == None:
                       continue
                else:
                    ST = ck_close_order_sim(order_id, coin, 'sell', exchange)
                    if ST == None:
                        continue
            if ST[0] == True and ST[1] == "close" and Type == "buy" and strategy == "bts":  ## Dev112
                StopLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Stoploss')
                StopLoss = (list(StopLoss.split(',')))
                if len(StopLoss) > 1:
                    BuyStopLoss = ""
                    for P in StopLoss:
                        BuyStopLoss += ("\n>" + P + "")
                else:
                    BuyStopLoss = StopLoss[0]
                CutLoss = Get_BittrexDB(order_id, 'bxinth', 'ckloss', 'Cutloss')
                BuyCutLoss = CutLoss
                ST = "OK"
                if ST == "OK":
                    ST = Insert_OrderBuy(order_id, exchange, time.strftime('%Y-%m-%d %H:%M:%S'), coin, qty, rate, 'buy')
                    print("DEBUG Status Insert OrderBuy " + ST)
                    if ST == "OK":
                        NT == "Noti"
                        bot.sendMessage(chat_id,
                                        "" + emoji.emojize(':heavy_check_mark:') + "Order buy have been closed !!")
                        print("StopLoss Count>" + str(len(StopLoss)))
                        if len(StopLoss) > 1:
                            bot.sendMessage(chat_id,
                                            "" + emoji.emojize(':heavy_check_mark:') + "Mode Custom,Apply BTS \
                                            \nOrder ID:/" + str(order_id) + "\
                                            \nCutLoss:" + str(BuyCutLoss) + " % \
                                            \nStopLoss:" + str(BuyStopLoss) + "\
                                            \nApply --> Completed ", reply_markup=mainmenu)
                            STRATEGY.clear()
                            CKLOSS.clear()
                        else:
                            bot.sendMessage(chat_id,
                                            "" + emoji.emojize(':heavy_check_mark:') + "Mode Auto,Apply BTS \
                                    \nOrder ID:/" + str(order_id) + "\
                                    \nCutLoss:" + str(BuyCutLoss) + " % \
                                    \nStopLoss:" + str(BuyStopLoss) + "% \
                                    \nApply --> Completed ", reply_markup=mainmenu)
                        ## Sync Balance with Exchange ##
                        STRATEGY.clear()
                        CKLOSS.clear()

                    else:
                        bot.sendMessage(chat_id,
                                        "!! Apply Strategy Trailing Stop to Order Buy " + order_id + "--> Failed !! ")
                        STRATEGY.clear()
                else:
                    STRATEGY.clear()

            elif ST[0] == True and ST[1] == "trading" and Type == "buy" and strategy == "bts" and str(order_id) not in CKORDERWAIT:  ## Dev112
                count = 0
                INFO_WAIT = ""
                INFO_RES = ""
                fee = 0.0025
                # volumn = (qty / rate)
                #volumn = volumn - (volumn * fee)
                if simtest != "yes":
                    INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)),'buy')
                else:
                    INFO = check_coin_list_sim(coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'buy','bxinth')
                print("Check Infomation> "+str(INFO))
                if INFO[0] == True:
                    count += 1
                    INFO_WAIT += ("\n---------\
                           \n" + str(count) + "Order:/" + str(order_id) + "\
                           \nCoin:" + coin + "|bts\
                           \n" + INFO[1])

                if INFO_WAIT != "":
                    INFO_RES += "[ Wait OrderBuy Trading(BTS)]\n"
                    INFO_RES += "[Bids]"
                    INFO_RES += INFO_WAIT
                    bot.sendMessage(chat_id, INFO_RES)
                    CKORDERWAIT.append(order_id)
                    INFO_WAIT = ""

            #elif ST[0] == True and ST[1] == "close" and Type == "buy" and strategy == "bls":  ## Dev112
            #    # CKCLOSE.append('ckclose_buy_apply')
            #    print("DEBUG Insert StopRisk =>" + str(BuyStopRisk) + "StopBuy =>" + str(BuyStopBuy))
            #    # bot.sendMessage(chat_id,"Apply BST Strategy or not?\n /Apply\n/No")
            #    ST = Insert_ckstopbuy(order_id, 'bxinth', BuyStopRisk, BuyStopBuy, 0)
            #    if ST == "OK":
            #        ST = Insert_OrderStopBuy(order_id, exchange, time.strftime('%Y-%m-%d %H:%M:%S'), coin, qty, rate,
            #                                 'buy')
            #        print("DEBUG Status Insert OrderStopBuy " + ST)
            #        if ST == "OK":
            #            NT == "Noti"
            #            bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Order buy have been closed !!")
            #            bot.sendMessage(chat_id,
            #                           ""+emoji.emojize(':heavy_check_mark:')+"Auto Apply BLS !! \
            #                            \nOrder ID:" + str(order_id) + "\
            #                            \nStopBuy:" + str(BuyStopBuy) + " % \
            #                            \nStopRisk:" + str(BuyStopRisk) + "% \
            #                            \nApply --> Completed ", reply_markup=mainmenu)
            #            STRATEGY.clear()

            #        else:
            #            bot.sendMessage(chat_id,
            #                            "!! Apply Strategy BLS  to Order Buy " + order_id + "--> Failed !! ")
            #            STRATEGY.clear()
            #    else:
            #        STRATEGY.clear()

            elif ST[0] == True  and ST[1] == "close" and Type == "sell" and strategy == "cts":
                print("DEBUG Insert Ckloss StopLoss " + str(SellStopLoss) + " CutLoss " + str(SellCutLoss))
                ST = Insert_ckloss(order_id, exchange, SellStopLoss, SellCutLoss, 0)
                if ST == "OK":
                    ST = Insert_OrderSale(order_id, exchange, time.strftime('%Y-%m-%d %H:%M:%S'), coin, qty, rate,
                                          'sell')
                    print("DEBUG Status Insert OrderSell " + ST)
                    if ST == "OK":
                        NT == "Noti"
                        bot.sendMessage(chat_id, ""+emoji.emojize(':heavy_check_mark:')+"Order Sell have been closed !!")
                        bot.sendMessage(chat_id,
                                        ""+emoji.emojize(':heavy_check_mark:')+"Auto Apply CTS \
                                             \nOrder ID:/" + str(order_id) + "\
                                             \nCutLoss:" + str(SellCutLoss) + " % \
                                             \nStopLoss:" + str(SellStopLoss) + "% \
                                             \nApply --> Completed ", reply_markup=mainmenu)

                        STRATEGY.clear()
                    else:
                        bot.sendMessage(chat_id,
                                        "!! Apply Strategy Trailing Stop to Order Sell " + order_id + "--> Failed !! ")
                        STRATEGY.clear()

                else:
                    STRATEGY.clear()

            elif ST[0] == True and ST[1] == "trading" and Type == "sell" and strategy == "cts" and str(order_id) not in CKORDERWAIT:  ## Dev112
                count = 0
                INFO_WAIT = ""
                INFO_RES = ""
                fee = 0.0025
                # volumn = (qty / rate)
                # volumn = volumn - (volumn * fee)
                if simtest != "yes":
                    INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)),
                                           'buy')
                else:
                    INFO = check_coin_list_sim(coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'buy',
                                               'bxinth')
                print("Check Infomation> " + str(INFO))
                if INFO[0] == True:
                    count += 1
                    INFO_WAIT += ("\n---------\
                           \n" + str(count) + "Order:/" + str(order_id) + "\
                           \nCoin:" + coin + "|bts\
                           \n" + INFO[1])

                if INFO_WAIT != "":
                    INFO_RES += "[ Wait OrderBuy Trading(BTS)]\n"
                    INFO_RES += "[Bids]"
                    INFO_RES += INFO_WAIT
                    bot.sendMessage(chat_id, INFO_RES)
                    CKORDERWAIT.append(order_id)
                    INFO_WAIT = ""


    def check_close_strategy_trading(self,exchange, chat_id): ###Dev112
        #exchange fee
        ### ORDER BTS ###
        fee=0.0025
        ST = Get_OrderBuy(exchange, 'trading')
        if str(ST) == "()":
            return False
        print("[= Remaining Order Sell(BTS) trading  =]")
        for order in list(ST):
            order_id = (order[0])
            Time = (order[1])
            coin = (order[2])
            qty = (order[3])
            rate = (order[4])
            status=(order[5])
            exchange=(order[6])
            volumn=(qty/rate)
            print("" + Time + "\nO:/" + order_id + "\nC:" + coin + "\nR:" + str(rate) + "\nQ:" + str(
                qty) + "\nVolumn:" + str(volumn) + "\nStatus:"+status )
            ## Check coin last pricce
            if simtest != "yes":
                lastprice = get_lastprice(bxin,str(coin))
                last_rate = get_coin_lastorder(bxin, coin, 'buy')
            else:
                last_rate=(rate,True)
                lastprice=get_lastprice_sim(str(coin),exchange)

            if is_number(lastprice) != True:
                print("!!! Can't get lastprice ")
                return False
            print("---------------------")

            if float(lastprice) >= float(rate) and float(rate) <= float(last_rate[0]):
                profit = (((lastprice / rate) * qty) - qty)
                profit_fee = (profit - (profit * fee))
                bot.sendMessage(chat_id, "!!Sell Coin(BTS) Direct Completed !!\
                     \nCoin:" + coin + "\
                     \nOrder:" + str(order_id) + "\
                     \nBuy:" + str(qty) + "\
                     \nSold:" + str(format_float(((lastprice / rate) * qty))) + "\
                     \nChange Fee " + str(fee) + "\
                     \nProfit " + str(format_float(profit_fee)) + "Bath", reply_markup=mainmenu)

                CK1 = Update_OrderBuy(order_id, exchange, 'sold')
                CK2 = Update_OrderBuy_Rate(order_id, exchange, lastprice)
                if CK1 == "OK" and CK2 == "OK":
                    bot.sendMessage(chat_id,
                                    "" + emoji.emojize(':heavy_check_mark:') + "Update Status Sold Out => Completed")
                else:
                    bot.sendMessage(chat_id,
                                    "" + emoji.emojize(':heavy_check_mark:') + "Update Status Sold Out => Completed")
                    ## Real Sale ###
            else:
                count=0
                INFO_WAIT=""
                INFO_RES=""
                fee = 0.0025
                #volumn = (qty / rate)
                #volumn = volumn - (volumn * fee)
                if simtest != "yes":
                    INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'buy')
                else:
                    INFO = check_coin_list_sim(coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)),'buy','bxinth')
                print("Information >"+str(INFO))
                if INFO[0] == True:
                    count += 1
                    INFO_WAIT += ("---------\
                       \n" + str(count) + "Order:/" + str(order_id) + "\
                       \nCoin:" + coin + "|bts\
                       \n" + INFO[1])

                if INFO_WAIT != "":
                    INFO_RES += "[ Wait OrderSell Trading(BTS)]\n"
                    INFO_RES += "[Asks]"
                    INFO_RES += INFO_WAIT
                    bot.sendMessage(chat_id, INFO_RES)
                    INFO_WAIT = ""

        ### ORDER CTS ####
        ST = Get_OrderSale(exchange,'trading')
        if str(ST) == "()":
            return False
        print("[= Remaining Order Sell(CTS) trading  =]")
        for order in list(ST):
            order_id = (order[0])
            Time = (order[1])
            coin = (order[2])
            qty = (order[3])
            rate = (order[4])
            status = (order[5])
            exchange = (order[6])
            volumn = (qty / rate)
            print("" + Time + "\nO:/" + order_id + "\nC:" + coin + "\nR:" + str(rate) + "\nQ:" + str(
                qty) + "\nVolumn:" + str(volumn) + "\nStatus " + status)
            ## Check coin last pricce
            lastprice = get_lastprice(bxin,str(coin))
            if is_number(lastprice) != True:
                print("!!! Can't get lastprice ")
                return False
            print("---------------------")
            if simtest != "yes":
                last_rate = get_coin_lastorder(bxin, coin, 'buy')
            else:
                last_rate=(rate,True)
            if float(lastprice) >= float(rate) and float(rate) <= float(last_rate[0]):
                profit = (((lastprice / rate) * qty) - qty)
                profit_fee = (profit - (profit * fee))
                bot.sendMessage(chat_id, "!!Sell Coin(CTS) Direct Completed !!\
                         \nCoin:" + coin + "\
                         \nOrder:" + str(order_id) + "\
                         \nBuy:" + str(qty) + "\
                         \nSold:" + str(format_float(((lastprice / rate) * qty))) + "\
                         \nChange Fee " + str(fee) + "\
                         \nProfit " + str(format_float(profit_fee)) + " Bath", reply_markup=mainmenu)

                CK1 = Update_OrderSale(order_id, exchange, 'sold')
                CK2 = Update_OrderSale_Rate(order_id, exchange, lastprice)
                if CK1 == "OK" and CK2 == "OK":
                    bot.sendMessage(chat_id,
                                    "" + emoji.emojize(':heavy_check_mark:') + "Update Status Sold Out => Completed")
                else:
                    bot.sendMessage(chat_id,
                                    "" + emoji.emojize(':heavy_check_mark:') + "Update Status Sold Out => Completed")
            else:
                count = 0
                INFO_WAIT =""
                INFO_RES =""
                fee = 0.0025
                #volumn = (qty / rate)
                #volumn = volumn - (volumn * fee)
                if simtest != "yes":
                    INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'sell')
                else:
                    INFO = check_coin_list_sim(coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)),'sell','bxinth')
               # print("Information Sale =>"+str(INFO))
                if INFO[0] == True:
                    count += 1
                    INFO_WAIT += ("---------\
                           \n" + str(count) + "Order:/" + str(order_id) + "\
                           \nCoin:" + coin + "|cts\
                           \n" + INFO[1])

                if INFO_WAIT != "":
                    INFO_RES += "[ Wait OrderSell Trading(CTS)]\n"
                    INFO_RES += "[Asks]"
                    INFO_RES += INFO_WAIT
                    bot.sendMessage(chat_id, INFO_RES)
                    INFO_WAIT = ""

        ### ORDER BLS ###
        ST = Get_OrderStopBuy(exchange, 'trading')
        if str(ST) == "()":
            return False
        print("[= Remaining Order(BLS) trading  =]")
        for order in list(ST):
            order_id = (order[0])
            Time = (order[1])
            coin = (order[2])
            qty = (order[3])
            rate = (order[4])
            status = (order[5])
            exchange = (order[6])
            volumn = (qty / rate)
            print("" + Time + "\nO:/" + order_id + "\nC:" + coin + "\nR:" + str(rate) + "\nQ:" + str(
                qty) + "\nVolumn:" + str(volumn) + "\nStatus " + status)
            ## Check coin last pricce
            lastprice = get_lastprice(bxin,str(coin))
            if is_number(lastprice) != True:
                print("!!! Can't get lastprice ")
                return False
            print("---------------------")
            if simtest == "yes":
                last_rate = get_coin_lastorder(bxin, coin, 'sell')
            else:
                last_rate = (rate,True)
            if float(lastprice) >= float(rate) and float(rate) <= float(last_rate[0]):
                profit = (((lastprice / rate) * qty) - qty)
                profit_fee = (profit - (profit * fee))
                bot.sendMessage(chat_id, "!!Buy Coin Direct Completed !!\
                         \nCoin:" + coin + "\
                         \nOrder:" + str(order_id) + "\
                         \nBuy:" + str(qty) + "\
                         \nSold:" + str(format_float(((lastprice / rate) * qty))) + "\
                         \nChange Fee " + str(fee) + "\
                         \nProfit " + str(format_float(profit_fee)) + "Bath", reply_markup=mainmenu)
                CK1 = Update_OrderStopBuy(order_id, exchange, 'bought')
                CK2 = Update_OrderStopBuy(order_id, exchange, lastprice)
                if CK1 == "OK" and CK2 == "OK":
                    bot.sendMessage(chat_id,
                                    "" + emoji.emojize(':heavy_check_mark:') + "Update Status Bought In => Completed")
                else:
                    bot.sendMessage(chat_id,
                                    "" + emoji.emojize(':heavy_check_mark:') + "Update Status Bought In => Completed")
            else:
                count = 0
                INFO_WAIT = ""
                INFO_RES = ""
                fee = 0.0025
                volumn = (qty / rate)
                volumn = volumn - (volumn * fee)
                INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'buy')


                if INFO[0] == True:
                    count += 1
                    INFO_WAIT += ("---------\
                           \n" + str(count) + "Order:/" + str(order_id) + "\
                           \nCoin:" + coin + "|bls\
                           \n" + INFO[1])

                if INFO_WAIT != "":
                    INFO_RES += "[ Wait OrderBuy Trading BLS]\n"
                    INFO_RES += "[Bids]"
                    INFO_RES += INFO_WAIT
                    bot.sendMessage(chat_id, INFO_RES)
                    INFO_WAIT = ""


    def check_trading_wait(self,exchange, chat_id):
        #print("2.Check Strategy income" + str(STRATEGY))
        INFO=""
        INFO_WAIT = ""
        INFO_RES=""
        CK1=""
        CK2=""
        CK3=""
        CK4=""
        ST = Get_OpenOrder(exchange, 'trading')
        if str(ST) == "()":
           CK1=False
        count=0
        for order in list(ST):
            Time = (order[2])
            order_id = (order[1])
            coin = (order[3])
            Type = (order[4])
            rate = (order[5])
            volumn = (order[6])
            exchange=(order[9])
            strategy=(order[10])
            qty = (order[7])
            ####### Open order trading wait ###
            if strategy == "bts":
                fee = 0.0025
                if simtest != "yes":
                    volumn = volumn - (volumn * fee)
                    INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'buy')
                else:
                    INFO = check_coin_list_sim(coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)),'buy','bxinth')
            elif strategy == "cts" or strategy == "normal":
                if simtest != "yes":
                    volumn = volumn - (volumn * fee)
                    INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'sell')
                else:
                    INFO = check_coin_list_sim(coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'sell','bxinth')
            print("Infomation Check wait > "+str(INFO))
            if INFO[0] == True:
               count+=1
               INFO_WAIT+=("---------\
               \n["+str(count)+"]|Order:[/"+str(order_id)+"]\
               \nCoin:["+coin+"]|["+str(strategy).upper()+"]\
               \n"+INFO[1])
            elif INFO[0] == False:
                continue
            else:
                continue
        if INFO_WAIT != "" and INFO_RES == "":
            INFO_RES += "[ Open Order Trading ]\n"
            if strategy == "bts":
                INFO_RES+="[Bids]\n"
            else:
                INFO_RES += "[Asks]\n"
            INFO_RES += INFO_WAIT
            INFO_WAIT = ""
            bot.sendMessage(chat_id, INFO_RES)

################################
        ### Order buy wait trading ##
        count=0
        ST=Get_OrderStopBuy(exchange,'trading')
        if str(ST) == "()":
           CK2=False
        for order in list(ST):
            Time = (order[1])
            order_id = (order[0])
            coin = (order[2])
            rate = (order[4])
            qty = (order[3])
            fee = 0.0025
            volumn = (qty / rate)
            volumn = volumn - (volumn * fee)
            INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'buy')
            if INFO[0] == True:
                count += 1
                INFO_WAIT += ("---------\
               \n" + str(count) + "Order:/" + str(order_id) + "\
               \nCoin:" + coin + "|bls\
               \n" + INFO[1])
            elif INFO[0] == False:
                continue
            else:
                continue

        if INFO_WAIT != "" and INFO_RES != "" and simtest != "yes":
            INFO_RES += "[ OrderBuy Trading BLS ]\n"
            INFO_RES += "[Bids]"
            INFO_RES += INFO_WAIT
            bot.sendMessage(chat_id, INFO_RES)
            INFO_WAIT=""
###################################
        count=0
        ST=Get_OrderBuy(exchange,'trading')
        if str(ST) == "()":
            CK3=False
        for order in list(ST):
            Time = (order[1])
            order_id = (order[0])
            coin = (order[2])
            rate = (order[4])
            qty = (order[3])

            fee = 0.0025
            volumn=(qty/rate)
            volumn = volumn - (volumn * fee)
            INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'sell')
            print(INFO)
            if INFO[0] == True:
               count+=1
               INFO_WAIT+=("---------\
               \n("+str(count)+")Order:/"+str(order_id)+"\
               \nCoin:"+coin+"|bts\
               \n"+INFO[1])
            elif INFO[0] == False:
                continue
            else:
                continue

        if INFO_WAIT != "" and INFO_RES != "" and simtest != "yes":
            INFO_RES+="[ OrderSell Trading BTS ]\n"
            INFO_RES+="[Asks]"
            INFO_RES+=INFO_WAIT
            INFO_WAIT=""
            bot.sendMessage(chat_id, INFO_RES)

 ####################################
        count=0
        ST=Get_OrderSale(exchange,'trading')
        if str(ST) == "()":
            CK4=False
        for order in list(ST):
            Time = (order[1])
            order_id = (order[0])
            coin = (order[2])
            rate = (order[4])
            qty = (order[3])

            fee = 0.0025
            volumn=(qty/rate)
            volumn = volumn - (volumn * fee)
            INFO = check_coin_list(bxin, coin, str(format_floatc(rate, 4)), str(format_floatc(volumn, 4)), 'sell')
            if INFO[0] == True:
               count+=1
               INFO_WAIT+=("---------\
               \n("+str(count)+")Order:/"+str(order_id)+"\
               \nCoin:"+coin+"|cts\
               \n"+INFO[1]+"\n")
            elif INFO[0] == False:
                continue
            else:
                continue

        if INFO_WAIT != "" and INFO_RES != "" and simtest != "yes":
            INFO_RES += "[ OrderSell Trading CTS ]\n"
            INFO_RES += "[Asks]"
            INFO_RES += INFO_WAIT
            bot.sendMessage(chat_id, INFO_RES)

        print("InfoWait=>"+INFO_WAIT)
        if INFO_WAIT == "" and INFO_RES == "":
           bot.sendMessage(chat_id,"No order Wait !!")



TOKEN = telegrambot
bot = YourBot(TOKEN)
bot.message_loop()


#############MAIN PROGRAM ###########
while True:
    if STRATEGY_CHECK == "ON":
        simtest = "yes"
        for adminid in adminchatid:
            print("ChatID:"+str(adminid))
            bot.bls('bxinth', adminid)
            ####################
            bot.bts('bxinth', adminid)
            ####################
            bot.cts('bxinth', adminid)
            ####################
            bot.check_close_order('bxinth', adminid)
            ###################
            bot.check_close_openorder_trading('bxinth', adminid)
            ###################
            bot.check_close_strategy_trading('bxinth',adminid)
    time.sleep(10)
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



