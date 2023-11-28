# -*- coding: utf-8 -*-  
from __future__ import unicode_literals

from email.mime.multipart import MIMEMultipart
from re import sub
from datetime import datetime
import smtplib  
# import email.MIMEMultipart# import MIMEMultipart  
# import email.MIMEText# import MIMEText  
# import email.MIMEBase# import MIMEBase  
import os.path  
import mimetypes 
from email.mime.application import MIMEApplication 
from update import setScreenXls,readFile,getXlsList,setScreenXlsAsin,setScreenXlsa

import time	
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# def pEmail(eAcct):
# 	From = "1634475170@qq.com"
# 	To = eAcct 
# 	# ti=time.strftime('%Y-%m-%d',time.localtime(time.time()))
# 	# file_name =ti +".xls"#附件名  
	  
# 	server = smtplib.SMTP_SSL("smtp.qq.com", 465)
# 	server.login("1634475170@qq.com","wsencctrzopwbgig") # pwd=QQ密码 仅smtp服务器需要验证时  

# 	# main_msg.attach(file_msg	# 设置根容器属性  
# 	main_msg['From'] = From  
# 	main_msg['To'] = To  
# 	main_msg['Subject'] = "xsellco "  
# 	main_msg['Date'] = email.Utils.formatdate( )  
	  
# 	# 得到格式化后的完整文本  
# 	fullText = main_msg.as_string( )  
	  
# 	# 用smtp发送邮件  
# 	try:  
# 	    server.sendmail(From, To, fullText)  
# 	    print '发送成功'+To
# 	finally:  
# 	    server.quit()  



def EmailS(to,text):
# 第三方 SMTP 服务
	sender = "pcdrob@foxmail.com"
	send_file = open(r"asin.xls", "rb").read()
	att = MIMEApplication(send_file)
	att['Content-Type'] = 'application/octet-stream'
	att['Content-Disposition'] = 'attachment;filename="asin.xls"'	 
	 
	message = MIMEMultipart('easybiz')
	message['From'] = Header("pcdRob", 'utf-8')
	message['To'] =  Header(to, 'utf-8')
	subject =text
	message['Subject'] = Header("跟卖信息", 'utf-8')
	message.attach(att)
	try:
		smtpObj =  smtplib.SMTP_SSL("smtp.qq.com", 465)
		smtpObj.login("pcdrob@foxmail.com","resrvcqpqjqebach") 
		smtpObj.sendmail(sender, to, message.as_string())
		print ("邮件发送成功")
		print (to)
	except smtplib.SMTPException as e:
		print ( "Error: 无法发送邮件",str(e))



def EmailNECR(to,text ,title):
# 第三方 SMTP 服务
	sender = "pcdrob@foxmail.com"
	send_file = open(r"asin.xls", "rb").read()
	att = MIMEApplication(send_file)
	att['Content-Type'] = 'application/octet-stream'
	att['Content-Disposition'] = 'attachment;filename="ASIN.xls"'	 
	
	message = MIMEMultipart("")
	message.attach(MIMEText(text, 'plain', 'utf-8'))
 	# message = MIMEText(text, 'html', 'utf-8')

	message['From'] = Header("pcdRob", 'utf-8')
	message['To'] =  Header(to, 'utf-8')
	 
	subject ="商品跟卖信息"
	subject=title
	message['Subject'] = Header(subject, 'utf-8')
	message.attach(att)
	try:
		smtpObj =  smtplib.SMTP_SSL("smtp.qq.com", 465)
		smtpObj.login("pcdrob@foxmail.com","nqmkoydcwlsycgjj") 
		smtpObj.sendmail(sender, to, message.as_string())
		print ("邮件发送成功")
		print (to)
	except smtplib.SMTPException as e:
		print ( "Error: 无法发送邮件",str(e))

    # 第三方 SMTP 服务
	sender = "pcdrob@foxmail.com"
	send_file = open(r"asin.xls", "rb").read()
	att = MIMEApplication(send_file)
	att['Content-Type'] = 'application/octet-stream'
	att['Content-Disposition'] = 'attachment;filename="ASIN.xls"'	 
	
	message = MIMEMultipart("")
	message.attach(MIMEText(text, 'plain', 'utf-8'))
 	# message = MIMEText(text, 'html', 'utf-8')

	message['From'] = Header("pcdRob", 'utf-8')
	message['To'] =  Header(to, 'utf-8')
	 
	subject ="商品跟卖信息"
	subject=title
	message['Subject'] = Header(subject, 'utf-8')
	message.attach(att)
	try:
		smtpObj =  smtplib.SMTP_SSL("smtp.qq.com", 465)
		smtpObj.login("pcdrob@foxmail.com","nqmkoydcwlsycgjj") 
		smtpObj.sendmail(sender, to, message.as_string())
		print ("邮件发送成功")
		print (to)
	except smtplib.SMTPException as e:
		print ( "Error: 无法发送邮件",str(e))

