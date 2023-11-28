
# -*- coding: utf-8 -*-
import keepa
import numpy as np
from keepa.interface import keepa_minutes_to_time, parse_csv
# import matplotlib.pyplot as plt
import json,datetime,time
from  openpyxl import  Workbook, workbook ,load_workbook
from dateutil.relativedelta import   relativedelta
import rcpublic
from update import setScreenXls,readFile,getXlsList,setScreenXlsAsin,setScreenXlsa,getXlsListxlsx
from spider import Spider,Spider1
from selenium.webdriver.common.by import By

aUrl='https://sellercentral.amazon.com/rcpublic/getadditionalpronductinfo?countryCode=US&asin=&fnsku=&searchType=GENERAL&locale=en-US'

br=	Spider(1)
br.browser.get('https://sellercentral.amazon.com/hz/fba/profitabilitycalculator/index?lang=en_US')
#  kat-button
time.sleep(3)
br.browser.find_elements(By.XPATH,'//kat-button')[-1].click()
time.sleep(2)


def plot_product(product, keys=['AMAZON', 'USED', 'COUNT_USED', 'SALES'],
				 price_limit=1000, show=True ,asin=''):


	if 'data' not in product:
		product['data'] = parse_csv[product['csv']]

	# Use all keys if not specified
	if not keys:
		keys = product['data'].keys()

	# Create three figures, one for price data, offers, and sales rank
	pricefig, priceax = plt.subplots(figsize=(10, 5))
	pricefig.canvas.manager.set_window_title('Product Price Plot')
	plt.title(product['title'])
	plt.xlabel('Date')
	plt.ylabel('Price')
	pricelegend = []

	# Add in last update time
	lstupdate = keepa_minutes_to_time(product['lastUpdate'])

	# Attempt to plot each key
	for key in keys:
		# Continue if key does not exist
		if key not in product['data']:
			continue

		elif 'SALES' in key and 'time' not in key:
			if product['data'][key].size > 1:
				x = np.append(product['data'][key + '_time'], lstupdate)
				y = np.append(product['data'][key],
							  product['data'][key][-1]).astype(np.float)
				replace_invalid(y)

				if np.all(np.isnan(y)):
					continue


		elif 'COUNT_' in key and 'time' not in key:
			x = np.append(product['data'][key + '_time'], lstupdate)
			y = np.append(product['data'][key],
						  product['data'][key][-1]).astype(np.float)
			replace_invalid(y)

			if np.all(np.isnan(y)):
				continue


		elif 'time' not in key:
			x = np.append(product['data'][key + '_time'], lstupdate)
			y = np.append(product['data'][key],
						  product['data'][key][-1]).astype(np.float)
			replace_invalid(y, max_value=price_limit)

			if np.all(np.isnan(y)):
				continue

			priceax.step(x, y, where='pre')
			pricelegend.append(key)

	# Add in legends or close figure
	pricefig.savefig('C:\\Users\\admin\\Desktop\\getOffers\\Delivery\\asin\\'+ asin)

	if pricelegend:
		priceax.legend(pricelegend)
	else:
		plt.close(pricefig)

	if not plt.get_fignums():
		raise Exception('Nothing to plot')




	if False:
		plt.show(block=True)
		plt.draw()
		# import time
		# time.sleep(0.5)
		# plt.savefig()
		# plt.savefig


def replace_invalid(arr, max_value=None):
	""" Replace invalid data with nan """
	with np.warnings.catch_warnings():
		np.warnings.filterwarnings('ignore')
		arr[arr < 0.0] = np.nan
		if max_value:
			arr[arr > max_value] = np.nan


