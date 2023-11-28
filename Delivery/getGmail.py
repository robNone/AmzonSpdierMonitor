
# -*- coding: utf-8 -*-
import sys


# sys.setdefaultencoding('utf8')
import imaplib, string, email,time

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import os
imaplib._MAXLINE = 20000000

M = imaplib.IMAP4_SSL("imap.gmail.com",993)

email1 = 'mitbbsyushen1989bu@gmail.com'
password = 'everestonline'
t=0
reList=['atoz-guarantee-no-reply@amazon.com','donotreply@amazon.com','order-update@amazon.com','@marketplace.amazon.com>',]
DTP={'value':None,'time':None,'msg':None}

value = ['','','']
def print_info(msg):
	global value 
	i = 0
	for header in ['From', 'To', 'Subject']:      #解析邮件头
		value[i] = msg.get(header, '')
		v = msg.walk()

		if value[i]:
			if header == 'Subject':                 #解析主题
				value[i] = decode_str(value[i])
			else:
				hdr, addr = parseaddr(value[i])
				name = decode_str(hdr)
				value[i] = u'%s <%s>' % (name, addr)
		i = i+1


def parseBody(message):
    # 循环信件中的每一个mime的数据块
    for part in message.walk():
        # 这里要判断是否是multipart，是的话，里面的数据是一个message 列表
        if not part.is_multipart():
            charset = part.get_charset()
            # print 'charset: ', charset
            contenttype = part.get_content_type()
            # print 'content-type', contenttype
            if 1==2:pass
            else:
                #不是附件，是文本内容
                return part.get_payload(decode=True) 


def decode_str(s):
	value, charset = decode_header(s)[0]
	if charset:value = value.decode(charset)
	return value

def main(umb):
	try:
		M = imaplib.IMAP4_SSL("imap.gmail.com",993)
		M.login(email1,password)####YYYY为密码
		M.select('INBOX',False)
		typ, data = M.search(None, 'ALL')
		print (len((data[0])))
		f,A,b,c=open('1.csv','a+'),open('2.csv','a+'),open('3.csv','a+'),open('4.csv','a+')
		ss=open('cc','a+')
		file_lis =[f,A,b,c]
		for num in range (umb,len((data[0]))):
			try:
				#  '(UID BODY.PEEK[])'
				typ, data = M.fetch(num,'(RFC822)')
				print(type(data[0][1]))
				msg = email.message_from_string(data[0][1])
				date2 = msg.get("Date")[0:24]
				print (msg.get("Date")[0:24])
				print_info(msg)
				DTP['time'],DTP['msg']=date2,msg
				sd(ss)
				# for f in range(len(file_lis)):
				# 	if isINTitle(f):sd(file_lis[f])
			except Exception as e:
				close_file(file_lis)				
				print( 'got msg error: %s' % e   )  
				# print num
				return main(num)
			# 	M.login(email1,password)####YYYY为密码
			# #print "wrong!"
			# 	M.select('INBOX',False)
			# 	print 'got msg error: %s' % e      
		# print "OK!"
		M.logout()
		close_file(file_lis)		
	except Exception as e:
		# print 12
		print ('imap error: %s' % e)
		time.sleep(100)
		# M.close()

def sd(op):
	sr= parseBody(DTP['msg'])
	
	op.write(value[2]+','+DTP['time']+','+sr+'\n ^*^')	

def isINTitle(umb):
    return value[0].find(reList[umb]) >=0


def close_file(file_lis):
	[file.close() for  file in file_lis]

if __name__ == '__main__':
#149289
    main(2718507)
	
