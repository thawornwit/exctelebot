import smtplib
import re
import random
######Check Email #######
import pymysql
import sys
import os
import time
from datetime import datetime  ## for datetime
import webbrowser

#######Check Internet ####
import socket
import requests


REMOTE_SERVER = "www.google.com"
###########################

global con

##################
def Update_OrderBuy(UUID, Exchange, Status):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE order_buy SET Status=%s WHERE UUID=%s AND Exchange=%s"
        cursor.execute(sql, (Status, UUID, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

def Update_OrderStopBuy(UUID, Exchange, Status):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE order_stopbuy SET Status=%s WHERE UUID=%s AND Exchange=%s"
        cursor.execute(sql, (Status, UUID, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

def Update_OrderSale(UUID, Exchange, Status):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE order_sale SET Status=%s WHERE UUID=%s AND Exchange=%s"
        cursor.execute(sql, (Status, UUID, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

## Insert CoinBalance ##
def Insert_CoinBlance(Exchange,Coin,Total,Used,Free,ChatID):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "INSERT INTO  `coin_balance` (`Exchange`,`Coin`,`Total`,`Used`,`Free`,`ChatID`) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (Exchange,Coin,Total,Used,Free,ChatID))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"
## Update CoinBalance ##
def Update_CoinBlance(Exchange,Coin,Total,Used,Free,ChatID):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE `coin_balance` SET Total=%s,Used=%s,Free=%s WHERE ChatID=%s AND Exchange=%s AND Coin=%s"
        cursor.execute(sql, (Total,Used,Free,ChatID,Exchange,Coin))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"
## GetCoinBalance ##
def Get_CoinBlance(Exchange,Coin,ChatID): ## buy,sold status
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT * FROM `coin_balance` where `Coin`=\""+Coin+"\" and `Exchange`=\"" + Exchange + "\" and `ChatID`=\"" + ChatID + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results
    except:
        return "failed"
## Insert Profitt ##
def Insert_Profit(UUID,Time,Exchange,Coin,Volumn, Buy,Sell,Margin):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "INSERT INTO  `profit` (`UUID`,`Time`,`Exchange`,`Coin`,`Volumn`,`Buy`,`Sell`,`Margin`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (UUID, Time, Exchange, Coin, Volumn, Buy, Sell,Margin))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"
# OrDer_Buy
def Insert_OrderBuy(UUID, Exchange, Time, Coin_Market, Quantity, Rate, Status):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "INSERT INTO  `order_buy` (`UUID`,`Time`,`Coin_Market`,`Quantity`,`Rate`,`Status`,`Exchange`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (UUID, Time, Coin_Market, Quantity, Rate, Status, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

#OrDer_Sell
def Insert_OrderSale(UUID, Exchange, Time, Coin_Market, Quantity, Rate, Status):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "INSERT INTO  `order_sale` (`UUID`,`Time`,`Coin_Market`,`Quantity`,`Rate`,`Status`,`Exchange`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (UUID, Time, Coin_Market, Quantity, Rate, Status, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

## Order StopBuy ##
def Insert_OrderStopBuy(UUID, Exchange, Time, Coin_Market, Quantity, Rate, Status):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "INSERT INTO  `order_stopbuy` (`UUID`,`Time`,`Coin_Market`,`Quantity`,`Rate`,`Status`,`Exchange`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (UUID, Time, Coin_Market, Quantity, Rate, Status, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"
####################
def Get_OrderBuy(Exchange,Status): ## buy,sold status
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT * FROM `order_buy` where `Status`=\""+Status+"\" and `Exchange`=\"" + Exchange + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results
    except:
        return "failed"

def Get_OrderStopBuy(Exchange,Status): ## buy,sold status
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT * FROM `order_stopbuy` where `Status`=\""+Status+"\" and `Exchange`=\"" + Exchange + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results
    except:
        return "failed"


def Get_OrderSale(Exchange,Status): ## sell ,sold status
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT * FROM `order_sale` where `Status`=\""+Status+"\" and `Exchange`=\"" + Exchange + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results
    except:
        return "failed"


def Insert_OpenOrder(UUID,Time,Coin,Type,Rate,Qty,Total,Status,Exchange,Strategy):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "INSERT INTO  `open_older` (`UUID`,`Time`,`Coin`,`Type`,`Rate`,`Qty`,`Total`,`Status`,`Exchange`,`Strategy`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (UUID, Time, Coin, Type, Rate, Qty,Total, Status, Exchange,Strategy))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"


def Update_OpenOrder(UUID, Exchange, Status):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE open_older SET Status=%s WHERE UUID=%s AND Exchange=%s"
        cursor.execute(sql, (Status, UUID, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"
##Oder Sale

def Get_Rate_OpenOrder(UUID,Exchange,Coin,Type):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT `Rate` FROM `open_older` where `UUID`=\"" + UUID + "\" and  `Type`=\""+Type+"\" and `Coin`=\""+Coin+"\" and `Exchange`=\"" + Exchange + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results[0][0]
    except:
        return "Failed"

def Get_OpenOrder(Exchange,Status):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT * FROM `open_older` where `Status`=\""+Status+"\" and `Exchange`=\"" + Exchange + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results
    except:
        return "Failed"

## Statigy ###
def Get_Nbuy(Exchange,Coin):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT * FROM `Nbuy` where `Exchange`=\"" + Exchange + "\" and `Coin`=\"" + Coin + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results
    except:
        return "Failed"

def Get_Nsell(Exchange, Coin):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT * FROM `Nsell` where `Exchange`=\"" + Exchange + "\" and `Coin`=\"" + Coin + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results
    except:
        return "Failed"



##Ckloss BTS,STS

def Insert_ckloss(UUID, Exchange, Stoploss, Cutloss, StoplossPoint):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "INSERT INTO  `ckloss` (`UUID`,`Exchange`,`Stoploss`,`Cutloss`,`StoplossPoint`) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (UUID, Exchange, Stoploss, Cutloss, StoplossPoint))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

def Update_StopLoss(UUID, Exchange, Stoploss):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE ckloss SET Stoploss=%s WHERE UUID=%s AND Exchange=%s "
        cursor.execute(sql, (Stoploss, UUID, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

def Update_CutLoss(UUID, Exchange, Cutloss):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE ckloss SET Cutloss=%s WHERE UUID=%s AND Exchange=%s "
        cursor.execute(sql, (Cutloss, UUID, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

def Update_Stoppoint(UUID, Exchange, StoplossPoint):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE ckloss SET StoplossPoint=%s WHERE UUID=%s AND Exchange=%s "
        cursor.execute(sql, (StoplossPoint, UUID, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

################
## CkstopBuy ##

def Insert_ckstopbuy(UUID, Exchange, StopRisk, StopBuy, StopBuyPoint):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "INSERT INTO  `ckstopbuy` (`UUID`,`Exchange`,`StopRisk`,`StopBuy`,`StopBuyPoint`) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (UUID, Exchange, StopRisk, StopBuy, StopBuyPoint))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

def Update_StopRisk(UUID, Exchange, StopRisk):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE ckstopbuy SET StopRisk=%s WHERE UUID=%s AND Exchange=%s "
        cursor.execute(sql, (StopRisk, UUID, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

def Update_StopBuy(UUID, Exchange, StopBuy):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE ckstopbuy SET StopBuy=%s WHERE UUID=%s AND Exchange=%s "
        cursor.execute(sql, (StopBuy, UUID, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"

def Update_StopBuyPoint(UUID, Exchange, StopBuyPoint):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "UPDATE ckstopbuy SET StopBuyPoint=%s WHERE UUID=%s AND Exchange=%s "
        cursor.execute(sql, (StopBuyPoint, UUID, Exchange))
        con.commit()
        con.close()
        return "OK"
    except:
        return "Failed"
############

def Get_BittrexOrder_buy(UUID, Exchange, table, col):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT `" + col + "` FROM `" + table + "` where `UUID`=\"" + UUID + "\" and `Status`=\"buy\" and `Exchange`=\"" + Exchange + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results[0][0]
    except:
        return "failed"


def Get_BittrexOrder_UUID(Exchange):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT `UUID` FROM `order_buy` where `Status`=\"buy\" and `Exchange`=\"" + Exchange + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results
    except:
        return "failed"


def Get_BittrexOpen_Order(Exchange,Type,Symbol):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT * FROM `open_older` where `Status`=\"open\" and `Exchange`=\"" + Exchange + "\" and `Type`=\""+Type+"\" and `Coin`=\""+Symbol+"\"" 
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results
    except:
        return "failed"


def Get_BittrexDB(UUID, Exchange, table, col):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT `" + col + "` FROM `" + table + "` where `UUID`=\"" + UUID + "\" and `Exchange`=\"" + Exchange + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results[0][0]
    except:
        return "failed"


def Get_Bittrex_Price(Market, Exchange):
    try:
        con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
        cursor = con.cursor()
        sql = "SELECT `Last_Price` FROM `Coin_LastPrice` where `Market_Coin`=\"" + Market + "\" and `Exchange`=\"" + Exchange + "\""
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        return results[0][0]
    except:
        return "failed"

def Update_Last_Price(Price,Market, Exchange):
        try:
            con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='bittrex_bot')
            cursor = con.cursor()
            sql = "UPDATE Coin_LastPrice SET `Last_Price`=%s WHERE `Market_Coin`=%s AND `Exchange`=%s"
            cursor.execute(sql, (Price,Market,Exchange))
            con.commit()
            con.close()
            return "OK"
        except:
            return "Failed"


def Del_DB(table, chat_id):
    con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='iams_db')
    cursor = con.cursor()
    sql = "DELETE FROM `" + table + "` WHERE `ChatID`=" + chat_id
    try:
        cursor.execute(sql)
        con.commit()
    except:
        con.rollback()
        return "failed"
    return "OK"
    con.close()


def Del_SDB(table, server, chat_id):
    con = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='iams_db')
    cursor = con.cursor()
    sql = "DELETE FROM `" + table + "` WHERE `ServerName`=\"" + server + "\" AND `ChatID`=" + chat_id
    try:
        cursor.execute(sql)
        con.commit()
    except:
        con.rollback()
        return "failed"
    return "OK"
    con.close()


def email(email):
    match = re.search(r'[\w.-]+@[\w.-]+.\w+', email)

    if match:
        return 0
    else:
        return 1


######Func tion Mail ######
def send_mail(mail, body_mail):
    TO = mail
    SUBJECT = 'This is message from IAMS'
    TEXT = body_mail
    gmail_sender = 'iams.notify@gmail.com'
    gmail_passwd = 'Admin_123456789'
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    # server.starttls()
    server.login(gmail_sender, gmail_passwd)
    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])
    try:
        print("sendmail " + gmail_sender + " To:" + TO + "  Body:" + BODY)
        server.sendmail(gmail_sender, [TO], BODY)
        server.close()
        print("Email have sent ..")
        return 0
    except:
        print("Something went wrong ..")
        return 1

    server.quit()


####Function command Bash ####
def check_sys(sys):
    ck = os.popen(sys)
    ck_read = ck.read()
    text = os.linesep.join([s for s in ck_read.splitlines() if s])
    return text


def web_site_online(url='http://www.google.co.th/', timeout=20):
    try:
        req = requests.get(url, timeout=timeout)
        # HTTP errors are not raised by default, this statement does that
        req.raise_for_status()
        return True
    except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(
            e.response.status_code))
    except requests.ConnectionError:
        return False


def checknum(num):
    # num_format = re.compile("^[\-]?[1-9][0-9]*\.?[0-9]+$")
    num_format = re.compile("^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$")
    isnumber = re.match(num_format, num)
    if isnumber:
        return "TRUE"
    else:
        return "FALSE"


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

def insert_orderbuy_test(Exchange,Coin,Oty,Rate,Status):
    count = 0
    number = ''.join(random.sample("0123456789", 4))
    print('Number of randome is ' + number)
    ## Insert Coin ####
    UUID = str(number) + '425861b8' + str(number)
    print(UUID)
    print(Insert_ckloss(UUID,Exchange, 5, 5, 0))  ## Percent Check Loss ##
    Status = Insert_OrderBuy(UUID,Exchange, time.strftime('%Y-%m-%d %H:%M:%S'),Coin,Oty,Rate,Status)
    print(Status)

def insert_orderbuy_test(Exchange,Coin,Oty,Rate,Status):
    count = 0
    number = ''.join(random.sample("0123456789", 4))
    print('Number of randome is ' + number)
    ## Insert Coin ####
    UUID = str(number) + '425861b8' + str(number)
    print(UUID)
    print(Insert_ckloss(UUID,Exchange, 5, 5, 0))  ## Percent Check Loss ##
    Status = Insert_OrderBuy(UUID,Exchange, time.strftime('%Y-%m-%d %H:%M:%S'),Coin,Oty,Rate,Status)
    print(Status)

def insert_ordersale_test(Exchange,Coin,Oty,Rate,Status):
    count = 0
    number = ''.join(random.sample("0123456789", 4))
    print('Number of randome is ' + number)
    ## Insert Coin ####
    UUID = str(number) + '425861b8' + str(number)
    print(UUID)
    print(Insert_ckloss(UUID,Exchange, 5, 5, 0))  ## Percent Check Loss ##
    Status = Insert_OrderSale(UUID,Exchange,time.strftime('%Y-%m-%d %H:%M:%S'),Coin,Oty,Rate,Status)
    print(Status)





#Rate="1"
#CK=(is_number(Rate))
#print("Action "+str(CK))E
#if CK == True:
#   print("Ok")




#print("--------------------------")
#print(Get_OrderBuy(UUID,'bxinth','buy'))
#ST = Insert_OpenOrder(UUID,time.strftime('%Y-%m-%d %H:%M:%S'),'DASH/THB','sell',4000, 0.01,400,'open', 'bxinth')
#print(ST)
##ST=Update_OpenOrder('542461','bxinth','close')

#ST=Get_BittrexOpen_Order('bxinth','sell','OMG/THB')
#print("Status:"+str(ST))
#for order in list(ST):
#    time=(order[2])
#    order_id=(order[1])
 #   coin=(order[3])
 #   rate=(order[5])
 #   qty=(order[6])
 #   total=(order[7])
 #   print(""+time+"\nO:/"+order_id+"\nC:"+coin+"\nR:"+str(rate)+"\nQ:"+str(qty)+"\nT:"+str(total) )

if __name__ == "__main__":

    #CK=Insert_CoinBlance('bxinth','LTC',10,0,10,342111)
    #print(CK)
    #CK=Update_CoinBlance('bxinth','LTC',100,0,100,'342111')
    #print(CK)
    CK=Get_CoinBlance('bxinth','BCH','342111')
    print(CK)

    #ST=Update_Last_Price('900000','BTC/THB','bxinth')
    #ST=Get_OpenOrder('bxinth','open')
    #ST=insert_ordersale_test('bxinth','DASH/THB',100,31000,'sell')
    #print(ST)

    #ST=insert_orderbuy_test('bxinth','DASH/THB',100,140,'buy')
    #print(ST)
   # SK=Insert_Profit("123456",time.strftime('%Y-%m-%d %H:%M:%S'),'bxinth',"LTC/THB",1,30000,40000,10000)
   # print(SK)
    #ST=Get_Nsell('bxinth','ETH/THB')
    #for N in list(ST):
     #   Coin=N[2]
     #   Count=N[3]
      #  print("NSell Coint is "+Coin+ " Discount is "+str(Count)+"")

    #ST = Get_Nbuy('bxinth', 'ETH/THB')
    #for N in list(ST):
    #    Coin = N[2]
    #    Count = N[3]
     #   print("Nbuy Coint is " + Coin + " Discount is " + str(Count) + "")
    #for order in list(ST):
    #    time=(order[2])
     #   order_id=(order[1])
      #  coin=(order[3])
      #  Type=(order[4])
      #  rate=(order[5])
      #  volumn=(order[6])
      #  qty=(order[7])
      #  print(""+time+"\nO:/"+order_id+"\nC:"+coin+"\nR:"+str(rate)+"\nQ:"+str(qty)+"\nVolumn:"+str(volumn) )
#ST=Get_Rate_OpenOrder('560134','bxinth','DASH/THB','buy')
#print(ST)
# count+=1
# CutLossPrice=(380 - (380 * (5 / 100)))
# print(CutLossPrice)
#Status=Insert_OrderBuy('e606d53c-8d70-11e3-94b5-425861b86ab6',time.strftime('%Y-%m-%d %H:%M:%S'),'USDT-BCC',3,318.9,'buy')
#print(Status)


#Status=Insert_OrderSale(time.strftime('%Y-%m-%d %H:%M:%S'),'USDT-BCC',3,318.9,20,0,'e606d53c-8d70-11e3-94b5-425861b86ab6')
#print(Status)

#Insert_ckloss('e606d53c-8d70-11e3-94b5-425861b86ab6',5,5,0.9545)
#status=Update_Stoppoint('e606d53c-8d70-11e3-94b5-425861b86ab6',290)
#Update_OrderBuy('e606d53c-8d70-11e3-94b5-425861b86ab6','buy')
#print(status)
#print(Get_BittrexDB('e606d53c-8d70-11e3-94b5-425861b86ab6','order_buy','Rate'))
#Get_BittrexOrder_buy(,table,col):
#if eneable == "ON":
#   Insert_ckloss('e606d53c-8d70-11e3-94b5-425861b86aa7',5,5,0)
#   stat=Insert_OrderBuy('e606d53c-8d70-11e3-94b5-425861b86aa7',time.strftime('%Y-%m-%d %H:%M:%S'),'USDT-BCC',4,334.9,'buy') 
#print(stat)