def query_keepa(asin , key='bvljtgbemk8gs3tjmas9va1tu73ij0kr86jiva4lgaef8nlnfmtr84hhe4ibid5l',avgdays=None):
	kp=keepa.Keepa(key).query(asin,rating=1)[0]

	# kp=keepa.Keepa(key).best_sellers_query(category='13896591011')

	cSalesRanks=kp['salesRanks']
	bs=kp['data']
	AmzonList,AmzonList_time=bs['AMAZON'],bs['AMAZON_time']
	NEW ,new_time=bs['NEW'],bs['NEW_time']
	SALES ,SALES_time=bs['SALES'],bs['SALES_time']
	NEW_Dic,SALES_Dic ,i,scSalesRanks_Dic={},{},0,{}
	for NewItem in NEW:
		NEW_Dic[new_time[i]]=NewItem
		i+=1
	i=0
	for SALESItem in SALES:
		SALES_Dic[SALES_time[i]]=SALESItem
		i+=1

	if cSalesRanks==None:key0=[]
	else:
		key0=[list(cSalesRanks.keys())[0]][0]
		for ra in range( int(len(cSalesRanks[list(cSalesRanks.keys())[0]])/2)):
			timestamp=(cSalesRanks[key0][ra*2] +21564000) *60000
			keeptime=datetime.datetime.fromtimestamp(timestamp/1000)
			scSalesRanks_Dic[keeptime]=cSalesRanks[key0][ra*2+1]
	AmzonList_time=list(AmzonList_time)
	AmzonList=list(AmzonList)
	AmzonList.append(AmzonList[-1])

	AmzonList_time.append(datetime.datetime.now())
	rating,count_reviews=0,0
	if kp['hasReviews']==True:
		rating=kp['data']['RATING'][-1]
		count_reviews=kp['data']['COUNT_REVIEWS'][-1]
	return {'title':kp['title'],"rating":rating,"count_reviews":count_reviews,'AmzonList':AmzonList,'AmzonList_time':AmzonList_time,'NEW_Dic':NEW_Dic,'SALES_Dic':SALES_Dic,'bs':[bs['SALES'],bs['SALES_time']],'cSalesRanks':scSalesRanks_Dic}


def  setDya(dya,AmzonList_time,index,last ,v):
		if  AmzonList_time[index]<=last:
			dya = ((v-last).days*60*60*24)+ dya+(v-last).seconds
		else:
			dya= ((v-AmzonList_time[index]).days*60*60*24)+ dya+(v-AmzonList_time[index]).seconds
		return dya

def time_difference(time1,time2):
	return (time1 - time2).days

def search_data_bykeepaApi(asin):

	dic=query_keepa(asin)
	AmzonList_time =list(reversed(dic['AmzonList_time']))
	init_count,index,is_stock_in60days ,Nstock_time,price_list,rank_list=0,0,True,{},[],[]
	stock_count=[]
	hasStock_timeTa,rankIndex,rankIndexT,bestRankPrice ,best_Rank_by_two_week,best_Rank_by_two_week_time,best_Rank_by_two_week_price=[],-1,{},0,-1,{},0
	best_Rank_by_two_week_time['starTime']=datetime.datetime.now()
	best_Rank_by_two_week_time['endTime']=datetime.datetime.now()
	rankIndexT['endTime']=datetime.datetime.now()
	rankIndexT['starTime']=datetime.datetime.now()
	lastStock='never'
	dya ,dya60,dya180,dya360,dya30=0,0,0,0 ,0
	index,v=0,1
	AmzonList_time =dic['AmzonList_time']
	a=datetime.datetime.now()
	last30=a  - relativedelta(months=1)
	last90=a  - relativedelta(months=3)
	last180=a  - relativedelta(months=6)
	last60=a  - relativedelta(months=2)
	last360=a  - relativedelta(months=12)

	for uAmzon in dic['AmzonList']:
		if index+1==len(AmzonList_time):
			v=datetime.datetime.now()
		else:
			v=AmzonList_time[index+1]
		
		if  np.isnan(uAmzon) :
			
			# init_count+=1
			# if index+1==len(AmzonList_time):
			# 	hasStock_timeTa.append({'starTime':AmzonList_time[index-1],'endTime':AmzonList_time[index]})
			# 	break
			if (v-AmzonList_time[index] ).days>14:
					Nstock_time={'starTime':AmzonList_time[index],'endTime':v}
			hasStock_timeTa.append({'starTime':AmzonList_time[index],'endTime':v})
		else:
			if v >=last30:
				dya30 =setDya(dya30,AmzonList_time,index ,last30,v)
    				
			if v >=last60:
				dya60 =setDya(dya60,AmzonList_time,index ,last60,v)
			if v >=last180:
				dya180 =setDya(dya180,AmzonList_time,index ,last180,v)
			if v >=last360:
				dya360 =setDya(dya360,AmzonList_time,index ,last360,v)
			if v >=last90:
				if  AmzonList_time[index]<=last90:
					dya = ((v-last90).days*60*60*24)+ dya+(v-last90).seconds
				else:
					dya= ((v-AmzonList_time[index]).days*60*60*24)+ dya+(v-AmzonList_time[index]).seconds
			
			stock_count.append({'starTime':AmzonList_time[index],'endTime':v})
		index+=1

