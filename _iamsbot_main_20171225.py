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
Alarm = "ON"
Email = ""
Text_mail = ""
COUNT = 0

##########BOT COIN#############
BX = []
BITTREX = []
YOBIT = []

CKLOSS=[]
CKCOMMAND=[]
BXCOIN=['BTC/THB','LTC/THB','DASH/THB','BCH/THB','OMG/THB','XRP/THB','REP/THB','GNO/THB','ETH/THB','XZC/THB']
################### make up keybord stop ######
stopmarkup = {'keyboard': [['Stop Interactive']]}  ## for build Stop command to telagram
cancelmarkup = {'keyboard': [['Cancel ']]}  ## for build cancle command to telagram
backmarkup = {'keyboard': [['Back']]}  ## for build cancle command to telagram
hide_keyboard = {'hide_keyboard': True}
###############################################
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

    def on_chat_message(self, msg):
        global Alarm
        global COUNT
        global COMMAND_ADD
        global COMMAND_ALIAS
        global SERVER_ADD
        global HOST
        global roomtempthreshold
        global roomflag
        global Buy
        global Rate
        global CoinBuy
        global CutLoss
        global StopLoss
        global Uid
        content_type, chat_type, chat_id = telepot.glance(msg)
        content_type, chat_type, chat_id_test = telepot.glance(msg)
        print("Your chat_id_test:" + str(chat_id_test))

        # Do your stuff according to `content_type` ...
        print("Your chat_id:" + str(chat_id))  # this is chat_id
        print("Your admin_id:" + str(adminchatid))  # this is adminchatid
        print("Message Text:" + str(msg['text']))  ## message recived
        ### Connect to BX
        bxin = ccxt.bxinth({
            'apiKey': '8cdf0f0a666c',
            'secret': 'b6b22e1e51eb',
            "enableRateLimit": True,
        })
        if chat_id in adminchatid:  # Store adminchatid variable in tokens.py
            print("Welcome Administrator:")
            if content_type == 'text':
                if msg['text'] == "/setroomtemp" and chat_id not in settingroomtemp:
                    bot.sendChatAction(chat_id, 'typing')
                    settingroomtemp.append(chat_id)
                    bot.sendMessage(chat_id, "\U0001F4B2 Send me a new room temperature threshold to monitor?")
                elif chat_id in settingroomtemp:
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
                elif msg['text'] == '/alarmoff':
                    bot.sendChatAction(chat_id, 'typing')
                    Alarm = "OFF"
                    if Alarm == "OFF":
                        bot.sendMessage(chat_id, "\U0001F534 Disable All IAMS Alarm !")
                elif msg['text'] == '/alarmon':
                    bot.sendChatAction(chat_id, 'typing')
                    Alarm = "ON"
                    if Alarm == "ON":
                        bot.sendMessage(chat_id, "\U0001F535 Enable All IAMS Alarm !")
                elif msg['text'] == '/help':
                    bot.sendMessage(chat_id, " \U0001F4DA TBOT COMMAND LIST\U0001F4DA \
                     \n\U0001F4C9 /buyCoin -->Buy coin from your Exchange \
                     \n\U0001F4C9 /ckCoinInfo -->Check coin information from your Exchange \
                     \n\U0001F4C9 /asicDash -->Monitor IAMS utilization and Alarm messages \
                     \n\U0001F4C8 /ckwan --> For check IP Wan of IAMS \
                     \n\U0001F6A8 /ckroomtemp --> For check Server Room temperature \
                     \n\U0001F525 /setroomtemp --> For Setting Room temperature threshold \
                     \n\U0001F534 /alarmoff --> For close IAMS Alarm \
                     \n\U0001F535 /alarmon --> For Open Alarm IAMS \
                     \n\U0001F6AB /cancel --> For Cancel your all operation")
                elif msg['text'] == '/buyCoin' or  msg['text'] == '/ckCoinInfo':
                    bot.sendChatAction(chat_id, 'typing')
                    CKCOMMAND.append(msg['text'])
                    bot.sendMessage(chat_id, "<= Select Exchange => \
                    \n /bxinth  --> www.bx.in.th \
                    \n /bittrex --> www.bittrex.com \
                    \n /yobit   --> www.yobit.com")
                    
                elif msg['text'] == '/bxinth' and '/buyCoin' in CKCOMMAND:
                    bot.sendChatAction(chat_id, 'typing')
                    BX.append('bxinth')
                    bot.sendMessage(chat_id, "<= Select Coin => \
                    \n /BTCTHB \
                    \n /DASHTHB \
                    \n /LTCTHB \
                    \n /BCHTHB \
                    \n /GNOTHB \
                    \n /OMGTHB \
                    \n /REPTHB \
                    \n /XRPTHB \
                    \n /XZCTHB \
                    \n /ETHTHB ")
                    CKCOMMAND.clear()
                elif msg['text'] == '/bxinth' and '/ckCoinInfo' in CKCOMMAND:
                    bot.sendChatAction(chat_id, 'typing')
                    for coin in BXCOIN: 
                        bot.sendMessage(chat_id, str(get_coin_information(bxin, coin)))
                    CKCOMMAND.clear()

                ### BTC BX ###
                elif msg['text'] == '/BTCTHB' and 'bxinth':
                    CoinBuy = "BTC/THB"
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, 'BTC/THB')))
                    bot.sendMessage(chat_id, str(get_balance(bxin)))
                    bot.sendMessage(chat_id, "How Many to Buy ?")
                    BX.append('BTC/THB')
                elif "BTC/THB" in BX and "bxinth":
                    bot.sendChatAction(chat_id, 'typing')
                    Buy=msg['text']
                    if  is_number(Buy) == True:
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")
                        BX.remove('BTC/THB')
                        BX.append('BUY')
                    else:

                        bot.sendMessage(chat_id, "Enter number only")
                        bot.sendMessage(chat_id, "How Many to Buy ?")
                ## DASH BX ##
                elif msg['text'] == '/DASHTHB' and 'bxinth':
                    CoinBuy = "DASH/THB"
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, 'DASH/THB')))
                    bot.sendMessage(chat_id, str(get_balance(bxin)))
                    bot.sendMessage(chat_id, "How Many to Buy ?")
                    BX.append('DASH/THB')
                elif "DASH/THB" in BX and "bxinth":
                    bot.sendChatAction(chat_id, 'typing')
                    Buy = msg['text']
                    if is_number(Buy) == True:
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")
                        BX.remove('DASH/THB')
                        BX.append('BUY')
                    else:
                        bot.sendMessage(chat_id, "Enter number only")
                        bot.sendMessage(chat_id, "How Many to Buy ?")
                ## LTC BX ##
                elif msg['text'] == '/LTCTHB' and 'bxinth':
                    CoinBuy = "LTC/THB"
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, 'LTC/THB')))
                    bot.sendMessage(chat_id, str(get_balance(bxin)))
                    bot.sendMessage(chat_id, "How Many to Buy ?")
                    BX.append('LTC/THB')
                elif "LTC/THB" in BX and "bxinth":
                    bot.sendChatAction(chat_id, 'typing')
                    Buy = msg['text']
                    if is_number(Buy) == True:
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")
                        BX.remove('LTC/THB')
                        BX.append('BUY')
                    else:

                        bot.sendMessage(chat_id, "Enter number only")
                        bot.sendMessage(chat_id, "How Many to Buy ?")
                ## BCH BX ##
                elif msg['text'] == '/BCHTHB' and 'bxinth':
                    CoinBuy = "BCH/THB"
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, 'BCH/THB')))
                    bot.sendMessage(chat_id, str(get_balance(bxin)))
                    bot.sendMessage(chat_id, "How Many to Buy ?")
                    BX.append('BCH/THB')
                elif "BCH/THB" in BX and "bxinth":
                    bot.sendChatAction(chat_id, 'typing')
                    Buy = msg['text']
                    if is_number(Buy) == True:
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")
                        BX.remove('BCH/THB')
                        BX.append('BUY')
                    else:

                        bot.sendMessage(chat_id, "Enter number only")
                        bot.sendMessage(chat_id, "How Many to Buy ?")
                ## ETH BX ##
                elif msg['text'] == '/ETHTHB' and 'bxinth':
                    CoinBuy = "ETH/THB"
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, 'ETH/THB')))
                    bot.sendMessage(chat_id, str(get_balance(bxin)))
                    bot.sendMessage(chat_id, "How Many to Buy ?")
                    BX.append('ETH/THB')
                elif "ETH/THB" in BX and "bxinth":
                    bot.sendChatAction(chat_id, 'typing')
                    Buy = msg['text']
                    if is_number(Buy) == True:
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")
                        BX.remove('ETH/THB')
                        BX.append('BUY')
                    else:

                        bot.sendMessage(chat_id, "Enter number only")
                        bot.sendMessage(chat_id, "How Many to Buy ?")
                ## OMG BX ##
                elif msg['text'] == '/OMGTHB' and 'bxinth':
                    CoinBuy = "OMG/THB"
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, 'OMG/THB')))
                    bot.sendMessage(chat_id, str(get_balance(bxin)))
                    bot.sendMessage(chat_id, "How Many to Buy ?")
                    BX.append('OMG/THB')
                elif "OMG/THB" in BX and "bxinth":
                    bot.sendChatAction(chat_id, 'typing')
                    Buy = msg['text']
                    if is_number(Buy) == True:
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")
                        BX.remove('OMG/THB')
                        BX.append('BUY')
                    else:

                        bot.sendMessage(chat_id, "Enter number only")
                        bot.sendMessage(chat_id, "How Many to Buy ?")
                ## REP BX ##
                elif msg['text'] == '/REPTHB' and 'bxinth':
                    CoinBuy = "REP/THB"
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, 'REP/THB')))
                    bot.sendMessage(chat_id, str(get_balance(bxin)))
                    bot.sendMessage(chat_id, "How Many to Buy ?")
                    BX.append('REP/THB')

                elif "REP/THB" in BX and "bxinth":
                    bot.sendChatAction(chat_id, 'typing')
                    Buy = msg['text']
                    if is_number(Buy) == True:
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")
                        BX.remove('REP/THB')
                        BX.append('BUY')
                    else:

                        bot.sendMessage(chat_id, "Enter number only")
                        bot.sendMessage(chat_id, "How Many to Buy ?")
                ## GNO BX ##
                elif msg['text'] == '/GNOTHB' and 'bxinth':
                    CoinBuy = "GNO/THB"
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, 'GNO/THB')))
                    bot.sendMessage(chat_id, str(get_balance(bxin)))
                    bot.sendMessage(chat_id, "How Many to Buy ?")
                    BX.append('GNO/THB')
                elif "GNO/THB" in BX and "bxinth":
                    bot.sendChatAction(chat_id, 'typing')
                    Buy = msg['text']
                    if is_number(Buy) == True:
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")
                        BX.remove('GNO/THB')
                        BX.append('BUY')
                    else:

                        bot.sendMessage(chat_id, "Enter number only")
                        bot.sendMessage(chat_id, "How Many to Buy ?")

                ##  XZC BX ##
                elif msg['text'] == '/XZCTHB' and 'bxinth':
                    CoinBuy = "XZC/THB"
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, 'XZC/THB')))
                    bot.sendMessage(chat_id, str(get_balance(bxin)))
                    bot.sendMessage(chat_id, "How Many to Buy ?")
                    BX.append('XZC/THB')
                elif "XZC/THB" in BX and "bxinth":
                    bot.sendChatAction(chat_id, 'typing')
                    Buy = msg['text']
                    if is_number(Buy) == True:
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")
                        BX.remove('XZC/THB')
                        BX.append('BUY')
                    else:
                        bot.sendMessage(chat_id, "Enter number only")
                        bot.sendMessage(chat_id, "How Many to Buy ?")

                ##  XRP BX ##
                elif msg['text'] == '/XRPTHB' and 'bxinth':
                    CoinBuy = "XRP/THB"
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id, str(get_coin_information(bxin, 'XRP/THB')))
                    bot.sendMessage(chat_id, str(get_balance(bxin)))
                    bot.sendMessage(chat_id, "How Many to Buy ?")
                    BX.append('XRP/THB')
                elif "XRP/THB" in BX and "bxinth":
                    bot.sendChatAction(chat_id, 'typing')
                    Buy = msg['text']
                    if is_number(Buy) == True:
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")
                        BX.remove('XRP/THB')
                        BX.append('BUY')
                    else:
                        bot.sendMessage(chat_id, "Enter number only")
                        bot.sendMessage(chat_id, "How Many to Buy ?")

                elif "bxinth" in BX and "BUY" in BX:
                    bot.sendChatAction(chat_id, 'typing')
                    Rate = msg['text']
                    Rate = check_sys("data=" + Rate + ";echo ${data#*/}")
                    if  is_number(Rate) == True:
                        Uid=(buy_coin(bxin, CoinBuy, Rate, Buy))
                        if Uid >= 0 and is_number(Uid) == True: ## Test
                            bot.sendMessage(chat_id, "You Buy:" + CoinBuy + "\n Price:" + str(Buy) + " Bath  \n Rate:" + str(
                            Rate) + " Bath \n Quality:"+str(format_float(float(Buy) / float(Rate)))+ "\n")
                            bot.sendMessage(chat_id,"<= protect your loss =>\
                            \n /TrailingStops \
                            \n /buyCoin"
                            )
                            #bot.sendMessage(chat_id,"Enter /buyCoin command for continue trading ..")
                            BX.clear()
                        else:
                            bot.sendMessage(chat_id,"Buy Coin incomplete,Please verify your balance ,,")
                            BX.clear()
                    else:
                        bot.sendMessage(chat_id, "Enter Number Only...")
                        bot.sendMessage(chat_id, "Now Last Price:/" + str(get_lastprice(bxin, BX[1])))
                        bot.sendMessage(chat_id, "Enter Coin Price Rate ?")

                elif msg['text'] == '/TrailingStops':
                    bot.sendChatAction(chat_id, 'typing')
                    bot.sendMessage(chat_id,'Enter Percent Cut loss')
                    CKLOSS.append('ckloss')
                elif 'ckloss' in CKLOSS:
                    CutLoss=msg['text']
                    if is_number(CutLoss) == True:
                        bot.sendMessage(chat_id,"Enter Percent Stop loss")
                        CKLOSS.remove('ckloss')
                        CKLOSS.append('stoploss')
                    else:
                        bot.sendMessage(chat_id, 'Enter Percent Cut loss')
                elif 'stoploss' in CKLOSS:
                    StopLoss=msg['text']
                    if is_number(StopLoss) == True:
                        bot.sendMessage(chat_id,"Uid:"+str(Uid)+" \
                       \n(%)StopLoss:"+str(StopLoss)+" \
                       \n(%)CutLoss:"+str(CutLoss))
                        ## Here insert database ##
                        bot.sendMessage(chat_id,'Continue to /buyCoin')
                        CKLOSS.clear()
                elif msg['text'] == '/ckwan':
                    bot.sendChatAction(chat_id, 'typing')
                    sys_ck = check_sys("wget http://ipecho.net/plain -O - -q ; echo")
                    if sys_ck != "":
                        bot.sendMessage(chat_id, "\U0001F30F\U000026A1 Your ip wan is " + sys_ck)
                elif msg['text'] == '/ckroomtemp':
                    bot.sendChatAction(chat_id, 'typing')
                    sys_ck = check_sys("bash /home/iams/iamsbot/bin/room_temperature")
                    if sys_ck != "":
                        bot.sendMessage(chat_id, "\U0001F6A8 Server Room temperature is " + sys_ck)
                elif msg['text'] == '/asicDash' and chat_id not in setmail:
                    bot.sendChatAction(chat_id, 'typing')
                    sys_ck = check_sys("wget http://ipecho.net/plain -O - -q ; echo")
                    if sys_ck != "":
                        bot.sendMessage(chat_id, "\U0001F30F Click:http://" + sys_ck + ":4001")
                elif chat_id in setmail:
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
                else:
                    bot.sendChatAction(chat_id, 'typing')
                    interact = '\U00002753 May I help you, Administrator'
                    bot.sendMessage(chat_id, interact)
                    bot.sendMessage(chat_id, "\U0001F4D8 Type /help command for management IAMS")


TOKEN = telegrambot
bot = YourBot(TOKEN)
bot.message_loop()
# tr = 0
# xx = 0
#sender = []

#############MAIN PROGRAM ###########
while 1:
    if str(web_site_online()) == "True":
        if Alarm == "ON":
            for adminid in adminchatid:
                temperature = check_sys('bash -x /home/iams/iamsbot/bin/room_temperature')
                print("Roomtemp Threshold: " + str(roomtempthreshold))
                if int(float(temperature)) >= roomtempthreshold:
                    bot.sendMessage(adminid,
                                    "\U0000203C\U0001F6A8\U0000203C CRITICAL: Server Room temperature Over threshold " + temperature + " Celsius")
                    roomflag = 1
                    time.sleep(5)
                elif int(float(temperature)) < roomtempthreshold and roomflag == 1:
                    bot.sendMessage(adminid,
                                    "\U0000203C\U00002714\U0000203C CLEAR: Server Room temperature " + temperature + " Celsius")
                    roomflag = 0
                    time.sleep(5)
        elif Alarm == "OFF":
            time.sleep(10)
            #print("Alarm state disable to all member..")
    else:
        print("IAMS no internet connection available.")
        time.sleep(10)  # sleep 10 seconds
