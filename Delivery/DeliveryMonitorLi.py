# -*- coding: utf-8 -*-
# import webdriver
from ast import While
from calendar import month
from turtle import title
from httpx import ASGITransport
from pip import main
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options
import time ,re, os,datetime,sys ,random 
import requests,zipfile,AsinItemToHtml

from yaml import KeyToken
from PostEmail import Email,EmailS ,EmailNECR	
from FindByHtml import findUpcByHtml,find_offers,find_offers
from selenium.webdriver.support.ui import WebDriverWait
from spider import Spider

from update import setScreenXls,readFile,getXlsList,setScreenXlsAsin,setScreenXlsa
STORESLIST=[]
PDATA=[]

DATADIC={
	"January":1,
	"February":2,	
	"March":3,	
	"April":4,	
	"May":5,	
	"June":6,	
	"July":7 ,	
	"August":8,	
	"September":9,	
	"October":10,	
	"November":11,	
	"December":12,	
 
}



CHROME_PROXY_HELPER_DIR = 'Chrome-proxy-helper'
# 存储自定义Chrome代理扩展文件的目录
CUSTOM_CHROME_PROXY_EXTENSIONS_DIR = 'chrome-proxy-extensions'
EMAILNAME='Delivery监控'
SELLERLIST=[ """"""]
def get_chrome_proxy_extension(proxy):
	"""获取一个Chrome代理扩展,里面配置有指定的代理(带用户名密码认证)
	proxy - 指定的代理,格式: username:password@ip:port
	"""
	m = re.compile('([^:]+):([^\@]+)\@(.+?):(\d+)').search(proxy)
	print (m.groups())

	if m:
		# 提取代理的各项参数
		username = m.groups()[0]
		password = m.groups()[1]
		ip = m.groups()[2]
		port = m.groups()[3]
		# 创建一个定制Chrome代理扩展(zip文件)
		if not os.path.exists(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR):
			os.mkdir(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR)
		extension_file_path = os.path.join(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR, '{}.zip'.format(proxy.replace(':', '_')))
		if not os.path.exists(extension_file_path):
			# 扩展文件不存在，创建
			zf = zipfile.ZipFile(extension_file_path, mode='w')
			zf.write(os.path.join(CHROME_PROXY_HELPER_DIR, 'manifest.json'), 'manifest.json')
			# 替换模板中的代理参数
			background_content = open(os.path.join(CHROME_PROXY_HELPER_DIR, 'background.js')).read()
			background_content = background_content.replace('%proxy_host', ip)
			background_content = background_content.replace('%proxy_port', port)
			background_content = background_content.replace('%username', username)
			background_content = background_content.replace('%password', password)
			zf.writestr('background.js', background_content)
			zf.close()
		return extension_file_path
	else:
		raise Exception('Invalid proxy format. Should be username:password@ip:port')

def findRW(asin ,br):
	reviews = re.search('(?<=title=").{0,5}(?=out of 5 stars)', str(br ).replace('\n',''))
	reviews = reviews != None and reviews.group().strip() or 0
	s,reviewsNumber= re.split('id="acrCustomerReviewText" class="a-size-base">',str(br ).replace('\n','')),None
	reviewsNumber = len(s) > 1 and re.split(" ", s[1])[0] or 0		
	print(reviewsNumber)
	print(reviews)
	try:
		if reviewsNumber==0:reviews=0
		PDATA.append({"asin":asin,"score":float(reviews), "commentsNum": int(reviewsNumber)})
	except Exception as es: print (es)