# 27200280.0 ((last90-v).days*60*60*24)+
	dya = dya/(60*60*24*90)
	dya60 = dya60/(60*60*24*60)
	dya180 = dya180/(60*60*24*180)
	dya360 = dya360/(60*60*24*360)
	dya30 = dya30/(60*60*24*360)



	AmzonList_time =list(reversed(dic['AmzonList_time']))
	index=0
	lastStocks='k'
	for Azmon in list(reversed(dic['AmzonList'])):
		if  np.isnan(Azmon) ==False:
			if index==0:
				lastStock ='today'
			else:
				lastStock =AmzonList_time[index-1]
			break
		index +=1
	if lastStock=='never':return [asin,lastStock]

	for key  in dic['NEW_Dic'].keys():
		if Nstock_time=={}:break
		if key>Nstock_time['starTime']:break
		if key >= Nstock_time['endTime']:
			if  np.isnan(dic['NEW_Dic'][key]) ==False:		price_list.append(dic['NEW_Dic'][key])
	# print(price_list)
	# //find bestRanks
 
	SALES=dic['bs'][0]
	SALES_time=dic['bs'][1]
	index=0
	v=0
	for SALES_item in SALES:
		if index+1==len(SALES_time):break
		else:v=SALES_time[index+1]
	
		if isINsection(SALES_time[index],v,hasStock_timeTa ):
			if  v>=last90 :
				# print(datetime.datetime.now()-v)

				if  rankIndex!=-1:
					if rankIndex > SALES_item:
						rankIndex=SALES_item
						# print (key)
						rankIndexT={'starTime':SALES_time[index],'endTime':v}

				else:
					rankIndex=SALES_item
					rankIndexT={'starTime':SALES_time[index],'endTime':SALES_time[index+1]}
			if lastStock!='today' and lastStock!='never' and (lastStock-v).days<=14 :
    				
				if best_Rank_by_two_week!=-1:
					if best_Rank_by_two_week > SALES_item:
						best_Rank_by_two_week=SALES_item
						best_Rank_by_two_week_time={'starTime':SALES_time[index],'endTime':v}
				else:
					best_Rank_by_two_week=SALES_item
					best_Rank_by_two_week_time={'starTime':SALES_time[index],'endTime':v}
		index+=1	
	index=0
	st=best_Rank_by_two_week_time['starTime']
	ste=best_Rank_by_two_week_time['endTime']
	rt=rankIndexT['starTime']
	rte=rankIndexT['endTime']

	AmzonList_time =dic['AmzonList_time']
	for  uAmzon in  dic['AmzonList']:
		if index+1==len(AmzonList_time):break
		else:v=AmzonList_time[index+1]
		amt= AmzonList_time[index]
		if np.isnan(uAmzon):
			index+=1
			continue

		if st<=amt<=ste or amt<= st <= v or amt<= ste <=v :
			best_Rank_by_two_week_price=uAmzon
		if  rt<=amt<=rte or amt<= rt <= v or amt<= rte <= v   :
			bestRankPrice=uAmzon
		index+=1
		

		# if dic['NEW_Dic']
	print(rankIndex)
	print(rankIndexT)
	print(bestRankPrice)
	print(best_Rank_by_two_week)
	print(best_Rank_by_two_week_time)
	print(best_Rank_by_two_week_price)
	avg90Stock='是'
	print (bestRankPrice)
	if bestRankPrice ==0:
		rankIndexT['starTime']='-'
		rankIndexT['endTime']='-'
		rankIndex='-'
		avg90Stock='否'
	else:
		best_Rank_by_two_week='-'
		best_Rank_by_two_week_time['starTime']='-'
		best_Rank_by_two_week_time['endTime']='-'
	


		best_Rank_by_two_week_price='-'
	if lastStock!='never':
		if lastStock=='today':avg90Stock='是'
		elif (datetime.datetime.now()-lastStock).days<91:avg90Stock='是'
		else:avg90Stock='否'

	dya='{:.2%}'.format(dya)
	dya60='{:.2%}'.format(dya60)
	dya180='{:.2%}'.format(dya180)
	dya360='{:.2%}'.format(dya360)

	dya30='{:.2%}'.format(dya30)

	return [asin,lastStock,avg90Stock,rankIndex,rankIndexT['starTime'],rankIndexT['endTime'],bestRankPrice,best_Rank_by_two_week,best_Rank_by_two_week_time['starTime'],best_Rank_by_two_week_time['endTime'],best_Rank_by_two_week_price,dya30,dya60,dya,dya180,dya360]



