import smtplib
import re
######Check Email #######
import pymysql
import sys
import os
import time
from datetime import datetime ## for datetime
import webbrowser

#######Check Internet ####
import socket
import requests
REMOTE_SERVER = "www.google.com"
###########################

shellexecution = []
shellconfirm = []
requestcommandconfirm = []
addserverconfirm = []
memberserverconfirm = []
timelist = []
memlist = []
xaxis = []
settingmemth = []
setmail = []
setapprove = []
setconfirm = []
setpolling = []
setshellhost = []
setrequestshellcommand = []
setrequestaliascommand = []
setrequestshellserver = []
shellexecutionhost = []
settingroomtemp = []
graphstart = datetime.now()

##########################
check_member = []
check_admin = []

###Register ####
reg_name = []
reg_lname = []
reg_mail = []
reg_tele = []
reg_desc = []
###Add Server ### 
add_sname = []
add_sip = []
add_sdesc = []
###Add Server Member ## 
add_smember = []
memberserverid = []
#################
delmember=[]
delserver=[]
delserverchatid=[]
listserver=[]
listcommand=[]


def Update_DB(table,col,data,chat_id):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="UPDATE  `"+table+"` SET "+col+"=%s WHERE ChatID=%s"
       cursor.execute(sql,(data,chat_id))
       con.commit()
       con.close()
       return "OK"
    except:
       return "Failed"

def Update_SMDB(table,col,data,serverid,chatid):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="UPDATE  `"+table+"` SET "+col+"=%s WHERE ServerID=%s and ChatID=%s"
       cursor.execute(sql,(data,serverid,chatid))
       con.commit()
       con.close()
       return "OK"
    except:
       return "Failed"

def Insert_SMDB(sid,time,chatid,status):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="INSERT INTO  `servermember` (`ServerID`,`Time`,`ChatID`,`Status`) VALUES (%s,%s,%s,%s)"
       cursor.execute(sql,(sid,time,chatid,status))
       con.commit()
       con.close()
       return "OK"
    except:
       return "Failed"

def Update_Alarm(chatid,alarmstatus,time):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="UPDATE  `alarmstatus` SET AlarmStatus=%s,Time=%s WHERE ChatID=%s"
       cursor.execute(sql,(alarmstatus,time,chatid))
       con.commit()
       con.close()
       return "OK"
    except:
       return "Failed"

def Insert_Alarm(chatid,alarmstatus,time):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="INSERT INTO  `alarmstatus` (`chatid`,`alarmstatus`,`Time`) VALUES (%s,%s,%s)"
       cursor.execute(sql,(chatid,alarmstatus,time))
       con.commit()
       con.close()
       return "OK"
    except:
       return "Failed"


def Get_DB(table,col,chat_id):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="SELECT "+col+" FROM `"+table+"` where ChatID="+chat_id
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results[0][0]
    except:
       return "failed"

def Get_ID(table,col,role):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       #sql="SELECT "+col+" FROM `"+table+"` where Role="+role
       sql="SELECT `"+col+"` FROM `"+table+"` where `Role`=\""+role+"\""
       print(sql)
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results
    except:
       return "failed"

def Get_IDSERVER(table,col,server):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="SELECT `"+col+"` FROM `"+table+"` where `ServerName`=\""+server+"\""
       #print(sql)
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results[0][0]
    except:
       return "Null"

def Get_CHATIDSERVER(table,col,server,chatid):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       #sql="SELECT `"+col+"` FROM `"+table+"` where `ServerName`=\""+server+"\" and `ChatID`="+chatid
       sql="SELECT `"+col+"` FROM `"+table+"` where `ServerName`=\""+server+"\""
       print(sql)
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results[0][0]
    except:
       return "Null"

def Get_IDSMEMBER(table,col,server):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="SELECT `"+col+"` FROM `"+table+"` where `ServerID`=\""+server+"\""
       print(sql)
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results
    except:
       return "Null"