def getWebbYs(code,Asins,seller_List ,retQty):
	global EMAILNAME
	asinItems=[]
	while True:	
		cw=Spider(retQty)
		if 	cw.setZip_code(code)==0:
			cw.closeChrome()
			continue
		break
		
	browser =cw.browser
		# browser = webdriver.Chrome(executable_path="101\\chromedriver.exe",options=chrome_option,)
				# WebDriverWait(browser,10,poll_frequency=1,ignored_exceptions=None)
				# browser.set_page_load_timeout(10)
	
	for asin in Asins:
		while True:
			try:
				browser.get("https://www.amazon.com/dp/"+asin)
				# browser.get("https://www.amazon.com/dp/B0B65GKJCP")
	
				break
			except:
				print ('======wait======')
				time.sleep(1)
		time.sleep(1)
		isFind= lambda x:x != None and x.group().strip() or "N"
							# rl=find_offers(browser.page_source)
		title=''
		price ,Deliver ,BuyBox,Sellers  ,Shipsfrom,Soldby='','',True,'','',''
		isFBA,IsO	 ,IsFromAmazon =True,False,False
		isBaseAsin=False
		baseAsin=''
		if len( browser.find_elements_by_id("prodDetails"))>=1:
			baseAsin=browser.find_element_by_id('prodDetails').text
		if baseAsin.find(asin)>=0:isBaseAsin=True
		if browser.page_source.find("Sorry! We couldn't find that page. Try searching or go to Amazon's home page.")>1:
			continue
		ranks= len(browser.find_elements_by_xpath('//th[contains(text(),"Best Sellers Rank")]/following-sibling::td'))>=1 and	browser.find_elements_by_xpath('//th[contains(text(),"Best Sellers Rank")]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
		of= findUpcByHtml(browser.page_source,"","")	
		if browser.page_source.find('a-box-group')>=0:
			price= isFind(re.search('(?<=class="a-offscreen">\$).{0,8}(?=<)',browser.page_source.split('a-box-group')[1] ))
		else:price ='0'
		title =of[3]
		# price =len( browser.find_elements_by_xpath('//*[@class="a-offscreen"]'))>=1 and browser.find_element_by_xpath('//*[@class="a-offscreen"]').text or "N"
		Soldby= len( browser.find_elements_by_id("sellerProfileTriggerId"))>=1 and browser.find_element_by_id("sellerProfileTriggerId").text or "N"
		Shipsfrom =len( browser.find_elements_by_id("tabular-buybox"))>=1 and browser.find_element_by_id("tabular-buybox").text or "N"
		Shipsfrom=Shipsfrom.replace('Shipsfrom','').split('Sold by')[0].replace(' ','').replace('\n','')
		Shipsfrom=Shipsfrom.replace('Shipsfrom','')
		if of[1]==-1:
			BuyBox=False
		timeStr=''
		Deliver=cw.searchDeliver()
		try:
			# print (Deliver)
			if Deliver!='异常':
				if Deliver.find("fastest delivery")>=0:
					timeStr=Deliver.split("fastest delivery")[1].split('.')[0]
				else:
					timeStr=Deliver.replace("FREE delivery",'').split('.')[0]
				day=str(timeStr.strip().split(' ')[-1])
				if timeStr.find(',')<0:
						month=timeStr.strip().split(' ')[0].strip()
				else:
					month=timeStr.strip().split(',')[1].strip().split(' ')[0]
				timeStr='2022/'+str(DATADIC[month])+"/"+day
		except Exception as es:
			print(es)
			timeStr=''
		if browser.page_source.find("We don't know when or if this item will be back in stock.")>1:
			Deliver='无库存'

		qty=""
   
		if Deliver!='无库存' and Deliver!="异常" and retQty and False:
			try:
				if len(browser.find_elements_by_xpath('//*[contains(text(),") from")]'))>0:
					browser.find_elements_by_xpath('//*[contains(text(),") from")]')[0].click()
					# WebDriverWait(browser, 10).until(
					# 	EC.presence_of_all_elements_located((By.XPATH, '//input[@class="aod-div-for-focus"]'))
					# 	)
					while True:
						try:
							if len(browser.find_elements_by_xpath('//input[@name="submit.addToCart"]'))>1:
								break
						except:pass
					# //*[data-action="aod-atc-action"][0:]
					tie=0
					time.sleep(3)
					for  s  in  browser.find_elements_by_xpath('//input[@name="submit.addToCart"]')[:-1]:
						# print ('1')
						# if tie%2!=0:
						browser.execute_script("""document.getElementsByName('submit.addToCart')["""+str(tie)+"""].click() """)
						time.sleep(2)
						tie+=1
				else:
					browser.find_elements_by_xpath('//*[@id="add-to-cart-button"]')[0].click()
	 
					time.sleep(2)

					while True:
						time.sleep(0.2)
						try:
							browser.execute_script("""document.getElementById('attachSiNoCoverage-announce').click() """)
							# browser.find_elements_by_xpath('//*[@id="attach-popover-lgtbox"]')[0].click()
							break
						except:print ('sleep')
				time.sleep(2)
				# print (tie)
				browser.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
				time.sleep(2)
				index=0
				DeI=0
				while DeI<20:
					DeI+=1
					try:
						if len(  browser.find_elements_by_xpath('//div[@data-asin]'))==0 :break
						if len(  browser.find_elements_by_xpath('//div[@data-asin]'))==1 and len(  browser.find_elements_by_xpath('//div[@data-asin][@data-removed="true"]'))==1  :break
						for o in  browser.find_elements_by_xpath('//*[@class="a-dropdown-prompt"]'):
							print ( '购物车商品数'+str(len((browser.find_elements_by_xpath('//*[@class="a-dropdown-prompt"]')))))
							ind=0
							while ind < 10:
								time.sleep(0.5)
								ind+=1
								try:
									browser.find_elements_by_xpath('//*[@class="a-dropdown-prompt"]')[0].click()
									break
								except:print ('sleep')
							# browser.find_elements_by_xpath('//*[text()="10+"]')
							browser.find_elements_by_xpath('//*[text()="10+"]')[0].click()
							time.sleep(0.5)
							browser.find_elements_by_xpath('//input[@aria-label="Quantity"]')[0].send_keys('999')
							time.sleep(0.5)
							browser.find_elements_by_xpath('//*[@data-action="update"]')[0].click()
							# WebDriverWait(browser, 10).until(
							# EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-quantity-update-message a-spacing-top-mini"))
							#  )		
							B=0
							while B <10:
								try:
									
									if browser.find_elements_by_xpath('//input[@aria-label="Quantity"]')[0].get_attribute('value')!='999':break
									# if len(browser.find_elements_by_xpath('//div[@data-asin][@data-removed]'))!=1 and browser.find_elements_by_xpath('//div[@data-asin]')[0].get_attribute('data-asin')!=asin:break
									# if browser.find_elements_by_xpath('//div[@data-asin]')[0].get_attribute('data-asin')!=asin:break
								except:pass	
								B+=1
								time.sleep(0.5)
							time.sleep(0.5)
							print(browser.find_elements_by_xpath('//input[@aria-label="Quantity"]')[0].get_attribute('value'))
							if browser.find_elements_by_xpath('//div[@data-asin]')[0].get_attribute('data-asin')==asin:
								
							# print(browser.find_elements_by_xpath('//div[@data-asin]')[0].get_attribute('data-asin'))
								qty+=' '+browser.find_elements_by_xpath('//input[@aria-label="Quantity"]')[0].get_attribute('value')+','
								print( asin+'库存'+ browser.find_elements_by_xpath('//input[@aria-label="Quantity"]')[0].get_attribute('value'))
							time.sleep(1)
							browser.find_elements_by_xpath('//*[@value="Delete"]')[0].click()
							index+=1
							time.sleep(1)		
					except:browser.refresh()
			except Exception as es: print(es)
		if retQty and False:
			while True:
				try:
											# browser.get("https://www.amazon.com/gp/aod/ajax/ref=dp_aod_ALL_mbc?asin="+key[1]+"&m=&pinnedofferhash=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=")
										# browser.get("https://www.amazon.com/dp/"+key[0])
					browser.get("https://www.amazon.com/gp/aod/ajax/ref=dp_aod_ALL_mbc?asin="+asin+"&m=&pinnedofferhash=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=")
					break
				except:
					print ('======wait======')
					time.sleep(1)
			time.sleep(1)
			Sellers ,IsO=cw.find_offers(seller_List)
			if Sellers.find('Amazon')>=0:IsFromAmazon=True
		asinItems.append([asin,title,price,qty,timeStr,Sellers,ranks ,Soldby,Shipsfrom,IsO,IsFromAmazon ,isBaseAsin])
	browser.quit()	
	asinItems.insert(0,['asin','title','价格','qty',code,'跟卖用户','ranks','Soldby','Shipsfrom','是否有其他卖家','跟卖 是否shipping from amazon','是否是当前asin'])
	return asinItems
			# getWebbYs(page,keys)
   # ['641741859@qq.com','1517496767@qq.com','1634475170@qq.com',"78845417@qq.com","1192373460@qq.com","10098591@qq.com","70354857@qq.com"]

def chRef(ret,code_List):
	mainItem=ret[0]
	for l in range(len(ret[0])):
		for code in range(len( code_List)):
			mainItem[l].append( ret[code][l][4])
		mainItem[l].append(cTime(mainItem[l]))
	return  mainItem


def cTime(Deliver_Time_list):
	a=1
	for DeTi in Deliver_Time_list[12:]:
		if DeTi.find('/')<=0:continue
		try:
			# print (time.mktime( time.strptime(DeTi,'%Y/%m/%d')))
			day=(time.time()-(time.mktime( time.strptime(DeTi,'%Y/%m/%d'))) ) // (3600 * 24) 
			if abs(day)>=abs(7):a+=1
		except:pass
	return a == len(Deliver_Time_list[12:]) 

def RetDdliveryBycode(code_List ,Asin_List,seller_List):
	
	ret =[]
	# Asins=re.findall('B0.{8}', requests.get("http://82.156.171.227:5000/FindAll?asin_type=3").text)	
	Asins=[asin[0] for asin in Asin_List ]
	# Asins=["B083QHD3NV"]

	retQty= True
	for code in code_List:
		code=code.replace('\n','')
		ret.append(getWebbYs(code ,Asins,seller_List ,retQty))
		retQty=False
	# ret=getXlsList("Tasin.xls")
	ret[0]	=chRef(ret ,code_List)
	setScreenXls(ret,"asin.xls")	
	Email("monitor@hzallin.com",AsinItemToHtml.toHtml(ret),'监控')
 
# def StartJob():
	# RetDdliveryBycode()
if __name__ == "__main__":
	import time
	# page=input("页数:")
	# keys=input("key:")
	# keys=open('as.txt','r').readl/ines()
	# keys='hp laptop'
	seller_List="""
		Hot Tech Geek
		iPuzzle Online
		Ref Plus Pro
		design-jet
		Tech Plus Pro
		boomoo
		JGB Distribution
		BSEA Distribution.
		BSEA Distribution
		PPM LLC
		GLOBAL CR
		mint jewelry ll
		mint jewelry llc
		ScanIt!
		PPM LLC
		Hott Tech Geek
		Electronics Express Sale (Free 2-days Shipping)
		Poly Molly
		Office-Product
 
 """
	from apscheduler.schedulers.blocking import BlockingScheduler
	# 创建调度器：BlockingScheduler
	scheduler = BlockingScheduler()
	Asin_List=getXlsList("D.xls")[0]
	# keys=['08733','92376','77423','61611']
	keys=['02127','10055','28246','32277','94112','98121','85048','60626','77053','80206']
	keys=['19720','90081',]
 
			# seller_List=getXlsList("FBA.xls")[2]
	# keys=open('init','r').readlines()
	print (keys)
	time.sleep(60*60*4)
	RetDdliveryBycode( keys ,Asin_List,seller_List)
	# scheduler.add_job(RetDdliveryBycode, 'cron', hour =1,minute=0, id='test_job2',args=[ keys ,Asin_List,seller_List])
	# scheduler.add_job(RetDdliveryBycode, 'cron', hour =17,minute=0, id='test_job1',args=[ keys ,Asin_List,seller_List])
	# scheduler.start()
 

		