import requests
def search_dataPrent_bykeepaApi(asin): 
	a=0
	while True:
		try:
			return keepa.Keepa('bvljtgbemk8gs3tjmas9va1tu73ij0kr86jiva4lgaef8nlnfmtr84hhe4ibid5l').query(asin,only_live_offers=1,)[0]
			# return json.loads (requests.get(url='https://api.keepa.com/product?key=bvljtgbemk8gs3tjmas9va1tu73ij0kr86jiva4lgaef8nlnfmtr84hhe4ibid5l&domain=1&asin='+asin+'&only_live_offers=1',verify=False,timeout=10).text)['products'][0]
		except Exception as ex:
			print(a)
			print(ex)
			a+=1

oss={
		'win10' :['windows 10','win10','win 10'],
		'win10p':['windows 10 pro','win10 pro' ,'win 10 pro','w10p'],
		'chromebook' :['chromebook'],
		'W11':['windows 11','win11','win 11'],
		'w11p':['windows 11 pro','win11 pro','win 11 pro'],

		}

ramcost={'4':-5,
	 '8':0,
	 '12':12,'16':14,'20':22,
	 '12':12,'16':14,'20':22,
	 '12':12,'16':14,'20':22,

	 }
ram =['DDR','Memory','RAM']
disk=['eMMC','NVME','PCIE','SSD','HDD','Solid State Drive']
# bbb=
import re