def Get_CHATMEMBER_ALARM(servername,chatid,status):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="SELECT servermember.ChatID FROM `servermember`, `serverlist` WHERE servermember.ServerID and serverlist.ID and serverlist.ServerName=\""+servername+"\" and servermember.ChatID=\""+chatid+"\" and servermember.Status=\""+status+"\""
       print(sql)
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results[0][0]
    except:
       return "Null"


def Get_MEMBER():
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="SELECT `ChatID`,`Name` FROM `register` where `Role`=\"member\""
       print(sql)
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results
    except:
       return "Null"

def Get_SERVER():
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="SELECT `ServerName`,`ChatID` FROM `serverlist`"
       print(sql)
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results
    except:
       return "Null"

def Get_SERVEROWN(ChatID):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="SELECT `ID`,`ServerName` FROM `serverlist` WHERE `ChatID`="+ChatID
       print(sql)
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results
    except:
       return "Null"

def Get_IPSERVER(table,col,ip):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="SELECT `"+col+"` FROM `"+table+"` where `IP`=\""+ip+"\""
       print(sql)
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results[0][0]
    except:
       return "Null"
###Get ChatID History approve ### 
def Get_HISPROVE_ID(table,col,approve,chatid):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       #sql="SELECT `"+col+"` FROM `"+table+"` where `Approve`=\""+approve+"\"  and  `ChatID`="+chatid
       sql="SELECT `"+col+"` FROM `"+table+"` where `Approve`=\""+approve+"\"  and  `ChatID`="+chatid
       print(sql)
       cursor.execute(sql)
       results=cursor.fetchall()
       con.close()
       return results
    except:
       return "Null"

##################

def Insert_DB(chat_id,name,lastname,mail,tele,desc,role,status,time):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="INSERT INTO  `register` (`ChatID`,`Name`,`LastName`,`Email`,`Telephone`,`Description`,`Role`,`Status`,`Time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
       cursor.execute(sql,(chat_id,name,lastname,mail,tele,desc,role,status,time))
       con.commit()
       con.close()
       return "OK"
    except:
       return "Failed"

def Insert_SDB(sname,ip,desc,time,chatid):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="INSERT INTO  `serverlist` (`ServerName`,`IP`,`Description`,`Time`,`ChatID`) VALUES (%s,%s,%s,%s,%s)"
       cursor.execute(sql,(sname,ip,desc,time,chatid))
       con.commit()
       con.close()
       return "OK"
    except:
       return "Failed"

def Insert_SMDB(sid,time,chatid,status):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="INSERT INTO  `servermember` (`ServerID`,`Time`,`ChatID`,`Status`) VALUES (%s,%s,%s,%s)"
       cursor.execute(sql,(sid,time,chatid,status))
       con.commit()
       con.close()
       return "OK"
    except:
       return "Failed"

def Insert_HISST(namestatus,approve,approveby,timestart,timeend,chatid):
    try:
       con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
       cursor=con.cursor()
       sql="INSERT INTO  `historystatus` (`NameStatus`,`Approve`,`ApproveBy`,`TimeStart`,`TimeEnd`,`ChatID`) VALUES (%s,%s,%s,%s,%s,%s)"
       cursor.execute(sql,(namestatus,approve,approveby,timestart,timeend,chatid))
       con.commit()
       con.close()
       return "OK"
    except:
       return "Failed"


def Del_DB(table,chat_id):
   con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
   cursor=con.cursor()
   sql="DELETE FROM `"+table+"` WHERE `ChatID`="+chat_id
   try:
       cursor.execute(sql)
       con.commit()
   except:
       con.rollback()
       return "failed"
   return "OK"
   con.close()


