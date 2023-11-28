import requests,json, sys,datetime,keepa
import numpy as np

sys.path.append('../')
from update import setScreenXls,readFile,getXlsList,setScreenXlsAsin,setScreenXlsa

# import requests.sessionsessions
cUrl='https://sellercentral.amazon.com/rcpublic/searchproduct?countryCode=US&locale=en-US'
aUrl='https://sellercentral.amazon.com/rcpublic/getadditionalpronductinfo?countryCode=US&asin=&fnsku=&searchType=GENERAL&locale=en-US'
bUrl='https://sellercentral.amazon.com/rcpublic/getprograms?countryCode=US&asin=&locale=en-US'
eUrl='https://sellercentral.amazon.com/rcpublic/getfees?countryCode=US&locale=en-US'
sUrl='https://fulfillment.speedersolutions.com/public/amazon_overview_asins/update/comments'
vUrl='https://fulfillment.speedersolutions.com/public/sales-report/asin-review'
# keepUrl=''
key='bvljtgbemk8gs3tjmas9va1tu73ij0kr86jiva4lgaef8nlnfmtr84hhe4ibid5l'
headers={
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
	'Content-Type':'application/json; charset=UTF-8',
	# 'Cookie':'session-id=139-7067946-8866464; ubid-main=130-6314803-4828838',
	'Referer':'https://sellercentral.amazon.com/hz/fba/profitabilitycalculator/index?lang=en_US',
	'Origin':'https://sellercentral.amazon.com',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
http_proxy  = "http://304504D9:50C3CCDAD815@tunnel5.qg.net:16588"
https_proxy = "https://304504D9:50C3CCDAD815@tunnel5.qg.net:16588"
# ftp_proxy   = "ftp://10.10.1.10:3128"
# proxy = {'tunnel.qg.net':}
proxies={
		"http"  : http_proxy, 
		"https" : https_proxy, 
}
postdata={"keywords":"B08ZMJWVVQ","countryCode":"US","searchType":"GENERAL","pageOffset":1}

getfees={"countryCode":"US","itemInfo":{"asin":"B0C69B1V7B","glProductGroupName":"gl_pc","packageLength":"0","packageWidth":"0","packageHeight":"0","dimensionUnit":"","packageWeight":"0","weightUnit":"","afnPriceStr":"689","mfnPriceStr":"689","mfnShippingPriceStr":"0","currency":"USD","isNewDefined":False},"programIdList":["Core","MFN"],"programParamMap":{}}

RET=[]

def query_Buybox(asin , key=key,avgdays=1,buybox=1):
	a=0
	while True:
		try:
			return keepa.Keepa(key).query(asin,rating=1,buybox=buybox,)[0]
			# kp=json.loads (requests.get(url='https://api.keepa.com/product?key=bvljtgbemk8gs3tjmas9va1tu73ij0kr86jiva4lgaef8nlnfmtr84hhe4ibid5l&domain=1&asin='+asin+'&rating=1&buybox='+str(buybox)+'&stats='+str(stats),verify=False,timeout=10).text)['products'][0]
		except:a+=1

def FBA_searchproductv(asin):
	Session=requests.Session()
	Session.proxies=proxies
	Session.headers=headers
	postdata['keywords']=asin[0]
	# cs=json.loads(Session.post(cUrl,headers=headers,json=postdata,proxies=proxies).text)
	cs=json.loads(Session.get(aUrl.replace('asin=','asin='+asin[0]),headers=headers,proxies=proxies).text)
 
	# cs['data']['products']
	# weight=cs['data']['products'][0]['weight']
	# weightUnit=cs['data']['products'][0]['weightUnit']
	# width=cs['data']['products'][0]['width']
	# length=cs['data']['products'][0]['leeight']
	# RET.append([asin[0],weight,weightUnit,width,length,height])
	# asin.append(cs['data']['products'][0]['customerReviewsCount'])
	# asin.append(cs['data']['products'][0]['customerReviewsRatingValue'])
	if cs['data']=={}:return 0
	if 'amount' in cs['data']['price']:
		if cs['data']['price']['amount']!=0:
			return cs['data']['price']['amount']
		else:
			return 0

def FBA_searchproduct(asin):
	Session=requests.Session()
	Session.proxies=proxies
	Session.headers=headers
	postdata['keywords']=asin[0]
	# cs=json.loads(Session.post(cUrl,headers=headers,json=postdata,proxies=proxies).text)
	cs=json.loads(Session.get(aUrl.replace('asin=','asin='+asin[0]),headers=headers,proxies=proxies).text)
 
	# cs['data']['products']
	# weight=cs['data']['products'][0]['weight']
	# weightUnit=cs['data']['products'][0]['weightUnit']
	# width=cs['data']['products'][0]['width']
	# length=cs['data']['products'][0]['leeight']
	# RET.append([asin[0],weight,weightUnit,width,length,height])
	# asin.append(cs['data']['products'][0]['customerReviewsCount'])
	# asin.append(cs['data']['products'][0]['customerReviewsRatingValue'])
	if cs['data']=={}:
		price=query_Buybox(asin[0])
		if  'BUY_BOX_SHIPPING' in price['data'] and  np.isnan(price['data']['BUY_BOX_SHIPPING'][-1])==False:
			RET.append([asin[0],price['data']['BUY_BOX_SHIPPING'][-1]])
			return price['data']['BUY_BOX_SHIPPING'][-1]
		else:
			RET.append([asin[0],'Nobb'])
			return 0 
	if 'amount' in cs['data']['price']:
		if cs['data']['price']['amount']!=0:
			RET.append([asin[0],cs['data']['price']['amount']
               ])
			return cs['data']['price']['amount']
		else:
			RET.append([asin[0],'Nobb'])
			return 0 
	else:
		RET.append([asin[0],'Nobb'])
		return 0 
	# RET.append(asin)
 
def FBA_FulfillmentCost(asin):
	Session=requests.Session()
	cs=json.loads(Session.get(aUrl.replace('asin=','asin='+asin[0]),headers=headers,proxies=proxies).text)
	price=cs['data']['price']['amount']
	getprograms=json.loads(Session.get(bUrl.replace('asin=','asin='+asin[0]),headers=headers,proxies=proxies).text)
	getfees['itemInfo']['asin']=asin[0]
	getfees['itemInfo']['afnPriceStr']=str(price)
	getfees['itemInfo']['mfnPriceStr']=str(price)
	getfees['programIdList']=[]
	for program in getprograms['programInfoList']:
		getfees['programIdList'].append(program['name'])
	getFee=json.loads(Session.post(eUrl.replace('asin=','asin='+asin[0]),headers=headers,json=getfees,proxies=proxies).text)
	RET.append([asin[0],getFee['data']['programFeeResultMap']['Core']['otherFeeInfoMap']['FulfillmentFee']['feeAmount']['amount']])
	return getFee
# getXlsList
# print(Session.get('https://sellercentral.amazon.com/rcpublic/getadditionalpronductinfo?countryCode=US&asin=B08ZMJWVVQ&fnsku=&searchType=GENERAL&locale=en-US',headers=headers,proxies=proxies).text)

def update_FBA_Fulfillment(asinItem):
	# date={
	# 	"userId":1102,
	# 	"asin":"B323412345",
	# 	"commentsNum":"ads",
	# 	"score":3.0
	# }
	# date["asin"]=asin[0]
	# date['commentsNum']=str(int(asin[-2]))
	# date['score']=asin[-1]
	# print(date)
	postData=[]
	for asin in asinItem:
		if float(asin[-2])==0 and int(asin[-1].replace(' ',''))==0:continue
		postData.append({"userId":1102,"asin":asin[0],"score":float(asin[-2]), "commentsNum": int(asin[-1].replace(' ','')),"parentAsin":None,})
	PJson={'list':postData}
	print (requests.post(vUrl,json=PJson).text)
 

def gettoday():
	c=datetime.datetime.now()
	mm=str(c.month) if c.month >=10  else ('0'+str(c.month))
	fz=str(c.day) if c.day >=10 else   ('0'+str(c.day))
	return(str(c.year)+'-'+mm+'-'+fz)

if __name__ == "__main__":
	# update_FBA_Fulfillment(getXlsList('C:\\File\\Qx\\allasin.xls')[0])
	# FBA_searchproduct(['B0C4NZ4W22',])

	for asin in getXlsList('C:\\File\\keepa\\'+gettoday()+'.xlsx')[1]:
		# if asin[-1]=='':continue
		print(asin[0])
		while True:
			try:
				FBA_searchproduct(asin)
				break
			except Exception as ex:
				print ('er')
				# RET.append([asin[0],'er'])
			
	setScreenXls([RET,],'C:\\File\\keepa\\1.xlsx')
# r = requests.post('https://sellercentral.amazon.com/rcpublic/searchproduct?countryCode=US&locale=en-US',data=postdata, headers=headers, proxies=proxies)
# print (r.text)