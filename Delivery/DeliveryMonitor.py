# -*- coding: utf-8 -*-
# import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.firefox.options import Options
import time ,re, os,datetime,sys ,random 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By

if sys.version_info[0] < 3:
	reload(sys)
	sys.setdefaultencoding('utf8')
from selenium.webdriver.common.action_chains import ActionChains

import requests,zipfile,AsinItemToHtml ,threading
# from yaml import KeyToken
from PostEmail import Email,EmailS ,EmailNECR	
from FindByHtml import findUpcByHtml,find_offers,find_offers
from selenium.webdriver.support.ui import WebDriverWait
from spider import Spider,Spider1
from keepaG import search_data_bykeepaApi
from update import setScreenXls,readFile,getXlsList,setScreenXlsAsin,setScreenXlsa
STORESLIST=[]
PDATA=[]
# D_Pool= multiprocessing.Pool(4)
DATADIC={
	"January":1,
	"February":2,	
	"March":3,	
	"April":4,	
	"May":5,	
	"June":6,	
	"July":7 ,	
	"August":8,	
	"Sep":9,
	"September":9,	
 	'Oct':10,
	"October":10,	
	"November":11,	
	"December":12,	
 
}



CHROME_PROXY_HELPER_DIR = 'Chrome-proxy-helper'
# 存储自定义Chrome代理扩展文件的目录
CUSTOM_CHROME_PROXY_EXTENSIONS_DIR = 'chrome-proxy-extensions'
EMAILNAME='Delivery监控'
SELLERLIST=[ """"""]
InvalidZipLIST=[]
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



def getAsin(browser,asin ):
	b=0
	while True:
		try:
			if b>0:
				browser.refresh()
			else:browser.get("https://www.amazon.com/dp/"+asin)
			b+=1
			time.sleep(1)	
				# browser.get("https://www.amazon.com/dp/B0B65GKJCP")
			of= findUpcByHtml(browser.page_source,"","")	
			if browser.page_source.find('Type the characters you see in this image:')>=0:
				print ('s=======')
				time.sleep(1)	
				continue
			if browser.page_source.find("Amazon.com Page Not Found")>1 or browser.page_source.find(" Page Not Found")>1:
				break
			# print (of[3])
			# if of[3]=='None':continue
			break
		except:
				print ('======wait======')
				time.sleep(1)
	return of