def Email(to,text ,title):
	# 第三方 SMTP 服务
	sender = "mnitor1@vip.163.com"
	send_file = open(r"asin.xls", "rb").read()
	att = MIMEApplication(send_file)
	att['Content-Type'] = 'application/octet-stream'
	
	att['Content-Disposition'] = 'attachment;filename="ASIN'+ str(datetime.now().month)+str(datetime.now().day)+'.xls"'	 
	
	message = MIMEMultipart("")
	message.attach(MIMEText(text, 'html', 'utf-8'))
 	# message = MIMEText(text, 'html', 'utf-8')
	# keys=	getXlsList("start.xls")
	message['From'] = Header("pcdRob", 'utf-8')
	message['To'] =  Header(to, 'utf-8')
	 
	subject ="商品跟卖信息"
	subject=title
	message['Subject'] = Header(subject, 'utf-8')
	message.attach(att)
	try:
		smtpObj =  smtplib.SMTP_SSL("smtp.vip.163.com", 465)
		# smtpObj.login("mnitor@vip.163.com","UQQEBKGIVSJGCUYU")
		smtpObj.login("mnitor1@vip.163.com","RRZBQADXRVQVBQDL")
  
		# smtpObj =  smtplib.SMTP_SSL("smtp.vip.tom.com", 465)
		# smtpObj.login("mnitor@vip.tom.com","1634475170q")
		# smtpObj.login("pcdrob@foxmail.com","gajrncivnkzffbhd")
		# smtpObj.login("pcdrob@foxmail.com","gajrncivnkzffbhd")
		# smtpObj =  smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
		# smtpObj.login("monitor@hzallin.com","JSRD8JGkEaFLWizE") 
		smtpObj.sendmail(sender,  to, message.as_string())
		print ("邮件发送成功")
		# print (to)
	except smtplib.SMTPException as e:
		print ( "Error: 无法发送邮件",str(e))


def Emails(to,text ,title ,path):
    	# 第三方 SMTP 服务
	sender = "mnitor1@vip.163.com"
	send_file = open(path, "rb").read()
	att = MIMEApplication(send_file)
	att['Content-Type'] = 'application/octet-stream'
	att['Content-Disposition'] = 'attachment;filename="'+path.split('\\')[-1]+'"'	 
	
	message = MIMEMultipart("")
	message.attach(MIMEText(text, 'html', 'utf-8'))
 	# message = MIMEText(text, 'html', 'utf-8')
	# keys=	getXlsList("start.xls")
	message['From'] = Header("pcdRob", 'utf-8')
	message['To'] =  Header(to, 'utf-8')
	 
	subject ="商品跟卖信息"
	subject=title
	message['Subject'] = Header(subject, 'utf-8')
	message.attach(att)
	try:
		smtpObj =  smtplib.SMTP_SSL("smtp.vip.163.com", 465)
		# smtpObj.login("mnitor@vip.163.com","UQQEBKGIVSJGCUYU")
		smtpObj.login("mnitor1@vip.163.com","RRZBQADXRVQVBQDL")
  
		# smtpObj =  smtplib.SMTP_SSL("smtp.vip.tom.com", 465)
		# smtpObj.login("mnitor@vip.tom.com","1634475170qQ")
		# smtpObj.login("pcdrob@foxmail.com","gajrncivnkzffbhd")1634475170qQ
		# smtpObj.login("pcdrob@foxmail.com","gajrncivnkzffbhd")
		# smtpObj =  smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
		# smtpObj.login("monitor@hzallin.com","JSRD8JGkEaFLWizE") 
		smtpObj.sendmail(sender,  to, message.as_string())
		print ("邮件发送成功")
		# print (to)
	except smtplib.SMTPException as e:
		print ( "Error: 无法发送邮件",str(e))		
if __name__ == '__main__':
	# Email("monitor@hzallin.com",' ','Active ASINs Review监控','D:\File\qx\ActiveASINsReview413.xls')A2TC87EJKQMY9O
    	
	Emails("monitor@hzallin.com",' ','Active ASINs Review监控','c:\File\Qx\ActiveASINsReview2023-11-21.xls')
 