def query_keepabb(asin , key='bvljtgbemk8gs3tjmas9va1tu73ij0kr86jiva4lgaef8nlnfmtr84hhe4ibid5l',avgdays=None,stats=14,buybox=1):
	a=0
	while True:
		try:
			kp=keepa.Keepa(key).query(asin,rating=1,buybox=buybox,stats=stats)[0]
			# kp=json.loads (requests.get(url='https://api.keepa.com/product?key=bvljtgbemk8gs3tjmas9va1tu73ij0kr86jiva4lgaef8nlnfmtr84hhe4ibid5l&domain=1&asin='+asin+'&rating=1&buybox='+str(buybox)+'&stats='+str(stats),verify=False,timeout=10).text)['products'][0]

			break
		except:a+=1
	# kp=keepa.Keepa(key).best_sellers_query(category='13896591011')
	cSalesRanks=kp['salesRanks']
	ram,ssd='',''
	size=kp['size']
	# if kp['title'] !=None:
	# 	os= 'mac' and  kp['title'].find('win')>0 or 'windows' 
	bs=kp['data']
	# if size!=None and len(size.split('|'))>1:
	# 	ram=size.split('|')[0]
	# 	ssd=size.split('|')[1]
	os='home'
	
	for k in oss:
		for o in oss[k]:
			if kp['title'].lower().find(o)>=0:os=k
	ramre='\d{1,3} {0,1}GB( |,|/|-|&|\|)(Memory|ram|DDR4|DDR5)'.lower()

	ssdre='\d{0,3}(?: |,|/|-|&|\||)(?:gb|tb)(?: |,|/|-|&|\|)(?:emmc|nvme|pcie|ssd|hdd)'.lower()
	title=kp['title'].lower()
	scram=	re.search(ramre,title)
	scdisk=	re.findall(ssdre,title)
	print (title)
	if scram!=None:ram=scram.group().upper().replace('DDR4','').replace('DDR5','').replace('RAM','').replace('MEMORY','')
	diskcost=0
	distupdat=0
	cst={}
	for pf in platformType:
		for ut in updataType:
			cst[pf+ut]=0
	print (len(scdisk))
	if  len(scdisk)>=2:
		for cs in cst:
			distupdat=Cost['ssd']['PCIE trade in'+cs]
			cst[cs]+=Cost['ssd']['PCIE trade in'+cs]
    
	if True:
		for disk  in scdisk:
			scd=disk.replace('nvme','pcie').replace('pcie','pcie ssd').upper().strip()
			print (scd)
			ssd+=scd+'/'
			c=re.search('\d{0,3}',scd).group()
			if scd.find('PCIE')>=0:
		
				for cs in cst:
					distupdat=Cost['ssd']['PCIE trade in'+cs]

					# if Cost['ssd']['pcie'][c+cs]!=0:

					# 	cst[cs]+=Cost['ssd']['PCIE trade in'+cs]
					cst[cs]+=Cost['ssd']['pcie'][c+cs]
				diskcost+=Cost['ssd']['pcie'][c]
				# for cs in cst:cst[cs]+=Cost['ssd']['pcie'][c+cs]
			elif scd.find('HDD')>=0:
				diskcost+=Cost['ssd']['hdd'][c]
				for cs in cst:cst[cs]+=Cost['ssd']['hdd'][c+cs]

			elif scd.find('EMMC')<0:
					
				for cs in cst:
					distupdat=Cost['ssd']['SSD trade in'+cs]
					# if Cost['ssd']['ssd'][c+cs]!=0 and distupdat!=0 :
						# cst[cs]+=Cost['ssd']['SSD trade in'+cs]

				diskcost+=Cost['ssd']['ssd'][c]
				for cs in cst:
					cst[cs]+=Cost['ssd']['ssd'][str(c)+cs]
		
	ssd=ssd[:-1]

	if ram!='' and ssd=='':
		r='(Memory|ram|DDR4|DDR5).{0,3}\d{0,3} {0,1}(GB|TB)'
		if re.search(r,title)!=None:ssd=re.search(r,title).group().replace('nvme','pcie').upper().strip()
	ram=ram.replace(' ','')
	# AmzonList,AmzonList_time=bs['AMAZON'],bs['AMAZON_time']
	# NEW ,new_time=bs['NEW'],bs['NEW_time']
	# SALES ,SALES_time=bs['SALES'],bs['SALES_time']
	NEW_Dic,SALES_Dic ,i,scSalesRanks_Dic={},{},0,{}
	# # for NewItem in NEW:
	# 	# NEW_Dic[new_time[i]]=NewItem
	# 	# i+=1
	# i=0
	# for SALESItem in SALES:
	# 	SALES_Dic[SALES_time[i]]=SALESItem
	# 	i+=1
	ospay=10 if os.find('p')>=0 else 0

	rampay=0
	ssdpay=0
	if cSalesRanks==None:key0=[]
	else:
		key0=[list(cSalesRanks.keys())[0]][0]
		for ra in range( int(len(cSalesRanks[list(cSalesRanks.keys())[0]])/2)):
			timestamp=(cSalesRanks[key0][ra*2] +21564000) *60000
			keeptime=datetime.datetime.fromtimestamp(timestamp/1000)
			scSalesRanks_Dic[keeptime]=cSalesRanks[key0][ra*2+1]
	# AmzonList_time=list(AmzonList_time)
	# AmzonList=list(AmzonList)
	# AmzonList.append(AmzonList[-1])

	# AmzonList_time.append(datetime.datetime.now())
	rating,count_reviews=0,0
	if kp['hasReviews']==True:
		rating=kp['data']['RATING'][-1]
		count_reviews=kp['data']['COUNT_REVIEWS'][-1]
	cs,sellerId,cp='','',0
	if "BUY_BOX_SHIPPING" in kp['data']:
		cp=kp['data'] ['BUY_BOX_SHIPPING'][-1]
	if "stats" in kp:
		sellerId=kp['stats']['buyBoxSellerId']

	cj=0
	ramDT={}
	for pf in platformType:
		for ut in updataType:
			for rt in RAMTYPE:
				ramDT[rt+' ' + pf +ut]=0
				# print (rt+' ' + pf +ut)

	prcz=[]
	if np.isnan(cp):cp=0
	if stats==7:
			try:
			
				br.browser.get(aUrl.replace('asin=','asin='+asin))
				time.sleep(2)
				csc=json.loads(br.browser.find_element(By.XPATH,"//pre").text)
				if csc['data']=={}:pass
				if 'amount' in csc['data']['price']:
					if csc['data']['price']['amount']!=0:
						cs= csc['data']['price']['amount']
    
				if cp!='' and cs==0:
					cs =cp
			except Exception as ex:
				cs=0
				print ('er')
	else :cs=0	
	cs=cp
	if cs!=0:
		cj=cs*0.82
		cj-=Cost['ssd']['freight']
		if ram!='':
			print (ram)
   
			r=re.search('\d{0,3}',ram).group()
			rCost= Cost['ram'][r]+diskcost+Cost['os'][os]
			cj-=rCost
			if diskcost!=0 and diskcost+Cost['os'][os]!=0 and Cost['ram'][r]!=0:
				cj-=Cost['ssd']['Upgrade']
			
			for pf in platformType:
				for ut in updataType:
					for rtc in RAMTYPE:
						rt=rtc+' ' + pf +ut
						cj=cs*0.82
						cj-=Cost['ssd']['freight'+pf +ut]
						cj-= Cost['ram'][r+rt]+Cost['os'][os]+cst[rt.split(' ')[1]]
						if cst[rt.split(' ')[1]]!=0 or Cost['os'][os]!=0 or Cost['ram'][r+rt]!=0:
							cj-=Cost['ssd']['Upgrade'+pf +ut]
						prcz.append(cj)
			for pf in platformType:
				for ut in updataType:
					for rtc in RAMTYPE:
						rt=rtc+' ' + pf +ut
						cj=cs*0.82
						cj-=Cost['ssd']['freight'+pf +ut]
						cj-= Cost['ram'][r+rt]+0+cst[rt.split(' ')[1]]
						if cst[rt.split(' ')[1]]!=0 or Cost['ram'][r+rt]!=0:
							cj-=Cost['ssd']['Upgrade'+pf +ut]
						prcz.append(cj)

	return { 'stats_parsed':kp["stats_parsed"], "BUY_BOX":cs,'ram':ram,'ssd':ssd,'os':os,'title':kp['title'],'cSalesRanks':scSalesRanks_Dic,'st':sellerId,'cj':cj,'prcz':prcz}



