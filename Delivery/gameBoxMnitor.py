# -*- coding: utf-8 -*-
# import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.chrome.service import Service
import time ,re, os,datetime,sys ,random ,paramiko
import requests,zipfile,AsinItemToHtml
from PostEmail import Email,EmailS ,EmailNECR	
from FindByHtml import findUpcByHtml,find_offers,find_offers
from update import setScreenXls,readFile,getXlsList,setScreenXlsAsin,setScreenXlsa
STORESLIST=[]

CHROME_PROXY_HELPER_DIR = 'Chrome-proxy-helper'
# 存储自定义Chrome代理扩展文件的目录
CUSTOM_CHROME_PROXY_EXTENSIONS_DIR = 'chrome-proxy-extensions'

def  setZip_code(browser):
	try:
		browser.get("https://www.amazon.com/")
		time.sleep(10)
		browser.find_element_by_id("glow-ingress-line1").click()
		time.sleep(10)
		try:
			browser.find_element_by_id("GLUXChangePostalCodeLink").click()
			time.sleep(4)
			browser.find_element_by_id('GLUXZipUpdateInput').clear()
			time.sleep(3)
		except Exception as es:pass
		browser.find_element_by_id('GLUXZipUpdateInput').send_keys(str("90680"))
		time.sleep(3)
		browser.find_element_by_css_selector('#GLUXZipUpdate > span > input').click()
		time.sleep(5)
		browser.refresh()
		print ("=================设置邮编成功====================")
		return 1
	except :return 0


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