def Del_SDB(table,server,chat_id):
   con=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='iams_db')
   cursor=con.cursor()
   sql="DELETE FROM `"+table+"` WHERE `ServerName`=\""+server+"\" AND `ChatID`="+chat_id
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
def send_mail(mail,body_mail):
    TO = mail
    SUBJECT = 'This is message from IAMS'
    TEXT = body_mail
    gmail_sender = 'iams.notify@gmail.com'
    gmail_passwd = 'Admin_123456789'
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    #server.starttls()
    server.login(gmail_sender, gmail_passwd)
    BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])
    try:
       print("sendmail "+gmail_sender+" To:"+TO+"  Body:"+BODY)
       server.sendmail(gmail_sender, [TO], BODY)
       server.close()
       print ("Email have sent ..")
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

def clearregister(chat_id):
    if chat_id in reg_name:
       reg_name.remove(chat_id)
    if chat_id in reg_lname:
       reg_lname.remove(chat_id)
    if chat_id in reg_mail:
       reg_mail.remove(chat_id)
    if chat_id in reg_tele:
       reg_tele.remove(chat_id)
    if chat_id in reg_desc:
       reg_desc.remove(chat_id)
def clearaddcommand(chat_id):
    if chat_id in setrequestshellserver:
       setrequestshellserver.remove(chat_id)

def clearaddserver (chat_id):
    if chat_id in add_sname:
       add_sname.remove(chat_id)
    if chat_id in add_sip:
       add_sip.remove(chat_id)
    if chat_id in add_sdesc:
       add_sdesc.remove(chat_id)

def clearlist(chat_id):    
    if chat_id in listcommand: 
       listcommand.remove(chat_id)
    if chat_id in listserver:
       listserver.remove(chat_id)

def clearservermember (chat_id):
    if chat_id in memberserverconfirm:
       memberserverconfirm.remove(chat_id)
    if chat_id in add_smember:
       add_smember.remove(chat_id)
    if chat_id in memberserverid:
       memberserverid.remove(chat_id)

def clearall(chat_id):
    if chat_id in shellexecution:
       shellexecution.remove(chat_id)
    if chat_id in settingmemth:
       settingmemth.remove(chat_id)
    if chat_id in setpolling:
       setpolling.remove(chat_id)
    if chat_id in setmail:
       setmail.remove(chat_id)
    if chat_id in setapprove:
       setapprove.remove(chat_id)
    if chat_id in setconfirm:
       setconfirm.remove(chat_id)
    if chat_id in shellconfirm:
       shellconfirm.remove(chat_id)
    if chat_id in shellexecutionhost:
       shellexecutionhost.remove(chat_id)
    if chat_id in setshellhost:
       setshellhost.remove(chat_id)
    if chat_id in add_smember:
       add_smember.remove(chat_id)
def clearsetting(chat_id):
    if chat_id in settingroomtemp:
       settingroomtemp.remove(chat_id)

def cleardel(chat_id):
    if chat_id in delmember:
       delmember.remove(chat_id)
    if chat_id in delserver:
       delserver.remove(chat_id)
    if chat_id in delserverchatid:
       delserverchatid.remove(chat_id)

def web_site_online(url='http://www.google.com/', timeout=5):
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
    #num_format = re.compile("^[\-]?[1-9][0-9]*\.?[0-9]+$")
    num_format = re.compile("^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$")
    isnumber = re.match(num_format,num)
    if isnumber:
        return "TRUE"
    else:
        return "FALSE"



#send_mail("javacpp.exp@gmail.com","Your OTP password is xxxxxxxxxxxx")
#DB=Get_SERVER()
#print(ck_mail)
#DB=Get_SERVEROWN('263956990')
#print(DB)
#DB=Del_SDB('serverlist','SERVER1-WWW','263956990')
#print(DB)
#DB=Del_SDB('serverlist','SERVER2-WWW')
#print (DB)
#DB=Del_DB('alarmstatus','263956990')
#print (DB)
#DB=Del_DB('serverlist','263956990')
#print (DB)
#DB=Del_DB('servermember','263956990')
#print (DB)
#def openwep(url):