def  search_asin_by_keepa( asin,isSeller):
	dic7=query_keepabb(asin ,stats=7 ,buybox=1)
	dic14=query_keepabb(asin,stats=14,buybox=0)
	cs30=1000000
	cs14=1000000
	cs7= 1000000
	if 'avg' in dic7['stats_parsed']  and "SALES" in dic7['stats_parsed']['avg']:
		cs7=dic7['stats_parsed']['avg']["SALES"]
	if 'avg' in dic14['stats_parsed']  and "SALES" in dic14['stats_parsed']['avg']:
		cs14=dic14['stats_parsed']['avg']["SALES"]
	if 'avg' in dic14['stats_parsed']  and "SALES" in dic14['stats_parsed']['avg30']:
		cs30=dic14['stats_parsed']['avg30']["SALES"]
	buyBoxStats='N'
	if isSeller and dic7['st']!=None:
		#  =dic7['stats_parsed']['buyBoxStats']
			buyBoxStats=keepa.Keepa('bvljtgbemk8gs3tjmas9va1tu73ij0kr86jiva4lgaef8nlnfmtr84hhe4ibid5l').seller_query(dic7['st'])
			buyBoxStats=buyBoxStats[dic7['st']]['sellerName']
	
	return [cs14,cs30,cs7, dic7['title'],dic7['BUY_BOX'],buyBoxStats,dic7['ram'],dic7['ssd'],dic7['os'],dic7['cj'],dic7['prcz']]

	count30=0
	count14=0
	count7=0

	a=datetime.datetime.now()
	last30=a  - relativedelta(months=1)
	last14=a  - relativedelta(day=14)
	last7=a  - relativedelta(day=7)
	if dic['cSalesRanks']=={}:return [100000,100000,100000, dic['title'],dic['BUY_BOX']]
	for key in dic['cSalesRanks']:
		if  key >=last7:
			count7+=1
			cs7+=(  dic['cSalesRanks'][key])
		if  key >=last14:
			count14+=1
			cs14+=(  dic['cSalesRanks'][key])
		if  key >=last30:
			count30+=1
			cs30+=( dic['cSalesRanks'][key])
	if cs14 ==0:
		cs14=dic['cSalesRanks'][-1]
		count14=1
	if cs30==0:
		cs30=dic['cSalesRanks'][-1] 
		count30=1
	if cs7==0:
		cs7=dic['cSalesRanks'][-1] 
		count7=1	
	return [cs14/count14,cs30/count30,cs7/count7, dic['title'],dic['BUY_BOX']]


def isINsection (ptime ,sections ):

	for stime in sections:
		if stime['starTime']>=ptime>stime['endTime']:
			return False
	return True

def isINsection (ptime1,ptime2 ,sections ):
	for stime in sections:
		if stime['starTime']<ptime1 <ptime2<stime['endTime']:
			return False
	return True


# Cost=json.load(open('cost.json','r'))

Cost={
	
	"ram":{},
	"os":{},
	"ssd":{
		"ssd":{
			
      },
		"pcie":{},
		"hdd":{},
		"PCIE trade in":None,
		"SSD trade in":None	,
		'freight':0,
		'Upgrade':0
  }
}
# DDRTYPE=[D4 SSL	D5 SSL	D4 SSD,'D5 SSD'	,'D4 BOL','D5 BOL','D4 BOD','D5 BOD']
platformType=['SS','BO']
updataType=['L','D']
RAMTYPE=['D4','D5']
s=getXlsList('cost.xlsx')
# s=getXlsList('cost.xls')

