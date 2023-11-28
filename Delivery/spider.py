# -*- coding: utf-8 -*-
from pickle import LIST
from ChromeHelper import get_chrome_proxy_extension
#from threading import Lock
#from tkinter.messagebox import RETRY
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time ,re
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from threading import Lock
import sys 
if sys.version_info[0] < 3:
	reload(sys)
	sys.setdefaultencoding('utf8')
class Spider:
		STORESLIST=[]
		FirstStar=True
		ASINS=[]
		DOGELIST=[]
		Zip_code=None
		storeName=[]
		EmailText=""
		retQty=True
		postData=[]
		
		browser =webdriver.Chrome
		def __init__(self ,retQty ):
			# self.store=[str(s[0]).replace("\xa0"," ") for s in keys[2]]
			# self.Zip_code=random.choice(keys[1])
			self.retQty=retQty
			self.browser=self.initChrome()
			
			print ("=================init====================")

		def initChrome(self):
			browser =None
			# profile = webdriver.FirefoxProfile()
			# ip,port='tunnel.qg.net',14027
			# settings = {
			# 	'network.proxy.type': 1,  # 0: 不使用代理；1: 手动配置代理
			# 	'network.proxy.http': ip,
			# 	'network.proxy.http_port': port,
			# 	'network.proxy.ssl': ip,  # https的网站,
			# 	'network.proxy.ssl_port': port,

			# }
			# for key, value in settings.items():
			# 	profile.set_preference(key, value)

			# # profile.update_preferences()
			# options = Options()
			# options.set_preference('permissions.default.image',2)
			# return webdriver.Firefox(firefox_profile=profile, options=options)
			chrome_option = Options()
			chrome_option.add_argument('--no-sandbox')
			# chrome_option.add_argument('--disable-dev-shm-usage')
			chrome_option.add_argument('--headless')
			chrome_option.add_argument('--disable-gpu')
			# chrome_option.add_argument('--ignore-certificate-errors')
			chrome_option.add_argument('--disable-dev-shm-usage')

			chrome_option.add_argument('--proxy-server=tunnel5.qg.net:16588')
			# chrome_option.add_argument('window-size=1920x1080');
			# chrome_option.add_argument("--proxy-server=http://tunnel5.qg.net:16588")
			# chrome_option.add_argument("--proxy-server=https://tunnel5.qg.net:16588")
   
			chrome_option.add_argument("user-agent="+"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
							
							)
			chrome_option.add_argument("blink-settings=imagesEnabled=false")

			# chrome_option.add_argument("--proxy-server=SOCKS5://1tunnel5.qg.net:16588")
			# chrome_option.add_extension(get_chrome_proxy_extension(proxy='6637554A:1B5A52BB43DD@tunnel.qg.net:14027'))
			# chrome_option.add_extension(get_chrome_proxy_extension(proxy='127.0.0.1:1080'))1
			# chrome_option.add_extension('Keepa.crx')
			# chrome_option.add_extension(get_chrome_proxy_extension(proxy='304504D9:50C3CCDAD815@tunnel5.qg.net:16588'))
			# chrome_option.add_experimental_option('excludeSwitches', ['enable-logging'])
			# chrome_option.add_argument('disable-infobars') 
			# chrome_option.add_argument('disable-infobars')
			# chrome_option.add_experimental_option("excludeSwitches", ['enable-automation'])
			# chrome_option.add_experimental_option("useAutomationExtension",'False')
			# chrome_option.add_argument('--disable-infobars')
			# chrome_option.add_experimental_option('excludeSwitches', ['enable-logging'])
			# prefs = {"profile.managed_default_content_settings.images": 2}
			# chrome_option.binary_location='D:\\ps\\Chrome-bin\\chrome\\App\\Chrome-bin\\chrome.exe'
			# chrome_option .add_experimental_option("prefs", prefs)
			# return webdriver.Chrome(executable_path="C:\\File\\chrome\\chromedriver.exe",options=chrome_option,)
			return webdriver.Chrome(options=chrome_option,)
   
			return webdriver.Chrome(executable_path="101\\chromedriver.exe",options=chrome_option,)

			# return webdriver.Chrome(executable_path="D:\\ps\\Chrome-bin\\chrome\\91.exe",options=chrome_option,)

		def find_offers(self ,seller_List):
			html=self.browser.page_source
			isFind= lambda x:x != None and x.group().strip() or "N"
			ret ,LIS='',False

			for cs in re.split('<h5>',html)[1:]:
				reb=False
				tp=(re.split('</h5>',cs)[0].replace('\\n\'','').replace('\'','').replace(',',''))
				price= isFind(re.search('(?<=class="a-offscreen">\$).{0,8}(?=<)',cs ))
				Shipsfrom=isFind(re.search('(?<=<span class="a-size-small a-color-base">).+?(?=<)',cs ))
				Sold_by=isFind(re.search('(?<=role="link">).+?(?=<)',cs.replace('\n','') )).replace('\\n\', \'','')
				# open('a.html','a+').writelines(cs)
				# print (Shipsfrom)
				# return Shipsfrom+ ' , '+Sold_by
				if seller_List.find (Sold_by.strip())<0:LIS=True
				ret+=''+tp+' , '+ price+' , '+ Shipsfrom+ ' , '+Sold_by+'   \n'
			return [ret ,LIS]

		def searchDeliver(self):
			try:
				# self.browser.find_elements_by_xpath('//*[@class="a-offscreen"]')

				return self.browser.find_element(By.ID,'deliveryBlockMessage').text
			except:
				return '异常'
		def  setZip_code(self ,code):
			try:
				self.browser.get("https://www.amazon.com/")
				time.sleep(3)
				# self.browser.refresh()
				# self.browser.find_element_by_xpath('')
				# time.sleep(10)
				if self.browser.page_source.find('e the characters you see in this image:')>0:return 0
				self.browser.find_element(By.ID,"glow-ingress-line1").click()
				time.sleep(10)
				try:
					self.browser.find_element(By.ID,"GLUXChangePostalCodeLink").click()
					time.sleep(4)
					self.browser.find_element(By.ID,'GLUXZipUpdateInput').clear()
					# self.browser.fin
					time.sleep(3)
				except Exception as es:pass
				az='02127	10055	32277	94112	85048	60626	77053	80206'
				
				self.browser.find_element(By.ID,'GLUXZipUpdateInput').send_keys(str(code))
				time.sleep(3)
				self.browser.find_element(By.CSS_SELECTOR,'#GLUXZipUpdate > span > input').click()
				time.sleep(5)
				if self.browser.page_source.find("此邮政编码目前不可用。请关闭此窗口，然后重试。")>0 or  self.browser.page_source.find("Please enter a valid US zip code")>0:return 2
				self.browser.refresh()
				# self.browser.lod


				print ("=================邮政编码成功====================")
				return 1
			except :return 0

		def setkeepa(self):

			self.browser.get('https://keepa.com/')
			WebDriverWait(self.browser,30).until(EC.presence_of_element_located((By.ID,'searchInput')))
			time.sleep(3)
			# self.browser.find_element(By.ID,'panelUserRegisterLogin').
			self.browser.find_element(By.ID,'panelUserRegisterLogin').click()	
			time.sleep(1)
			self.browser.find_element(By.ID,'password').send_keys('123abc')
			self.browser.find_element(By.ID,'username').send_keys('hzcy')
			time.sleep(1)
			self.browser.find_element(By.ID,'submitLogin').click()	
			time.sleep(10)


		def get_Amazon_Rew(self,asin):
			try:

				self.browser.get("https://www.amazon.com/gp/customer-reviews/widgets/average-customer-review/popover/ref=dpx_acr_pop_?contextId=dpx&asin="+asin[0])
				
				while True:
					time.sleep(1)
					if self.browser.page_source.find('Type the characters you see in this image:')>0 or self.browser.page_source.find("We're sorry, an error has occurred. Please reload this page and try again.")>0  :
							self.browser.refresh()
							time.sleep(1)
					else:
							break
			except:pass
			if   self.browser.page_source.find("Sorry! We couldn't find that page. Try searching or go to Amazon's home page.")<0 and self.browser.page_source.find("<html><head></head><body></body></html>")<0 and self.browser.page_source!="":
				return self.parse_rank_Html(asin)
			else:return [asin[0],0,0]
		def parse_rank_Html(self,asin):
			if self.browser.page_source.find("BAAAAAAD ASIN")>0:return [asin[0],0,0]
			rating=self.browser.page_source.split("</span>")[0]
			rating= rating.split(">")[len(rating.split(">"))-1].replace("星，共 5 星","").replace(" ","")
			ratingumb=self.browser.page_source.split("</span>")[2]
			ratingumb= ratingumb.split(">")[len(ratingumb.split(">"))-1].replace("个全球评分","").replace(",","")
			return [asin[0],rating,ratingumb]
		def  parse_AsinHtml(self ,asin):
			isFind= lambda x:x != None and x.group().strip() or "N"
			name=	self.browser.find_element(By.ID,"productTitle").text
			# name=	self.browser.find_elements_by_xpath("productTitle").text
   
			# price=	self.browser.find_element(By.ID,"price_inside_buybox").text
			price = re.search('(?<=a-offscreen">\$).+?(?=</span>)',str(self.browser.page_source ).replace('\n','') )
			price = price != None and price.group().strip().split('"')[0] or 'None'
			p= re.split("a-price a-text-price a-size-medium",str(self.browser.page_source ).replace('\n',''))
			if len(p)>1:
				price = re.search('(?<=a-offscreen">\$).+?(?=</span>)',p[1])
				price = price != None and price.group().strip().split('"')[0] or 'None'
	
				
			# reviewe= len(self.browser.find_elements_by_class_name("a-icon-alt"))>=1 and self.browser.find_element_by_class_name("a-icon-alt").text.replace("out of 5 stars","")  or"N" 
			# revieweNum= len(self.browser.find_elements_by_id("acrCustomerReviewText"))>=1 and self.browser.find_element(By.ID,"acrCustomerReviewText").text.replace(",","")  or"N" 
			reviews = re.search('(?<=title=").{0,5}(?=out of 5 stars)', str(self.browser.page_source ).replace('\n',''))
			reviews = reviews != None and reviews.group().strip() or 0
			s,reviewsNumber= re.split('id="acrCustomerReviewText" class="a-size-base">',str(self.browser.page_source ).replace('\n','')),None
			reviewsNumber = len(s) > 1 and re.split(" ", s[1])[0] or 0		
			print(reviewsNumber)
			print(reviews)

			# {"asin":"B07VGRJDFY","score":0, "commentsNum": 0}
			try:
				if reviewsNumber==0:reviews=0
				self.postData.append({"asin":asin[0],"score":float(reviews), "commentsNum": int(reviewsNumber)})
			except Exception as es: print (es)
			storeName= len(self.browser.find_elements_by_id("sellerProfileTriggerId"))>=1 and	self.browser.find_element(By.ID,"sellerProfileTriggerId").text or "N"
			# storeId= len(self.browser.find_elements_by_id("sellerProfileTriggerId"))>=1 and	self.browser.find_element(By.ID,"sellerProfileTriggerId").get_attribute("href")or "N"
			# s=self.browser.find_element_by_xpath("Best Sellers Rank")
			brand= len(self.browser.find_elements_by_id("bylineInfo"))>=1 and	self.browser.find_element(By.ID,"bylineInfo").text or "N"
			storeId=isFind(re.search('(?<=seller=).+?(?=\&)',str(self.browser.page_source ).replace('\n','') )).split('"')[0]
			offers =re.search('(?<=\().{0,5}(?=\) from)',str(self.browser.page_source ).replace('\n','') )    
			isBuybox=str(self.browser.page_source ).replace('\n','').find("a-box-group")>=1 and  "False"or "True"
			ranks= len(self.browser.find_elements_by_xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()="\nBest Sellers Rank\n"]/following-sibling::td'))>=1 and	self.browser.find_elements_by_xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()="\nBest Sellers Rank\n"]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
			# date= len(self.browser.find_elements_by_link_text(' Date First Available '))>=1 and	self.browser.find_elements_by_link_text(' Date First Available ')[0].text.replace("\n","")or "N"
			offers =offers!=None and offers.group() or '0'
			Currently_unavailable=self.browser.page_source.find("Currently unavailable")>=1 and "True" or "False"
			us= "Buybox"
			if isBuybox=="True" and Currently_unavailable =="True":
				us="无库存"
			elif isBuybox=="True" and Currently_unavailable !="True":
				us="NoBuybox"
			if price == 'None':price=asin[3]
			if storeName == 'N':storeName=asin[5]
			if storeId == 'N':storeId=asin[6]
			# print(self.browser.find_elements_by_tag_name('td'))
			data=self.browser.find_element(By.ID,'productDetails_detailBullets_sections1').text.split('\n')[-1]
			# Date First Available
			if data.find('Date First Available')>=0:data=data.replace('Date First Available','')
			else :data='N'
			# print(data)
			return [asin[0],'False',name ,price ,str(reviews),storeName,storeId,offers,time.asctime( time.localtime(time.time()) ),brand,ranks,isBuybox ,us ,"N" ,"N",data]
		def getAsin(self,asin):
			self.browser.get("https://www.amazon.com/dp/"+asin[0])
			time.sleep(1)
			if self.browser.page_source.find("validateCaptcha")>=0:
				time.sleep(20)
				return self.getAsin(self,asin)
			if self.browser.page_source.find("Sorry! We couldn't find that page. Try searching or go to Amazon's home page.")>=1:
				if len(asin)<2:
					# asin.append("True")
					asin=[asin[0],"True","N","N","N","N","N","N",time.asctime( time.localtime(time.time()) ),"","","","N","N","N"]
				else:
					if asin[1] !="True":
						asin[1]='True'
						asin[8]=time.asctime( time.localtime(time.time()) )
				return asin
			return self.parse_AsinHtml(asin)
	
		def AddNewSrore(self ,storeId):
			# if storeId in self.store:self.store.append(storeId)
			lambda	storeId : storeId not in self.store   and  self.store.append (storeId) (storeId)
		def closeChrome(self):
			self.browser.quit()
		
		def aShoudAsin(self):
			index=0
			for asin in self.STORESLIST :
				# a+=1
				# print (a)
				try:

					asinitem=(self.getAsin(asin))


					if  len(asin)>10:
							# print  (sqlite().execute("INSERT INTO asinTable (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0]))

						if len(asin)==1 :pass

						elif asin[12] ==asinitem[12] :
							asinitem[13]=asin[13]
							asinitem[14]=asin[14] 
						#重新上架asin
						elif asin[12]!="Buybox" and  asinitem[12] =="Buybox":
						#重新上架时间
							asinitem[13]=asin[13]
							asinitem[14]=asinitem[8]
						# 下架时间
						elif asin[12]!=asinitem[12]:
							asinitem[13]=asinitem[8]
							asinitem[14]=asin[14] 
					else:
						if asinitem[12]!="Buybox":
							asinitem[13]=asinitem[8]
		
					print(asinitem)
			
					self.STORESLIST[index]=asinitem
				except Exception as  es :
					print(es)
				index+=1
				# self.AddNewSrore(asin[5])
			print (self.STORESLIST)
		
  
		def newaShoudAsin(self ):
			# for asin in self.STORESLIST :
			while ASINITEMESLIST:
				# a+=1
				# print (ASINITEMESLIST)
				lock1.acquire()
				asin,index=ASINITEMESLIST.pop()
				lock1.release()
				try:

					asinitem=(self.getAsin(asin))
					if  len(asin)>10:
							# print  (sqlite().execute("INSERT INTO asinTable (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0]))

						if len(asin)==1 :pass
						elif asin[12] ==asinitem[12] :
							asinitem[13]=asin[13]
							asinitem[14]=asin[14] 
						#重新上架asin
						elif asin[12]!="Buybox" and  asinitem[12] =="Buybox":
						#重新上架时间
							asinitem[13]=asin[13]
							asinitem[14]=asinitem[8]
						# 下架时间
						elif asin[12]!=asinitem[12]:
							asinitem[13]=asinitem[8]
							asinitem[14]=asin[14] 
					else:
						if asinitem[12]!="Buybox":
							asinitem[13]=asinitem[8]
		
					print(asinitem)
			
					ASINILIST[index]=asinitem
				except Exception as  es :
					print(es)
				# self.AddNewSrore(asin[5])
			# print (ASINILIST)
			print (self.postData)
			PJson={'list':self.postData}
			try:
				print(requests.post("https://fulfillment.speedersolutions.com/public/sales-report/asin-review",json=PJson).text)			
			except :pass
			# self.postData.clear()
		
  
		def setEmailText(self):
			title= ["asin" ,"isDoge","name","price","reviewe","storeName","storeId" ,"offers","time","brand","ranks","isbuybox","us","下架时间","上架时间","创建时间"]
			
			titleText="\n ASIN     获取时间   		review  	 卖家id            卖家名字              被跟卖个数  		价格             title\n"
			dogelist ="《变狗asin》 "+titleText
			Normallist ="《未变狗asin》 "+titleText
			NobuyboxList="《Nobuybox asin》 "+titleText
			PutList="《重新上架 asin》 "+titleText
			Currently_unavailableist="《Currently_unavailable asin》 "+titleText
			now_asin=[  asin[0] for asin in ASINILIST]
			print ("=============================")
			print (now_asin)
			print ("=============================")
			dogAsin=[]
			Currently_unavailableist_Asin=[]
			PutAsin=[]
			NormaAsin=[]
			NobuyboxAsin=[]
			for Asin,isDoge,title,price ,reviewe,storeName,storeId ,offers,dTime ,brand,ranks,isbuybox,us,Change_time ,d_time , creat_time in ASINILIST:
				aitm=[Asin,isDoge,title,price ,reviewe,storeName,storeId ,offers,dTime ,brand,ranks,isbuybox,us,Change_time ,d_time ,creat_time]
				dTime=str(dTime)
				isbuybox=str(isbuybox)
				strText=Asin+"  "+dTime+"           "+reviewe+"    " +storeName+ "  "+storeId+"           "+offers+"   " +price+"  "+title+  "      "+brand+"		"+ranks+"		"+us+"		"+Change_time+"			"+ d_time+"\n"
				if isDoge=="True":
					dogAsin.append(aitm)
					dogelist+=strText
				elif str(isbuybox)=="False":
					Normallist +=strText
					NormaAsin.append(aitm)
				else:
					if us=="NoBuybox":
						NobuyboxList += strText
						NobuyboxAsin .append(aitm)
					else:
						Currently_unavailableist+=strText
						Currently_unavailableist_Asin.append(aitm)
				if d_time!="N" and us=="Buybox" and isDoge!="True":
					PutList+=strText
					PutAsin.append(aitm)
		
			dogAsin.sort(key=lambda items: time.strptime(items[8], '%a %b %d %H:%M:%S %Y'),reverse = True)
			PutAsin.sort(key=lambda items: time.strptime(items[14], '%a %b %d %H:%M:%S %Y'))
			Currently_unavailableist_Asin.sort(key=lambda items: time.strptime(items[13], '%a %b %d %H:%M:%S %Y'))
			NobuyboxAsin.sort(key=lambda items: time.strptime(items[13], '%a %b %d %H:%M:%S %Y'))
			for asinItem in PutAsin:
				time_difference='N'
				try:
					if asinItem[14]!='N' and asinItem[13]!='N':
						time_difference =(time.mktime(time.strptime(asinItem[14], '%a %b %d %H:%M:%S %Y'))-time.mktime(time.strptime(asinItem[13], '%a %b %d %H:%M:%S %Y')))/60/60
				except:pass
				asinItem.append(time_difference)
			for it in [PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]:
				it.insert(0,["ASIN","isdoge","title","price","reviewe","storeName","storeId","offers","Crawling time","brand","ranks","isbuybox","us","Change_time","d_time","creat_time"])
			dogAsin.insert(0,["变狗asin",])
			PutAsin.insert(0,["重新上架asin",])
			Currently_unavailableist_Asin.insert(0,["Currently_unavailableist_Asin",])
			NobuyboxAsin.insert(0,["NobuyboxAsin"])
			NormaAsin.insert(0,["正常asin"])
			print("=----------------------------------------------------------")
			[ ASINILIST.append(asin)   for  asin in  getXlsList("st1.xls")[0] if asin[0] not in now_asin ]
			
			setN=	getXlsList("st1.xls")
			setN[0]=ASINILIST
			setScreenXls([ASINILIST,PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin])
			setScreenXls(setN,"st1.xls")	
			# print (len([PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]))
			# print (AsinItemToHtml.toHtml([dogAsin[:2],PutAsin[:3],Currently_unavailableist_Asin[:3],NobuyboxAsin[:3],NormaAsin[:2]]))
			Email("20",AsinItemToHtml.toHtml([dogAsin,PutAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]),keys[-2][0][0])
			# [Email(x,AsinItemToHtml.toHtml([dogAsin,PutAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]),keys[-2][0][0]) for x in keys[-1]]
			# self.closeChrome()
			# os.system("")
			# ssh= paramiko.Transport(("82.156.171.227",22))
			# ssh.connect(username="root", password="1634475170qQ")
			# sftp = paramiko.SFTPClient.from_transport(ssh)
			# sftp.put("st1.xls",'/root/search/File/st1.xls')
		# def findStoreNewAsin(self):s
		def insertItems(self):
			for item in ASINILIST:
				sqlstr='INSERT INTO asinTable VALUES ('
				for asin in item:
					sqlstr+='"'+str(asin).replace('"',"")+'",'
				sqlstr=sqlstr[:-1]
				sqlstr+=")"
				# print (sqlstr)
				try:
					(sqlite().execute(sqlstr))
				except Exception as es:
					print (es)
		def newSpendEmail(self ,BIGtitle):
			title= ["asin" ,"isDoge","name","price","reviewe","storeName","storeId" ,"offers","time","brand","ranks","isbuybox","us","下架时间","上架时间",'creat_time']
			
			titleText="\n ASIN     获取时间   		review  	 卖家id            卖家名字              被跟卖个数  		价格             title\n"
			dogelist ="《变狗asin》 "+titleText
			Normallist ="《未变狗asin》 "+titleText
			NobuyboxList="《Nobuybox asin》 "+titleText
			PutList="《重新上架 asin》 "+titleText
			Currently_unavailableist="《Currently_unavailable asin》 "+titleText
			now_asin=[  asin[0] for asin in ASINILIST]
			print ("=============================")
			print (now_asin)
			print ("=============================")
			dogAsin=[]
			Currently_unavailableist_Asin=[]
			PutAsin=[]
			NormaAsin ,NoDATAASIN=[],[]
   
			NobuyboxAsin=[]
			for Asin,isDoge,title,price ,reviewe,storeName,storeId ,offers,dTime ,brand,ranks,isbuybox,us,Change_time ,d_time ,creat_time in ASINILIST:
				aitm=[Asin,isDoge,title,price ,reviewe,storeName,storeId ,offers,dTime ,brand,ranks,isbuybox,us,Change_time ,d_time,creat_time]
				dTime=str(dTime)
				isbuybox=str(isbuybox)
				strText=Asin+"  "+dTime+"           "+reviewe+"    " +storeName+ "  "+storeId+"           "+offers+"   " +price+"  "+title+  "      "+brand+"		"+ranks+"		"+us+"		"+Change_time+"			"+ d_time+"\n"
				if isDoge=="True":
					dogAsin.append(aitm)
					dogelist+=strText
				elif str(isbuybox)=="False":
					Normallist +=strText
					if creat_time!='N':
						NormaAsin.append(aitm)
					else:
						NoDATAASIN.append(aitm)
						
				else:
					if us=="NoBuybox" :
						NobuyboxList += strText
						NobuyboxAsin .append(aitm)
					else:
						if Change_time!='':
							Currently_unavailableist+=strText
							Currently_unavailableist_Asin.append(aitm)
						if Change_time=='':print(Asin)
				if d_time!="N" and us=="Buybox" and isDoge!="True" and d_time!="" :
					PutAsin.append(aitm)
		
			dogAsin.sort(key=lambda items: time.strptime(items[8], '%a %b %d %H:%M:%S %Y'),reverse = True)
			PutAsin.sort(key=lambda items: time.strptime(items[14], '%a %b %d %H:%M:%S %Y'))
			Currently_unavailableist_Asin.sort(key=lambda items: time.strptime(items[13], '%a %b %d %H:%M:%S %Y'))
			NobuyboxAsin.sort(key=lambda items: time.strptime(items[13], '%a %b %d %H:%M:%S %Y'))
			for asinItem in PutAsin:
				time_difference='N'
				try:
					if asinItem[14]!='N' and asinItem[13]!='N'and asinItem[14]!=''and asinItem[13]!=''  :
						time_difference =(time.mktime(time.strptime(asinItem[14], '%a %b %d %H:%M:%S %Y'))-time.mktime(time.strptime(asinItem[13], '%a %b %d %H:%M:%S %Y')))/60/60
				except:pass
				asinItem.append(time_difference)
			for it in [PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]:
				it.insert(0,["ASIN","isdoge","title","price","reviewe","storeName","storeId","offers","Crawling time","brand","ranks","isbuybox","us","Change_time","d_time",'creat_time'])
			dogAsin.insert(0,["变狗asin",])
			PutAsin.insert(0,["重新上架asin",])
			Currently_unavailableist_Asin.insert(0,["Currently_unavailableist_Asin",])
			NobuyboxAsin.insert(0,["NobuyboxAsin"])
			NormaAsin.insert(0,["正常asin"])
			print("=----------------------------------------------------------")
			newASINS=[]
			oldAsin=re.findall('B0.{8}', requests.get("http://82.156.171.227:5000/FindAll?asin_type=0").text)			
			[ ASINILIST.append([asin,])   for  asin in oldAsin   if asin not in now_asin ]
			[ newASINS.append( asin)   for  asin in ASINILIST   if asin[0] in oldAsin ]
			ASINILIST.clear()
			[ASINILIST.append(asin) for asin in  newASINS]
			setN=	getXlsList("st1.xls")
			setN[0]=ASINILIST
			setScreenXls([ASINILIST,PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin])
			setScreenXls(setN,"st1.xls")	
			# print (len([PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]))
			# print (AsinItemToHtml.toHtml([dogAsin[:2],PutAsin[:3],Currently_unavailableist_Asin[:3],NobuyboxAsin[:3],NormaAsin[:2]]))
			Email("20",AsinItemToHtml.toHtml([dogAsin,PutAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin,NoDATAASIN]),BIGtitle)
			# [Email(x,AsinItemToHtml.toHtml([dogAsin,PutAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]),keys[-2][0][0]) for x in keys[-1]]
			# self.closeChrome()
			os.system("")
			ssh= paramiko.Transport(("82.156.171.227",22))
			ssh.connect(username="root", password="1634475170qQ")
			sftp = paramiko.SFTPClient.from_transport(ssh)
			sftp.put("asin.xls",'/root/search/File/st1.xls')


