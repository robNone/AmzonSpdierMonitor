# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.chrome.service import Service
import time ,re, os,datetime,sys ,random

from PostEmail import Email,EmailS ,EmailNECR
from FindByHtml import findUpcByHtml,find_offers,find_offers
from update import setScreenXls,readFile,getXlsList,setScreenXlsAsin,setScreenXlsa
STORESLIST=[]

def getWebbYs(keys):
	sc=[str(s[0]).replace("\xa0"," ") for s in keys[2]]
	# bs=random.choice(keys[1])
	STORESLIST=[[],[],[],[]]
	bb=[]
	ba=[]
	NotFind=[]
	# for bs in keys[1]:
	if True:
		# asins=[]
		url='https://www.amazon.com/'
		chrome_option = Options()
		chrome_option.add_argument('--no-sandbox')
		chrome_option.add_argument('--disable-dev-shm-usage')
		# chrome_option.add_argument('--headless')
		chrome_option.add_argument('--disable-gpu')
		chrome_option.add_argument('--ignore-certificate-errors')
		chrome_option.add_argument('--disable-dev-shm-usage')
  

		# chrome_option.add_argument('–disable-javascript')
		# chrome_option.add_argument('user-agent=%s'%user_agent) 
		# chrome_option.add_argument('Accept-Language=en;q=0.8') 
		# browser_locale = 'en'
		# chrome_option.add_argument(r'user-data-dir=User Data')
		# chrome_option.add_argument("--lang={}".format(browser_locale))
		chrome_option.add_experimental_option('excludeSwitches', ['enable-logging'])
		chrome_option.add_argument('disable-infobars') 
		prefs = {"profile.managed_default_content_settings.images": 2}
		chrome_option .add_experimental_option("prefs", prefs)
		browser =None

	

		try:
			browser = webdriver.Chrome(executable_path="chromedriver.exe",options=chrome_option)
				# browser.set_window_size(1920,1080) 
			browser.get(url)
			print('get')
			time.sleep(3)
			if True:
				if True:
						time.sleep(3)
						browser.find_element_by_id("glow-ingress-line1").click()
						time.sleep(4)
						try:
							browser.find_element_by_id("GLUXChangePostalCodeLink").click()
							time.sleep(4)
							browser.find_element_by_id('GLUXZipUpdateInput').clear()
							time.sleep(3)
						except Exception as es:pass
						# print(type(bs))
						browser.find_element_by_id('GLUXZipUpdateInput').send_keys("10010")
						time.sleep(3)
						browser.find_element_by_css_selector('#GLUXZipUpdate > span > input').click()
						time.sleep(5)
						browser.refresh()
						time.sleep(5)
						# browser.find_element_by_id('twotabsearchtextbox').send_keys(key[2])
						# browser.find_element_by_css_selector('#nav-search-submit-text > input').click()
						# time.sleep(2)   
				dog =""
				for key in keys[0]:
					key[0]=key[1]
					try:
						# if key[7] !="Currently unavailable" and key[8]!="Your question might be":
							browser.get("https://www.amazon.com/dp/"+key[0])
							# browser.get("https://www.amazon.com/gp/aod/ajax/ref=dp_aod_ALL_mbc?asin="+key[0]+"&m=&pinnedofferhash=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=")
							time.sleep(3)
							# rl=find_offers(browser.page_source)
							if browser.page_source.find("Sorry! We couldn't find that page. Try searching or go to Amazon's home page.")>=1:
								print ('1')
								dog+=key[0]+"\n"
								STORESLIST[3].append([key[0],])
								continue
							of= findUpcByHtml(browser.page_source,"","")	
							# browser.st
							if of[1]==-1:
								bb.append([key[0],True,[],[],of])
							elif of[14]!=0:
								#  of[15] not in sc and 
								browser.get("https://www.amazon.com/gp/aod/ajax/ref=dp_aod_ALL_mbc?asin="+key[0]+"&m=&pinnedofferhash=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=")
								time.sleep(3)
								bb.append([key[0],False,find_offers(browser.page_source),of[5],of])
							elif float(of[5])<3:
								STORESLIST[2].append([key[0]])
								ba.append(key[0])
						# STORESLIST.append(key)
					except Exception as es:
						print (es)
				# print asins
				print (bb)
				if bb!=[] or ba!=[] or STORESLIST[3]!=[]:
					NoBuybox ,ob ,dvbv ,dogs='掉buybox \n',' ASIN      被跟卖个数     卖家id           卖家名字              review               title\n',"差评商品","变狗\n"
					for sv,tt,sz ,scb ,of in bb:
						if tt:
							NoBuybox+=""+sv+"\n"	
							STORESLIST[0].append([sv,])		
						else:
							for v in sz:
								if v[-3] not in sc:
									ob+=" "+sv+"  "+sz[-1][-1]+"           "+v[-2]+"    " +v[-3]+ "  "+scb+"           "+of[3]+"\n"
									STORESLIST[1].append([sv,of[3],sz[-1][-1],v[-2],v[-3],scb])
							time.sleep(3)
					print (NoBuybox)
					print (ob)
					setScreenXls(STORESLIST,"x.xls")
					# [EmailNECR(x,NoBuybox+ob+dogs+dog) for x in ['1517496767@qq.com','1634475170@qq.com',"78845417@qq.com","1192373460@qq.com","10098591@qq.com","70354857@qq.com"]]
		except Exception as es:
			print (es)
			browser.quit()
		browser.quit()

			# getWebbYs(page,keys)

if __name__ == "__main__":
	import time
	# page=input("页数:")
	# keys=input("key:")
	# keys=open('as.txt','r').readl/ines()
	# keys='hp laptop'
	keys=	getXlsList("赶跟卖-2.xlsx")
	getWebbYs(keys)