def getWebbYs(keys):
	sc=[str(s[0]).replace("\xa0"," ") for s in keys[2]]
	bs=random.choice(keys[1])
	STORESLIST=[[],[],[],[],[],[]]
	bb=[]
	ba=[]
	NotFind=[]
	# for bs in keys[1]:
	if True:
			# asins=[]
		asins=[]
		page= 5
		url='https://www.amazon.com/'
		chrome_option = Options()
		chrome_option.add_argument('--no-sandbox')
		# chrome_option.add_argument('--disable-dev-shm-usage')
		# chrome_option.add_argument('--headless')
		chrome_option.add_argument('--disable-gpu')
		# chrome_option.add_argument('--ignore-certificate-errors')
		chrome_option.add_argument('--disable-dev-shm-usage')
		chrome_option.add_argument('window-size=1920x1080');
		# chrome_option.add_argument("--proxy-server=http://47.98.118.113:16818")
		# chrome_option.add_argument("--proxy-server=tunnel.qg.net:14027")
		chrome_option.add_extension(get_chrome_proxy_extension(proxy='6637554A:1B5A52BB43DD@tunnel.qg.net:14027'))
		# proxy='http://t13281769853377:rohbyz4t@tps115.kdlapi.com:15818'
		# chrome_option.set_capability(CapabilityType.ACCEPT_INSECURE_CERTS, true)
		Av=	webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
  
		# Av['proxy']={
   
		# 	"httpProxy":proxy,
		# 	"ftpProxy":proxy,
		# 	"sslProxy":proxy,
		# 	"noProxy":None,
		# 	"proxyType":"MANUAL",
		# 	"class":"org.openqa.selenium.Proxy",
		# 	"autodetect":False,
	
		# }
		# chrome_option.to_capabilities
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
		# if  True:
				
			browser = webdriver.Chrome(executable_path="chromedriver.exe",options=chrome_option,desired_capabilities=Av)
				# browser.set_window_size(1920,1080) 
			browser.get(url)
			print('get')
			time.sleep(10)  
			if True:
				if True:
						browser.find_element_by_id("glow-ingress-line1").click()
						time.sleep(10)
						try:	
							browser.find_element_by_id("GLUXChangePostalCodeLink").click()
							time.sleep(4)
							browser.find_element_by_id('GLUXZipUpdateInput').clear()
							time.sleep(3)
						except Exception as es:pass
						# print(type(bs))sssssssssssssssss
						browser.find_element_by_id('GLUXZipUpdateInput').send_keys(str(bs[0]))
						time.sleep(3)
						browser.find_element_by_css_selector('#GLUXZipUpdate > span > input').click()
						time.sleep(5)
						browser.refresh()
						time.sleep(5)
						# browser.find_element_by_id('twotabsearchtextbox').send_keys(key[2])
						# browser.find_element_by_css_selector('#nav-search-submit-text > input').click()
						# time.sleep(2)   
				dog =""
				print ("-------------------------------------------------------------------------")
				lowRank="\n"
    
				sft=[]
				for key in keys[0]:
					try:
						# if key[7] !="Currently unavailable" and key[8]!="Your question might be":

							browser.get("https://www.amazon.com/dp/"+key[0])
							# browser.get("https://www.amazon.com/gp/aod/ajax/ref=dp_aod_ALL_mbc?asin="+key[0]+"&m=&pinnedofferhash=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=")
							time.sleep(1)
							# rl=find_offers(browser.page_source)
							if browser.page_source.find("Sorry! We couldn't find that page. Try searching or go to Amazon's home page.")>=1:
								# print ('1')
								dog+=key[0]+"\n"
								if len(key)==1:
									key.append("N")
									key.append(time.asctime( time.localtime(time.time())))
								if len(key)==2:
									key.append(time.asctime( time.localtime(time.time())))
								elif key[2]=="":
									key[2]=(time.asctime( time.localtime(time.time())))
								STORESLIST[3].append(key)
								print (key)	
        
								STORESLIST[4].append([key[0],key[1]])
								sft.append(key)
								continue
							
							of= findUpcByHtml(browser.page_source,"","")	
							sft.append([key[0],of[3]])
       
							STORESLIST[4].append([key[0],of[3]])
							# browser.st
							isBuybox='buybox'
							if of[1]==-1:
								if browser.page_source.find("Currently unavailable")>=1:
									bb.append([key[0],"无库存",[],[],of ])
									isBuybox="无库存"
									# continue
								else:
									bb.append([key[0],"NoBuyBox",[],[],of])
									isBuybox="NoBuyBox"
         
 							# elif of[14]!=0:
								#  of[15] not in sc and 
							browser.get("https://www.amazon.com/gp/aod/ajax/ref=dp_aod_ALL_mbc?asin="+key[0]+"&m=&pinnedofferhash=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=")
							time.sleep(1)
							bb.append([key[0],False,find_offers(browser.page_source),of[5],of])
							if float(of[5])<3 and float(of[5])!=0 :
								STORESLIST[2].append([key[0],of[3],isBuybox])
								lowRank+=key[0]+"\n "
								ba.append(key[0])
						# STORESLIST.append(key)
					except Exception as es:
						print (es)
				# print asins
				print (bb)
				print(STORESLIST)

				if bb!=[] or ba!=[] or STORESLIST[3]!=[]:
					NoBuybox ,ob ,dvbv ,dogs='《掉Buy Box》 \n ASIN      title\n','《被跟卖》 \n ASIN      被跟卖个数     卖家id           卖家名字              review               title\n',"差评商品","《变狗》\n"
					dof='《未下库存》 \n ASIN      被跟卖个数     卖家id           卖家名字              review               title\n'
					Currently_unavailable='《无库存》 \n ASIN       title\n'
					STORESLIST[0].append(["NoBuybox",])
					STORESLIST[1].append(["ASIN","title","被跟卖个数","卖家Id","卖家名字","review",])
					STORESLIST[2].insert(0,["低评分asin",])
					STORESLIST[1].insert(0,["被跟卖asin",])
     
					STORESLIST[3].sort(key=lambda items: time.strptime(items[2], '%a %b %d %H:%M:%S %Y'),reverse = True)
					STORESLIST[3].insert(0,["变狗",])
					STORESLIST[4].insert(0,["正常",])
					STORESLIST[5].insert(0,["未下库存",])
	 

					for sv,tt,sz ,scb ,of in bb:
						if tt=="无库存":
							Currently_unavailable+=sv+"  "+of[3]+"\n"
							STORESLIST[0].append([sv,of[3],tt])	
						elif tt=="NoBuyBox":
							NoBuybox+=sv+"  "+of[3]+"\n"
							STORESLIST[0].append([sv,of[3],tt])	
							
						else:
							for v in sz:
								if v[-3] not in sc:
									ob+=sv+"  "+sz[-1][-1]+"           "+v[-2]+"    " +v[-3]+ "  "+scb+"           "+of[3]+"\n"
									STORESLIST[1].append([sv,of[3],sz[-1][-1],v[-2],v[-3],scb])
								elif time.localtime( time.time() )[3]==12 or time.localtime( time.time() )[3]<9:
									dof+=sv+"  "+sz[-1][-1]+"           "+v[-2]+"    " +v[-3]+ "  "+scb+"           "+of[3]+"\n"
									STORESLIST[5].append([sv,of[3],sz[-1][-1],v[-2],v[-3],scb])
							# time.sleep(3)
					print (NoBuybox)
					print (ob)
					print (dog)
					bs=[ [] for s in STORESLIST]
					bs[0]=STORESLIST[1]
					bs[1]=STORESLIST[3]
					bs[2]=STORESLIST[5]
					bs[3]=STORESLIST[0]
					bs[4]=STORESLIST[2]
					bs[5]=STORESLIST[4]
					htmlList=[]
					for item  in bs: 	
						# for asin in item:
						htmlList.append(item)
					setScreenXls(STORESLIST)
					browser.quit()
					setN=	getXlsList("start.xls")
					now_asin=[ asin[0] for asin in sft]
					[ sft.append(asin)   for  asin in  getXlsList("start.xls")[0] if asin[0] not in now_asin ]
					setN[0]= sft
					print (sft)
					setScreenXls(setN,"start.xls")	
					Email("1",AsinItemToHtml.toHtml(htmlList),keys[-2][0][0])
					# [EmailNECR(x,AsinItemToHtml.toHtml(htmlList),keys[-2][0][0]) for x in keys[-1]]
					ssh= paramiko.Transport(("82.156.171.227",22))
					ssh.connect(username="root", password="1634475170qQ")
					sftp = paramiko.SFTPClient.from_transport(ssh)
					sftp.put("asin.xls",'/root/search/File/asin.xls')
					# time.sleep(60*10)
     
		except Exception as es:
			print (es)
			browser.quit()

			# getWebbYs(page,keys)
   # ['641741859@qq.com','1517496767@qq.com','1634475170@qq.com',"78845417@qq.com","1192373460@qq.com","10098591@qq.com","70354857@qq.com"]

if __name__ == "__main__":
	import time
	# page=input("页数:")
	# keys=input("key:")
	# keys=open('as.txt','r').readl/ines()
	# keys='hp laptop'
 
	while True:
		try:
			keys=	getXlsList("start.xls")
			keys[-1]=[emali[0] for emali in keys[-1] ]
			print ( int(keys[-2][1][0]))
			# print(keys[-2][0])
			# break
			getWebbYs(keys)
		except Exception as es:
			print (es)	
			break
		
		