for x in s[0][1:]:
	Cost['ram'][str(int(x[0]))]=x[1]
	cz=2
	for pf in platformType:
		for ut in updataType:
			for rt in RAMTYPE:
				# print (rt+' ' + pf +ut)
				Cost['ram'][str(int(x[0]))+rt+' ' + pf +ut]=x[cz]
				cz+=1

 
 
for x in s[1]:
	Cost['os'][x[0]]=x[1]

def setDt(ty,x):
	cz=2
	for pf in platformType:
		for ut in updataType:
			# print (pf +ut)
			Cost['ssd'][ty+pf+ut]=x[cz]
			cz+=1
ssdtype=''
for x in s[2][1:]:
	if str(x[0]).find('HDD')>=0:
		ssdtype='hdd'
		continue
	if str(x[0]).find('PCIE')>=0:
		ssdtype='pcie'
		continue
	if str(x[0]).find('SSD')>=0:
		ssdtype='ssd'
		continue
	if x[0]==('pcietradein'):
		Cost['ssd']['PCIE trade in']=x[1]
		setDt('PCIE trade in',x)
  
		continue
	if x[0]==('ssdtradein'):
		Cost['ssd']['SSD trade in']=x[1]
		setDt('SSD trade in',x)
		continue

	if str(x[0]).find('freight')>=0:
		Cost['ssd']['freight']=x[1]
		setDt('freight',x)
  
		continue
	if str(x[0]).find('Upgrade')>=0:
		Cost['ssd']['Upgrade']=x[1]
		setDt('Upgrade',x)
		continue
	Cost['ssd'][ssdtype][str(int(x[0]))]=x[1]
	cz=2
	for pf in platformType:
		for ut in updataType:
			# print (pf +ut)
			Cost['ssd'][ssdtype][str(int(x[0]))+pf+ut]=x[cz]
			cz+=1
   
   

s=1
def query_keepa_java(asin , key='bvljtgbemk8gs3tjmas9va1tu73ij0kr86jiva4lgaef8nlnfmtr84hhe4ibid5l',avgdays=1 ):
	kp=keepa.Keepa(key).query(asin,buybox=1,update=1)[0]
	# kp=keepa.Keepa(key).best_sellers_query(category='13896591011')

	if kp['data']=={}:return 'dog'
	if np.isnan(kp['data']['BUY_BOX_SHIPPING'][-1])  :
		return 'Nobb'
	else :return str(kp['data']['BUY_BOX_SHIPPING'][-1])


def takeSix(elem):
    return elem[6]


def search():

	s=getXlsList('asin.xls')[0]

	# s=[['B0CLHJM1XJ'],]
	if True:
		asins=[]
		AsinList=[]


		AsinList.append(['asin','Parent ASIN','BUY_BOX','TYPE','Title',"Seller",'Avg. Rank 7D','Avg. Rank 14D','Avg. Rank 30D','ram','ssd','os','GP10% UPC COST',])
		sc=['D4 16-512-11H (L)','D5 16-512-11H (L)','D4 16-512-11H (D)','D5 16-512-11H (D)',
                'D4 8-256-11H (L)','D5 8-256-11H (L)','D4 8-256-11H (D)','D5 8-256-11H (D)',
                'D4 16-512-11P (L)','D5 16-512-11P (L)','D4 16-512-11P (D)','D5 16-512-11P (D)',
                'D4 8-256-11P (L)','D5 8-256-11P (L)','D4 8-256-11P (D)','D5 8-256-11P (D)',]
		color =0
		index=0
		
		color1=[['FFD700','FFFF00'],['4876FF','436EEE']]
		for cc in sc:
			if color%4==0 and index==0:
				index=1
			elif color%4==0 and index==1:
				index=0
			AsinList[0].append((cc,color1[index][0],color1[index][1]))
			color+=1
		# setScreenXls([AsinList,],"asinRankavg.xlsx")
   
		# for pf in platformType:
		# 	for ut in updataType:
		# 		for rt in RAMTYPE:
		# 			AsinList[0].append(rt+' ' + pf +ut)
		for ab in s:
			Seller=""
			isSeller=True
			v=ab[0]
			if v  in asins:continue
			csAvg14=0
			csAvg30=0
			csAvg7=0
			keepaAo=search_dataPrent_bykeepaApi(v)
			# print (keepaAo)
			try:
				if True:
					if keepaAo['variationCSV']!=None:
						pa=[]
						for asin in (keepaAo['variationCSV']).split(',') :
							asins.append(asin)
							try:
				#  B0C5D72SBM/.	
								vavg=search_asin_by_keepa(asin,isSeller)
								if Seller!="":isSeller=False
								else : Seller=vavg[5]
								print (vavg)
								csAvg14+=1/vavg[0]
								csAvg30+=1/vavg[1]
								csAvg7+=1/vavg[2]
								pa.append([asin,[keepaAo['parentAsin']],vavg[4],'child',vavg[3] ,Seller,int(vavg[2]), int(vavg[0]),int(vavg[1]),vavg[6],vavg[7],vavg[8],vavg[9]]+vavg[10])
							except Exception as es:
								AsinList.append(["v","erro",str(es)])
								open('log.txt','a+').write(str(es))
					# vavg=search_asin_by_keepa(keepaAo['parentAsin'])
						pa.sort(reverse=True,key=takeSix)
						AsinList+=pa
						csAvg7=csAvg7 if csAvg7!=0 else 1000000 
						csAvg14=csAvg14 if csAvg14!=0 else 1000000 
						csAvg30=csAvg30 if csAvg30!=0 else 1000000 
						AsinList.append([keepaAo['parentAsin'],[keepaAo['parentAsin']],vavg[4],'parent',vavg[3],Seller,int(1/csAvg7), int(1/csAvg14),int(1/csAvg30)])
							# unm+=1
					else:
						try:
						
							vavg=search_asin_by_keepa(v,True)
							AsinList.append([v,'',vavg[4],'parent',vavg[3],vavg[5],int(vavg[2]),int(vavg[0]),int(vavg[1]),vavg[6],vavg[7],vavg[8],vavg[9]]+vavg[10])
						except Exception as es:
							AsinList.append([asin,"v","erro",str(es)])
							open('log.txt','a+').write(str(es))
					AsinList.append(["",])
			except Exception as es:
				open('log.txt','a+').write(str(es))
				AsinList.append([asin,"v","erro",str(es)])
				
				# setScreenXls([AsinList,],"asinRankavg.xlsx")
		setScreenXls([AsinList,],"asinRankavg.xlsx")