def getWebbYs(code,Asins,seller_List ,retQty):
	print (Asins)
	global EMAILNAME
	asinItems=[]
	while True:	
		cw=Spider(1)
		# cw.setkeepa()
		retZip=cw.setZip_code(code)
		if 	retZip==0:
			cw.closeChrome()
			continue
		break
		
	browser =cw.browser
		# browser = webdriver.Chrome(executable_path="101\\chromedriver.exe",options=chrome_option,)
				# WebDriverWait(browser,10,poll_frequency=1,ignored_exceptions=None)
				# browser.set_page_load_timeout(10)
	
	for asin in Asins[1:]:
		nm=''
		getAsin(browser , asin[0])
		isFind= lambda x:x != None and x.group().strip() or "N"
		if browser.page_source.find("Amazon.com Page Not Found")>1 or browser.page_source.find(" Page Not Found")>1:
			continue
							# rl=find_offers(browser.page_source)
		if len(browser.find_elements(By.XPATH,"//*[@id='newer-version']/div//a"))>0 :
    							# key.append(browser.find_elements(By.XPATH,"//*[@id='newer-version']/div//a")[0].get_attribute('href').split('/')[5])
			nm=browser.find_elements(By.XPATH,"//*[@id='newer-version']/div//a")[0].get_attribute('href')
			nmasin = nm.split('/')[5]
		title=''
		price ,Deliver ,BuyBox,Sellers  ,Shipsfrom,Soldby='','',True,'','',''

		isFBA,IsO	 ,IsFromAmazon =True,False,False
		isBaseAsin=False
		baseAsin=''
		try:
			# if len( browser.find_elements(By.ID,"prodDetails"))>=1:
				# baseAsin=browser.find_element(By.ID,'prodDetails').text
			# baseAsin=re.search(' B0.{8}',baseAsin).group()
			# if baseAsin.find(asin[0])>=0:isBaseAsin=True

			of= findUpcByHtml(browser.page_source,"","")	
			price= isFind(re.search('(?<=class="a-offscreen">\$).{0,8}(?=<)',browser.page_source ))
			print (browser.title)

				# price= isFind(re.search('(?<=">\$).{0,8}(?=<)',browser.page_source.split('<div class="a-box-inner">')[1] ))
			title =browser.title
			# price =len( browser.find_elements(By.XPATH,'//*[@class="a-offscreen"]'))>=1 and browser.find_element(By.XPATH,('//*[@class="a-offscreen"]').text or "N"
			Soldby= len( browser.find_elements(By.ID,"sellerProfileTriggerId"))>=1 and browser.find_element(By.ID,"sellerProfileTriggerId").text or "N"
			Shipsfrom =len( browser.find_elements(By.ID,"tabular-buybox"))>=1 and browser.find_element(By.ID,"tabular-buybox").text or "N"
			Shipsfrom=Shipsfrom.replace('Shipsfrom','').split('Sold by')[0].replace(' ','').replace('\n','')
			Shipsfrom=Shipsfrom.replace('Shipsfrom','')
			if Soldby!='N'  :
				BuyBox=Soldby
			elif  Shipsfrom!="N":
				BuyBox =Shipsfrom
			else :
				price=0
				if title=='None':
					BuyBox='erro'
				else:
					BuyBox ='No BB'
			timeStr=''
			stock=0
			Deliver=cw.searchDeliver()

			if Deliver!='异常'  and False:
				# stock=len( browser.find_elements_by_class_name('a-dropdown-item'))
				try:
					browser.find_elements(By.XPATH,'//*[@title="Add to Shopping Cart"]')[0].click()
					time.sleep(1)
					b=0
					while b < 10:
						if browser.current_url.find('cart')>0:break
						try:
							# if browser.page_source.find('')
							if browser.page_source.find('Buy used')>=0 or browser.page_source.find('Buy new')>=0 :
								browser.execute_script("""document.getElementById('attachSiNoCoverage-announce').click() """)
							else:
								browser.execute_script("""document.getElementById('attachSiNoCoverage-announce').click() """)
						except:pass
						# if browser.page_source.find('Buy used')<=0 or browser.page_source.find('Buy new')<=0 :break
						time.sleep(0.5)
						b+=1
						# try:
							# browser.execute_script("""document.getElementById('attachSiNoCoverage-announce').click() """)
							# 	# browser.find_elements(By.XPATH,'//*[@id="attach-popover-lgtbox"]')[0].click()
							# break
						# except:print ('sleep')
					time.sleep(1)
					browser.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')

					# browser.execute_script(axjx.axjx)
					browser.execute_script("""
					
						var script = document.createElement('script');
						script.src = "https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.js";
						document.getElementsByTagName('head')[0].appendChild(script);
									""")
					time.sleep(1)
					isrun=False
					stockumb=0
					while stockumb < 20:
						if browser.find_element(By.ID,'twotabsearchtextbox').get_attribute('name')!='field-keywords':break
						try:
							# if browser.page_source.find('')
							if isrun==False:
								browser.execute_script (axjx.getQty)
							isrun=True
						except:pass
						stockumb+=1
						time.sleep(0.3)

					stock=browser.find_element(By.ID,'twotabsearchtextbox').get_attribute('name')
					Deumb=0
					be=browser.find_elements(By.XPATH,'//*[@value="Delete"]')[0]
					while True:
						try:
							ActionChains(browser).move_to_element(be).perform()
							time.sleep(0.3)
							
							browser.find_elements(By.XPATH,'//*[@value="Delete"]')[0].click()
							break
						except Exception as es :
							print (es)
							time.sleep(0.5)
							Deumb+=1
					time.sleep(1)
				except Exception as ex:print (ex)
			else:stock='限量商品'
			try:
				print (Deliver)


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
					timeStr='2023/'+str(DATADIC[month])+"/"+day
			except Exception as es:
				print(es)
				timeStr=''
			if browser.page_source.find("We don't know when or if this item will be back in stock.")>1:
				Deliver='无库存'
			if False:
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
			
			ss=[]
			ss1=[]
			if True:
				brand, model, seller='','',''
				seller =len( browser.find_elements(By.ID,"tabular-buybox"))>=1 and browser.find_element(By.ID,"tabular-buybox").text or "N"
				
				model=len(browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Item model number "]/following-sibling::td'))>=1 and	browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Item model number "]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
				brand=len(browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Manufacturer "]/following-sibling::td'))>=1 and	browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Manufacturer "]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
				DFA=len(browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Date First Available "]/following-sibling::td'))>=1 and	browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Date First Available "]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
				ranks= len(browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Best Sellers Rank "]/following-sibling::td'))>=1 and	browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Best Sellers Rank "]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
				s=[]
				if ranks!='N':
							for r in ranks.split('#')[1:]:
								s.append(r.split(' in ')[0])
								s.append(r.split(' in ')[1])
				dataidxintoggleswatchlist=[]
				# browser.find_element('').
				for ke in browser.find_elements(By.XPATH,'//li[@data-idxintoggleswatchlist]'):
					dataidxintoggleswatchlist.append(ke.get_attribute('data-asin='))
				ss1=	[brand, model, seller,]+[DFA,]+dataidxintoggleswatchlist+s
			if   nm!='':
			# if True:
				# nmasin=''
				bs= getAsin(browser, nmasin)
				brand, model, seller='','',''
				seller =len( browser.find_elements(By.ID,"tabular-buybox"))>=1 and browser.find_element(By.ID,"tabular-buybox").text or "N"
				
				model=len(browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Item model number "]/following-sibling::td'))>=1 and	browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Item model number "]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
				brand=len(browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Manufacturer "]/following-sibling::td'))>=1 and	browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Manufacturer "]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
				DFA=len(browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Date First Available "]/following-sibling::td'))>=1 and	browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Date First Available "]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
				ranks= len(browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Best Sellers Rank "]/following-sibling::td'))>=1 and	browser.find_elements(By.XPATH,'//*[@id="productDetails_detailBullets_sections1"]/tbody/tr/th[text()=" Best Sellers Rank "]/following-sibling::td')[0].text.replace("\n","").replace("(See Top 100 in Video Games)","") or "N"
				s=[]
				if ranks!='N':
							for r in ranks.split('#')[1:]:
								s.append(r.split(' in ')[0])
								s.append(r.split(' in ')[1])
				dataidxintoggleswatchlist=[]
				# browser.find_element('').
				for ke in browser.find_elements(By.XPATH,'//li[@data-idxintoggleswatchlist]'):
					dataidxintoggleswatchlist.append(ke.get_attribute('data-asin='))
				ss=	[nmasin,bs[3],bs[4],brand, model, seller,]+[DFA,]+dataidxintoggleswatchlist+s
				# ss=	[brand, model, seller,]+[DFA,]+dataidxintoggleswatchlist+s

				# ss=s
				# print(ss)
				# search_data_bykeepaApi(asin[0]) search_data_bykeepaApi(asin[0]) +
			asinItems.append(
				[asin[0],title,price,Deliver,timeStr,asin[6],BuyBox ,Soldby,asin[8],stock]+search_data_bykeepaApi(asin[0])+ss1+ss)
		except Exception as ex:
			print (ex)
	browser.quit()	
	asinItems.insert(0,['asin','title','价格','预计到货时间','最快到货时间','昨天buybox','buybox','Shipsfrom','operator','库存' ,'Asin','亚马逊最近有货日期','最近3个月是否有货'
	,'最近有货3个月最好的rank','时间','','售价','最近有货2周最好的rank','时间','','售价','amz offer 30D','amz offer 60D','amz offer 90D',"amz offer 180D","amz offer 360D",'asin','title','price','brand','model','ships from sold by','opendate','rank1','category','rank2','category'
])
	return asinItems
			# getWebbYs(page,keys)
   # ['641741859@qq.com','1517496767@qq.com','1634475170@qq.com',"78845417@qq.com","1192373460@qq.com","10098591@qq.com","70354857@qq.com"]

def chRef(ret,code_List):
	mainItem=ret[0]
	nCode_list=[   code  for  code in code_List if code not in InvalidZipLIST]
	for l in range(len(ret[0])):
		for code in range(len( nCode_list)):
			mainItem[l].append( ret[code][l][4])
		# mainItem[l].append(cTime(mainItem[l]))
	return  mainItem
def cTime(Deliver_Time_list):
	a=0
	for DeTi in Deliver_Time_list[12:]:
		if DeTi.find('/')<=0:continue
		try:
			day=(time.time()-(time.mktime( time.strptime(DeTi,'%Y/%m/%d'))) ) // (3600 * 24) 
			if abs(day)>=abs(7):a+=1
		except:pass
	return a== len(Deliver_Time_list[12:]) 

def RetDdliveryBycode(code_List ,Asin_List,seller_List ,retQty ,emailTitle):
	ret =[]
	# Asins=re.findall('B0.{8}', requests.get("http://82.156.171.227:5000/FindAll?asin_type=3").text)	
	# Asins=[asin[0] for asin in Asin_List ]
	# Asins=['B08L619MRF','B083SC5G87']
	# code=code.replace('\n','')
	retItem=getWebbYs(code_List[0] ,Asin_List,seller_List,retQty)
	# if retItem==None:continue
	ret.append(retItem)
	# ret=getXlsList("Tasin.xls")
	# ret[0]	=chRef(ret,code_List)
	print (ret)
	p=getXlsList("FBA.xls")
	p[4]=retItem[1:]
	setScreenXls(p,"FBA.xls")	
	setScreenXls(ret,"asin.xls")	
	# print ('BB 监控')emailTitle
	Email("monitor@hzallin.com",AsinItemToHtml.toHtml(	ret),emailTitle)
	Email("2896747059@qq.com",AsinItemToHtml.toHtml(	ret),emailTitle)

	ret.clear()
	# Email("monitor@hzallin.com",AsinItemToHtml.toHtml(ret),'FBA-SFP 监控')
	# Email("641741859@qq.com",AsinItemToHtml.toHtml(ret),'BB监控')
#  
# def StartJob():
	# RetDdliveryBycode()
def starByJob (scheduler  ,Asin_List ,code_list ,seller_List  , hour, minute  ,emailTitle):
	# scheduler.a
	if  scheduler==None:
		RetDdliveryBycode(code_list, Asin_List , seller_List,True ,emailTitle)
		return
	if len(code_list)<6:
		scheduler.add_job(RetDdliveryBycode, 'cron', hour =hour,minute=minute, id=emailTitle+'cr',args=[ code_list ,Asin_List,seller_List,True ,emailTitle])
		return
	retQty =True
	if len(code_list)<100:
		for cdk in range( int(len(code_list)/4)+1):
			# print (cdk)
			if (cdk+1)*4 >len(code_list):ud=code_list[cdk*4:] 
			else: ud=code_list[cdk*4:(cdk+1)*4] 
			print ((cdk+1)*4)
			scheduler.add_job(RetDdliveryBycode, 'cron', hour =hour,minute=minute, id=emailTitle+str(cdk),args=[ ud ,Asin_List,seller_List,retQty ,emailTitle])
			retQty=False
	else:
		lens=int(len(code_list)/4)
		for cdk in range(4):
			if lens*(cdk+1) >len(code_list):ud=code_list[lens*cdk:] 
			else:
				ud=code_list[lens*cdk:lens*(cdk+1)  ]
			print (lens*(cdk+1))
			# print (ud)
			scheduler.add_job(RetDdliveryBycode, 'cron', hour =hour,minute=minute, id=emailTitle+str(cdk),args=[ ud ,Asin_List,seller_List,False ,emailTitle ])



def run():

	if True :
		print('run')
		RetDdliveryBycode(['19720'],getXlsList("FBA.xls")[-1],seller_List,False,'BB 监控')
		# RetDdliveryBycode(['08733'],getXlsList("FBA.xls")[0],seller_List,False,'EOL 监控')

		# print('=-====')
		print(	'end')
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
	# loop = asyncio.get_event_loop()

	scheduler = BlockingScheduler()
	Asin_List=getXlsList("FBA.xls")[0]
	keys=['08733','92376','77423','61611']
	# keys=['08733',]
	# LL1Asins ,ll1zip=getXlsList("3.xls")
	# keys=getXlsList("FBA.xls")[2]
	# keys=[ str(zip[0]).replace('.0','') for zip in keys ]
		# seller_List=getXlsList("FBA.xls")[2]
	# keys=open('init','r').readlines()

	# D_Pool.apply_async()
	# ret[0]	=chRef(ret,keys)
	# setScreenXls(ret,"asinb.xls")	 

	# print (LL1Asins)
	# print (ll1zip)
	
#400zip
	# starByJob(scheduler , LL1Asins,[ str(zip[0]).replace('.0','') for zip in ll1zip],seller_List,7,30,'400+ zip')
 
#BB监控
	# run()
	scheduler.add_job(run, 'cron', hour =1,minute=1	, id='2',)
	# asyncio.run(run())
	# RetDdliveryBycode(['08733'],getXlsList("FBA.xls")[4],seller_List,False,'BB 监控')
	# starByJob(scheduler , getXlsList("FBA.xls")[4],['08733'],seller_List,8,30,'BB 监控')
	
	# keys=[ str(zip[0]).replace('.0','') for zip in ll1zip ]
#AP每日监控 
	# starByJob(None , getXlsList("FBA.xls")[0],['08733','92376','77423','61611'],seller_List,12,55 ,'FBA-SFP 监控')
#LL 每日监控
	# starByJob(scheduler , LL1Asins,keys,seller_List,11,30 )
	# starByJob(scheduler , getXlsList("FBA.xls")[1],[ str(zip[0]).replace('.0','') for zip in getXlsList("FBA.xls")[2] ],seller_List,18,15 ,'LL FBA-SFP 监控')
	# starByJob(None , Asin_List,keys,seller_List,18,0 )
	scheduler.start()
	# 
 
	# retQty =True
	# for cdk in range( int(len(keys)/4)+1):
	# 	# print (cdk)
	# 	if (cdk+1)*4 >len(keys):ud=keys[cdk*4:] 
	# 	else: ud=keys[cdk*4:(cdk+1)*4] 
	# 	print ((cdk+1)*4)
	# 	scheduler.add_job(RetDdliveryBycode, 'cron', hour =22,minute=15, id=str(cdk),args=[ ud ,Asin_List,seller_List,retQty ])
	# 	retQty=False
 	# time.sleep(60*60*8)
	# RetDdliveryBycode( keys ,Asin_List,seller_List)
	# scheduler.add_job(RetDdliveryBycode, 'cron', hour =4,minute=0, id='test_job2',args=[ keys ,Asin_List,seller_List ,retQty])
	# scheduler.add_job(RetDdliveryBycode, 'cron', hour =17,minute=0, id='test_job1',args=[ keys ,Asin_List,seller_List])

 

		