class Spider1:
	STORESLIST=[]
	FirstStar=True
	ASINS=[]
	DOGELIST=[]
	Zip_code=None
	storeName=[]
	EmailText=""
	postData=[]
	browser =webdriver.Firefox
	def __init__(self ):
			# self.store=[str(s[0]).replace("\xa0"," ") for s in keys[2]]
			# self.Zip_code=random.choice(keys[1])
			self.browser=self.initChrome()
			# self.STORESLIST =keys[0]	
			print ("=================init====================")

	def initChrome(self):
			browser =None
			webdriver.FirefoxProfile()
			profile = webdriver.FirefoxProfile()
			ip,port='tunnel5.qg.net',16588
			# 304504D9:50C3CCDAD815@tunnel5.qg.net:16588
			settings = {
				'network.proxy.type': 1,  # 0: 不使用代理；1: 手动配置代理
				'network.proxy.http': ip,
				'network.proxy.http_port': port,
				'network.proxy.ssl': ip,  # https的网站,
				'network.proxy.ssl_port': port,

			}
			for key, value in settings.items():
				profile.set_preference(key, value)

			profile.set_preference('permissions.default.image', 2)	
			profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

			profile.update_preferences()
			# options = Options()
			# options.set_preference('permissions.default.image',2)
			# return webdriver.Firefox(firefox_profile=profile, options=options)

			# chrome_option.binary_location='D:\\ps\\Chrome-bin\\chrome\\App\\Chrome-bin\\chrome.exe'
			# chrome_option .add_experimental_option("prefs", prefs)
			return webdriver.Firefox(firefox_profile=profile)
	
	
			# return webdriver.Chrome(executable_path="D:\\ps\\Chrome-bin\\chrome\\91.exe",options=chrome_option,)
	def searchDeliver(self):
			try:
				# self.browser.find_elements_by_xpath('//*[@class="a-offscreen"]')

				return self.browser.find_element(By.ID,'deliveryBlockMessage').text
			except:
				return '异常'

	def  setZip_code(self ,zip=19721):
			try:
				self.browser.get("https://www.amazon.com/")
				time.sleep(10)
				if self.browser.page_source.find('e the characters you see in this image:')>0:return 0
				self.browser.find_element(By.ID,"glow-ingress-line1").click()
				time.sleep(10)
				try:
					self.browser.find_element(By.ID,"GLUXChangePostalCodeLink").click()
					time.sleep(4)
					self.browser.find_element(By.ID,'GLUXZipUpdateInput').clear()
					time.sleep(3)
				except Exception as es:pass
				if zip!='19721':
					self.browser.find_element(By.ID,'GLUXZipUpdateInput').send_keys(str(zip))
				else:
					self.browser.find_element(By.ID,'GLUXZipUpdateInput').send_keys(str("80206"))
						
				time.sleep(3)
				self.browser.find_element(By.CSS_SELECTOR,'#GLUXZipUpdate > span > input').click()
				time.sleep(5)
				if self.browser.page_source.find("此邮政编码目前不可用。请关闭此窗口，然后重试。")>0:return 0
				self.browser.refresh()
				# self.browser.find_element('').
				# WebDriverWait(self.browser,10,poll_frequency=1,ignored_exceptions=None)
				# self.browser.set_page_load_timeout(10)

				print ("=================邮政编码成功====================")
				return 1
			except :return 0

	def  parse_AsinHtml(self ,asin):
			isFind= lambda x:x != None and x.group().strip() or "N"
			name=	self.browser.find_element(By.ID,"productTitle").text
			# name=	self.browser.find_elements_by_xpath("productTitle").text
   
			# price=	self.browser.find_element(By.ID,"price_inside_buybox").text
			price = re.search('(?<=a-offscreen">\$).+?(?=</span>)',str(self.browser.page_source ).replace('\n','') )
			price = price != None and price.group().strip().split('"')[0] or 'None'
			p= re.split("a-price a-text-price a-size-medium",str(self.browser.page_source ).replace('\n',''))
			if len(p)>1:
				price = re.search('(?<=a-offscreen">\$).+?(?=</span>)',p[1])
				price = price != None and price.group().strip().split('"')[0] or 'None'
	
				
			# reviewe= len(self.browser.find_elements_by_class_name("a-icon-alt"))>=1 and self.browser.find_element_by_class_name("a-icon-alt").text.replace("out of 5 stars","")  or"N" 
			# revieweNum= len(self.browser.find_elements_by_id("acrCustomerReviewText"))>=1 and self.browser.find_element(By.ID,"acrCustomerReviewText").text.replace(",","")  or"N" 
			reviews = re.search('(?<=title=").{0,5}(?=out of 5 stars)', str(self.browser.page_source ).replace('\n',''))
			reviews = reviews != None and reviews.group().strip() or 0
			s,reviewsNumber= re.split('id="acrCustomerReviewText" class="a-size-base">',str(self.browser.page_source ).replace('\n','')),None
			reviewsNumber = len(s) > 1 and re.split(" ", s[1])[0] or 0		
			print(reviewsNumber)
			print(reviews)

			# {"asin":"B07VGRJDFY","score":0, "commentsNum": 0}
			try:
				if reviewsNumber==0:reviews=0
				self.postData.append({"asin":asin[0],"score":float(reviews), "commentsNum": int(reviewsNumber)})
			except Exception as es: print (es)
			storeName= len(self.browser.find_elements_by_id("sellerProfileTriggerId"))>=1 and	self.browser.find_element(By.ID,"sellerProfileTriggerId").text or "N"
			# storeId= len(self.browser.find_elements_by_id("sellerProfileTriggerId"))>=1 and	self.browser.find_element(By.ID,"sellerProfileTriggerId").get_attribute("href")or "N"
			# s=self.browser.find_element_by_xpath("Best Sellers Rank")
			brand= len(self.browser.find_elements_by_id("bylineInfo"))>=1 and	self.browser.find_element(By.ID,"bylineInfo").text or "N"
			storeId=isFind(re.search('(?<=seller=).+?(?=\&)',str(self.browser.page_source ).replace('\n','') )).split('"')[0]
			offers =re.search('(?<=\().{0,5}(?=\) from)',str(self.browser.page_source ).replace('\n','') )    
			isBuybox=str(self.browser.page_source ).replace('\n','').find("a-box-group")>=1 and  "False"or "True"
			ranks= len(self.browser.find_elements_by_xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()="\nBest Sellers Rank\n"]/following-sibling::td'))>=1 and	self.browser.find_elements_by_xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()="\nBest Sellers Rank\n"]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
			# date= len(self.browser.find_elements_by_link_text(' Date First Available '))>=1 and	self.browser.find_elements_by_link_text(' Date First Available ')[0].text.replace("\n","")or "N"
			offers =offers!=None and offers.group() or '0'
			Currently_unavailable=self.browser.page_source.find("Currently unavailable")>=1 and "True" or "False"
			us= "Buybox"
			if isBuybox=="True" and Currently_unavailable =="True":
				us="无库存"
			elif isBuybox=="True" and Currently_unavailable !="True":
				us="NoBuybox"
			if price == 'None':price=asin[3]
			if storeName == 'N':storeName=asin[5]
			if storeId == 'N':storeId=asin[6]
			# print(self.browser.find_elements_by_tag_name('td'))
			data=self.browser.find_element(By.ID,'productDetails_detailBullets_sections1').text.split('\n')[-1]
			# Date First Available
			if data.find('Date First Available')>=0:data=data.replace('Date First Available','')
			else :data='N'
			# print(data)
			return [asin[0],'False',name ,price ,str(reviews),storeName,storeId,offers,time.asctime( time.localtime(time.time()) ),brand,ranks,isBuybox ,us ,"N" ,"N",data]
	def getAsin(self,asin):
			self.browser.get("https://www.amazon.com/dp/"+asin[0])
			time.sleep(1)
			if self.browser.page_source.find("validateCaptcha")>=0:
				time.sleep(20)
				return self.getAsin(self,asin)
			if self.browser.page_source.find("Sorry! We couldn't find that page. Try searching or go to Amazon's home page.")>=1:
				if len(asin)<2:
					# asin.append("True")
					asin=[asin[0],"True","N","N","N","N","N","N",time.asctime( time.localtime(time.time()) ),"","","","N","N","N"]
				else:
					if asin[1] !="True":
						asin[1]='True'
						asin[8]=time.asctime( time.localtime(time.time()) )
				return asin
			return self.parse_AsinHtml(asin)
	
	def AddNewSrore(self ,storeId):
			# if storeId in self.store:self.store.append(storeId)
			lambda	storeId : storeId not in self.store   and  self.store.append (storeId) (storeId)
	def closeChrome(self):
			self.browser.quit()
		
	def aShoudAsin(self):
			index=0
			for asin in self.STORESLIST :
				# a+=1
				# print (a)
				try:

					asinitem=(self.getAsin(asin))


					if  len(asin)>10:
							# print  (sqlite().execute("INSERT INTO asinTable (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0]))

						if len(asin)==1 :pass

						elif asin[12] ==asinitem[12] :
							asinitem[13]=asin[13]
							asinitem[14]=asin[14] 
						#重新上架asin
						elif asin[12]!="Buybox" and  asinitem[12] =="Buybox":
						#重新上架时间
							asinitem[13]=asin[13]
							asinitem[14]=asinitem[8]
						# 下架时间
						elif asin[12]!=asinitem[12]:
							asinitem[13]=asinitem[8]
							asinitem[14]=asin[14] 
					else:
						if asinitem[12]!="Buybox":
							asinitem[13]=asinitem[8]
		
					print(asinitem)
			
					self.STORESLIST[index]=asinitem
				except Exception as  es :
					print(es)
				index+=1
				# self.AddNewSrore(asin[5])
			print (self.STORESLIST)
		
  
	def newaShoudAsin(self ):
			# for asin in self.STORESLIST :
			while ASINITEMESLIST:
				# a+=1
				# print (ASINITEMESLIST)
				lock1.acquire()
				asin,index=ASINITEMESLIST.pop()
				lock1.release()
				try:

					asinitem=(self.getAsin(asin))
					if  len(asin)>10:
							# print  (sqlite().execute("INSERT INTO asinTable (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0],asinitem[0]))

						if len(asin)==1 :pass
						elif asin[12] ==asinitem[12] :
							asinitem[13]=asin[13]
							asinitem[14]=asin[14] 
						#重新上架asin
						elif asin[12]!="Buybox" and  asinitem[12] =="Buybox":
						#重新上架时间
							asinitem[13]=asin[13]
							asinitem[14]=asinitem[8]
						# 下架时间
						elif asin[12]!=asinitem[12]:
							asinitem[13]=asinitem[8]
							asinitem[14]=asin[14] 
					else:
						if asinitem[12]!="Buybox":
							asinitem[13]=asinitem[8]
		
					print(asinitem)
			
					ASINILIST[index]=asinitem
				except Exception as  es :
					print(es)
				# self.AddNewSrore(asin[5])
			# print (ASINILIST)
			print (self.postData)
			PJson={'list':self.postData}
			try:
				print(requests.post("https://fulfillment.speedersolutions.com/public/sales-report/asin-review",json=PJson).text)			
			except :pass
			# self.postData.clear()
		
  
	def setEmailText(self):
			title= ["asin" ,"isDoge","name","price","reviewe","storeName","storeId" ,"offers","time","brand","ranks","isbuybox","us","下架时间","上架时间","创建时间"]
			
			titleText="\n ASIN     获取时间   		review  	 卖家id            卖家名字              被跟卖个数  		价格             title\n"
			dogelist ="《变狗asin》 "+titleText
			Normallist ="《未变狗asin》 "+titleText
			NobuyboxList="《Nobuybox asin》 "+titleText
			PutList="《重新上架 asin》 "+titleText
			Currently_unavailableist="《Currently_unavailable asin》 "+titleText
			now_asin=[  asin[0] for asin in ASINILIST]
			print ("=============================")
			print (now_asin)
			print ("=============================")
			dogAsin=[]
			Currently_unavailableist_Asin=[]
			PutAsin=[]
			NormaAsin=[]
			NobuyboxAsin=[]
			for Asin,isDoge,title,price ,reviewe,storeName,storeId ,offers,dTime ,brand,ranks,isbuybox,us,Change_time ,d_time , creat_time in ASINILIST:
				aitm=[Asin,isDoge,title,price ,reviewe,storeName,storeId ,offers,dTime ,brand,ranks,isbuybox,us,Change_time ,d_time ,creat_time]
				dTime=str(dTime)
				isbuybox=str(isbuybox)
				strText=Asin+"  "+dTime+"           "+reviewe+"    " +storeName+ "  "+storeId+"           "+offers+"   " +price+"  "+title+  "      "+brand+"		"+ranks+"		"+us+"		"+Change_time+"			"+ d_time+"\n"
				if isDoge=="True":
					dogAsin.append(aitm)
					dogelist+=strText
				elif str(isbuybox)=="False":
					Normallist +=strText
					NormaAsin.append(aitm)
				else:
					if us=="NoBuybox":
						NobuyboxList += strText
						NobuyboxAsin .append(aitm)
					else:
						Currently_unavailableist+=strText
						Currently_unavailableist_Asin.append(aitm)
				if d_time!="N" and us=="Buybox" and isDoge!="True":
					PutList+=strText
					PutAsin.append(aitm)
		
			dogAsin.sort(key=lambda items: time.strptime(items[8], '%a %b %d %H:%M:%S %Y'),reverse = True)
			PutAsin.sort(key=lambda items: time.strptime(items[14], '%a %b %d %H:%M:%S %Y'))
			Currently_unavailableist_Asin.sort(key=lambda items: time.strptime(items[13], '%a %b %d %H:%M:%S %Y'))
			NobuyboxAsin.sort(key=lambda items: time.strptime(items[13], '%a %b %d %H:%M:%S %Y'))
			for asinItem in PutAsin:
				time_difference='N'
				try:
					if asinItem[14]!='N' and asinItem[13]!='N':
						time_difference =(time.mktime(time.strptime(asinItem[14], '%a %b %d %H:%M:%S %Y'))-time.mktime(time.strptime(asinItem[13], '%a %b %d %H:%M:%S %Y')))/60/60
				except:pass
				asinItem.append(time_difference)
			for it in [PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]:
				it.insert(0,["ASIN","isdoge","title","price","reviewe","storeName","storeId","offers","Crawling time","brand","ranks","isbuybox","us","Change_time","d_time","creat_time"])
			dogAsin.insert(0,["变狗asin",])
			PutAsin.insert(0,["重新上架asin",])
			Currently_unavailableist_Asin.insert(0,["Currently_unavailableist_Asin",])
			NobuyboxAsin.insert(0,["NobuyboxAsin"])
			NormaAsin.insert(0,["正常asin"])
			print("=----------------------------------------------------------")
			[ ASINILIST.append(asin)   for  asin in  getXlsList("st1.xls")[0] if asin[0] not in now_asin ]
			
			setN=	getXlsList("st1.xls")
			setN[0]=ASINILIST
			setScreenXls([ASINILIST,PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin])
			setScreenXls(setN,"st1.xls")	
			# print (len([PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]))
			# print (AsinItemToHtml.toHtml([dogAsin[:2],PutAsin[:3],Currently_unavailableist_Asin[:3],NobuyboxAsin[:3],NormaAsin[:2]]))
			Email("20",AsinItemToHtml.toHtml([dogAsin,PutAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]),keys[-2][0][0])
			# [Email(x,AsinItemToHtml.toHtml([dogAsin,PutAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]),keys[-2][0][0]) for x in keys[-1]]
			# self.closeChrome()
			# os.system("")
			# ssh= paramiko.Transport(("82.156.171.227",22))
			# ssh.connect(username="root", password="1634475170qQ")
			# sftp = paramiko.SFTPClient.from_transport(ssh)
			# sftp.put("st1.xls",'/root/search/File/st1.xls')
		# def findStoreNewAsin(self):s
	def insertItems(self):
			for item in ASINILIST:
				sqlstr='INSERT INTO asinTable VALUES ('
				for asin in item:
					sqlstr+='"'+str(asin).replace('"',"")+'",'
				sqlstr=sqlstr[:-1]
				sqlstr+=")"
				# print (sqlstr)
				try:
					(sqlite().execute(sqlstr))
				except Exception as es:
					print (es)
	def newSpendEmail(self ,BIGtitle):
			title= ["asin" ,"isDoge","name","price","reviewe","storeName","storeId" ,"offers","time","brand","ranks","isbuybox","us","下架时间","上架时间",'creat_time']
			
			titleText="\n ASIN     获取时间   		review  	 卖家id            卖家名字              被跟卖个数  		价格             title\n"
			dogelist ="《变狗asin》 "+titleText
			Normallist ="《未变狗asin》 "+titleText
			NobuyboxList="《Nobuybox asin》 "+titleText
			PutList="《重新上架 asin》 "+titleText
			Currently_unavailableist="《Currently_unavailable asin》 "+titleText
			now_asin=[  asin[0] for asin in ASINILIST]
			print ("=============================")
			print (now_asin)
			print ("=============================")
			dogAsin=[]
			Currently_unavailableist_Asin=[]
			PutAsin=[]
			NormaAsin ,NoDATAASIN=[],[]
   
			NobuyboxAsin=[]
			for Asin,isDoge,title,price ,reviewe,storeName,storeId ,offers,dTime ,brand,ranks,isbuybox,us,Change_time ,d_time ,creat_time in ASINILIST:
				aitm=[Asin,isDoge,title,price ,reviewe,storeName,storeId ,offers,dTime ,brand,ranks,isbuybox,us,Change_time ,d_time,creat_time]
				dTime=str(dTime)
				isbuybox=str(isbuybox)
				strText=Asin+"  "+dTime+"           "+reviewe+"    " +storeName+ "  "+storeId+"           "+offers+"   " +price+"  "+title+  "      "+brand+"		"+ranks+"		"+us+"		"+Change_time+"			"+ d_time+"\n"
				if isDoge=="True":
					dogAsin.append(aitm)
					dogelist+=strText
				elif str(isbuybox)=="False":
					Normallist +=strText
					if creat_time!='N':
						NormaAsin.append(aitm)
					else:
						NoDATAASIN.append(aitm)
						
				else:
					if us=="NoBuybox" :
						NobuyboxList += strText
						NobuyboxAsin .append(aitm)
					else:
						if Change_time!='':
							Currently_unavailableist+=strText
							Currently_unavailableist_Asin.append(aitm)
						if Change_time=='':print(Asin)
				if d_time!="N" and us=="Buybox" and isDoge!="True" and d_time!="" :
					PutAsin.append(aitm)
		
			dogAsin.sort(key=lambda items: time.strptime(items[8], '%a %b %d %H:%M:%S %Y'),reverse = True)
			PutAsin.sort(key=lambda items: time.strptime(items[14], '%a %b %d %H:%M:%S %Y'))
			Currently_unavailableist_Asin.sort(key=lambda items: time.strptime(items[13], '%a %b %d %H:%M:%S %Y'))
			NobuyboxAsin.sort(key=lambda items: time.strptime(items[13], '%a %b %d %H:%M:%S %Y'))
			for asinItem in PutAsin:
				time_difference='N'
				try:
					if asinItem[14]!='N' and asinItem[13]!='N'and asinItem[14]!=''and asinItem[13]!=''  :
						time_difference =(time.mktime(time.strptime(asinItem[14], '%a %b %d %H:%M:%S %Y'))-time.mktime(time.strptime(asinItem[13], '%a %b %d %H:%M:%S %Y')))/60/60
				except:pass
				asinItem.append(time_difference)
			for it in [PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]:
				it.insert(0,["ASIN","isdoge","title","price","reviewe","storeName","storeId","offers","Crawling time","brand","ranks","isbuybox","us","Change_time","d_time",'creat_time'])
			dogAsin.insert(0,["变狗asin",])
			PutAsin.insert(0,["重新上架asin",])
			Currently_unavailableist_Asin.insert(0,["Currently_unavailableist_Asin",])
			NobuyboxAsin.insert(0,["NobuyboxAsin"])
			NormaAsin.insert(0,["正常asin"])
			print("=----------------------------------------------------------")
			newASINS=[]
			oldAsin=re.findall('B0.{8}', requests.get("http://82.156.171.227:5000/FindAll?asin_type=0").text)			
			[ ASINILIST.append([asin,])   for  asin in oldAsin   if asin not in now_asin ]
			[ newASINS.append( asin)   for  asin in ASINILIST   if asin[0] in oldAsin ]
			ASINILIST.clear()
			[ASINILIST.append(asin) for asin in  newASINS]
			setN=	getXlsList("st1.xls")
			setN[0]=ASINILIST
			setScreenXls([ASINILIST,PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin])
			setScreenXls(setN,"st1.xls")	
			# print (len([PutAsin,dogAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]))
			# print (AsinItemToHtml.toHtml([dogAsin[:2],PutAsin[:3],Currently_unavailableist_Asin[:3],NobuyboxAsin[:3],NormaAsin[:2]]))
			Email("20",AsinItemToHtml.toHtml([dogAsin,PutAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin,NoDATAASIN]),BIGtitle)
			# [Email(x,AsinItemToHtml.toHtml([dogAsin,PutAsin,Currently_unavailableist_Asin,NobuyboxAsin,NormaAsin]),keys[-2][0][0]) for x in keys[-1]]
			# self.closeChrome()
			os.system("")
			ssh= paramiko.Transport(("82.156.171.227",22))
			ssh.connect(username="root", password="1634475170qQ")
			sftp = paramiko.SFTPClient.from_transport(ssh)
			sftp.put("asin.xls",'/root/search/File/st1.xls')