# MacOS
#chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

# Windows
#      chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'

# Linux
# chrome_path = '/usr/bin/google-chrome %s'

#      webbrowser.get(chrome_path).open(url)



#openwep ('http://docs.python.org/')
#






#print (checknum("333333553"))
#Insert_Alarm ('263956990','ON',time.strftime('%Y-%m-%d %H:%M:%S'))
#Update_Alarm('263956990','OFF',time.strftime('%Y-%m-%d %H:%M:%S'))
#DB=Get_DB('alarmstatus','AlarmStatus','263956990')
#print(DB)

#DB=Get_IDSERVER('serverlist','ID','SERVER1-WWW')
#print(DB)

#from prettytable import PrettyTable
#member=[]
#t = PrettyTable(['ChatID', 'Name'])
#for i in Get_MEMBER():
#   for j in i: 
#       member.append(j)  
#   t.add_row(member)
#   member=[]

#print(str(t))
    # t.add_rows(Get_MEMBER())
#print (table.draw())
#imemberlist=[[]]
#member=[]
#print("ChatID \tName \tLastname")
#for i in Get_MEMBER():
#       member.append(i)

#print(member)
#DB=Get_CHATMEMBER_ALARM('IAMS','263956991','disable')
#print(DB)
#Chat_Status=Get_DB('register','Status','263956990')
#print(Chat_Status)
#sender="20161108103950:91000017:CLEAR:DISK_CHECK:IAMS:Running Space /dev/root :65%:Iams_Client"
#ServerName=check_sys("echo "+sender+"|awk -F: '{print $5}'")
#print(ServerName)
#ChatID=Get_IDSERVER('serverlist','ChatID',ServerName)
#print(ChatID)



#print(Get_DB('register','ChatID',''))
#MCID=Get_IDSMEMBER('servermember','ChatID','9000')
#if str(MCID) == "()":
#   print("TRUE")
#else: 
#   print("FALSE")
#memberchatid = []

#Insert_HISST('addcommand','wait','263956990',time.strftime('%Y-%m-%d %H:%M:%S'),'0','263956991')
#APID=Get_HISPROVE_ID('historystatus','ID','Wait','263956991')
#for L in APID :
#    memberchatid.append(int(L[0]))
#print (memberchatid)


#DB=Update_SMDB('servermember','Status','enable','9001','263956990')
#print(DB)


#DB=Get_CHATIDSERVER('serverlist','ChatID','www-server','263956990')
#DB=Get_IDSMEMBER('servermember','ChatID','9001')
#print(DB)
#for L in DB :
#    memberserverid.append(int(L[0]))
#print (memberserverid)
#Insert_SMDB('9001',time.strftime('%Y-%m-%d %H:%M:%S'),'263956990','disable')
#Insert_SDB("www-server","192.168.1.222","Server For Test",time.strftime('%Y-%m-%d %H:%M:%S'),"263956990")
#DB=Get_DB('register','Status','263956990')
#print(DB)
#DB=Get_IPSERVER('serverlist','IP','192.168.1.222')
#print(DB)
#DBL=[]
#DB=Get_ID('register','ChatID','member')
#for L in DB :
#    print(L[0].replace("'", ""))
#    DBL.append(int(L[0]))
#DBL.append("END")
#print (DBL)
#data=check_sys ("ifconfig")
#if data == "":
#  print("Null")
#else:
#  print(data)
#print(data)
#for item in check_sys ("service"):
#    if item:
#        newlist.append(str(item))

#print (item)
#newlist=filter(lambda x: len(x)>0, check_sys ("service"))
#print(str(newlist[0]))
#str_list = [x for x in check_sys ("chkconfig") if x != '']
#print (str_list)
#print(s.replace('\n\n','\n'),check_sys ("service"))
#filtered = filter(lambda x: not re.match(r'^\s*$', x), check_sys ("service"))
#for i in filtered:
#    print(i+"11")