def gettoday():
	c=datetime.datetime.now()
	mm=str(c.month) if c.month >10  else ('0'+str(c.month))
	fz=str(c.day) if c.day >10 else   ('0'+str(c.month))
	return(str(c.year)+'-'+mm+'-'+fz)
 

# [	
# B083ZYLGGR
# B01LZW2L1P
# B09J79Y6Z5
# B08VF1PKPF
# B01MZD55F2
# B08HJS5VX8
# B0875J4RYWsds
# ]
import sys 
if __name__ == "__main__":
	
#  B0BX4T79QV B0BY8FFH1M B0BVBXWG9F B0C4WQDXCV B0BWSN9T3D B0BTPGWC94 B0BS6QSTNK B0C282TK59 B0BLT1VQN6
	s="B0BX4T79QV".split(' ')

	# v=input('path:')
	# sv=search_asin_by_keepa('B0C76861LD',True)
	# print ('test')
	search()
	br.closeChrome()
	# print (search_dataPrent_bykeepaApi("B0BS6QSTNK"))
	# time.sleep(60*)
	# time.sleep(60*60*3)
 
	# s=getXlsListxlsx('C:\\File\\keepa\\Amazon_sales_report_asinSkuReportData_2023-07-06_TO_2023-07-06.xlsx')[0]

	# s=getXlsListxlsx('C:\\File\\keepa\\'+gettoday()+'.xlsx')[1]
	# s=getXlsListxlsx('C:\\File\\keepa\\2023-07-11.xlsx')[1]
 
	
	# # # s=getXlsList('keepa.xls')[0]+s
	# # # # setScreenXlsAsin(s)

	# sount=[]
	
	# # sount=[['Asin','亚马逊最近有货日期','最近3个月是否有货','最近有货3个月最好的rank','时间','','售价','最近有货2周最好的rank','时间','','售价','30','60','90','180','360','',datetime.datetime.now()],]
	# for aisn in s:
	# 	bs=[]
	# 	try:
	# 		# b=query_keepa(aisn[0])
	# 		# sount.append([aisn[0],b['title'],b['rating'],b['count_reviews']])
	# 		b=query_keepa_java(aisn[1])
	# 		print (aisn[1] +''+ b)
	# 		bs.append(aisn[1])
	# 		bs.append(b)
	# 		time.sleep(4)
	# 	except Exception as ex:
	# 		print (ex)
	# 		bs.append(aisn[1])
	# 		bs.append('er')

	# 	sount.append(bs)
	# # sount.append(search_data_bykeepaApi('B01MZD55F2'))

	# setScreenXls([sount,],"C:\File\keepa\sc.xlsx")