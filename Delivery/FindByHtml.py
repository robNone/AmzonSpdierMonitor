# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys ,re 
 
STORE=['Holiday Tech Deals','Back to School Computer Deals','Discount PC Store','longhorn Computers',
'northeastern online','Computer Distribution Solution','boomoo','GLOBAL CR']
NEWEGGSSTORE=['Mid-Atlantic Laptops and Desktops']
def findBuyPriceByHtml(Html ,storeName=None ,lowPrice=None):
	html=str(Html).replace('\n','')
	storePrice='0'
	try:
		for item in re.split('a-row a-spacing-mini olpOffer',html)[1:]:
			if re.search('(?<=">from seller ).+?(?=and price .)', item).group().strip()==storeName:
				if lowPrice!=None:
					storePrice=re.search('(?<=and price .).+?(?=</span>)', item).group()
					return[lowPrice,storePrice ]
				else:storePrice=re.search('(?<=and price .).+?(?=</span>)', item).group()
 
		for item in re.split('a-row a-spacing-mini olpOffer',html)[1:]:
			if re.search('(?<=">from seller ).+?(?=and price .)', item).group().strip() not in STORE:
				return [re.search('(?<=and price .).+?(?=</span>)', item).group(),storePrice]
	except Exception as es:
		print (es)
	return ['0','0']
def findBuyPriceByHtmlA(Html ,asin):
	html=str(Html).replace('\n','').replace('\\n','')
	isFirstPage=1
	isFind= lambda x:x != None and x.group().strip() or 'None'
	try:
		for item in re.split('a-row a-spacing-mini olpOffer',html)[isFirstPage:]:
			price=isFind(re.search('(?<=class="a-size-large a-color-price olpOfferPrice a-text-bold">).+?(?=</span>)', item)).replace(',','').replace("'",'')
			state=isFind(re.search('(?<=<span class="a-size-medium olpCondition a-text-bold">).+?(?=</span>)', item)).replace(',','').replace("'",'').replace('  ','' )
			Shipsfrom=isFind(re.search('(?<=from seller ).+?(?= and price)', item)).replace(',','').replace("'",'').replace('  ','' )
			# Soldby=isFind(re.search('(?<=role="link">).+?(?=</a>)', item)).replace(',','').replace("'",'').replace('  ','' )
			rank=isFind(re.search('(?<=class="a-icon-alt">).+?(?=out of 5 stars)', item)).replace(',','').replace("'",'').replace('  ','' )
			rcx=isFind(re.search('(?<="><b>).+?(?=positive)', item)).replace(',','').replace("'",'').replace('  ','' )
			tim=isFind(re.search('over the past .+? months', item))
			ratings=isFind(re.search('(?<=\. \().+?(?= total ratings)', item))
			yield [asin,price,state,Shipsfrom,ratings,rcx,tim,rank]
	except Exception as es:
		print (es)
def findParameter(html):
	isFind ,dom = lambda x:x != None and x.group().strip() or '',str(html).replace('\n','')
	return [isFind(re.search('(?<=id="mboParentItemNumber" name="hiddenQValue" type="hidden" value=").+?(?=" />)', dom)),isFind(re.search('(?<=id="mboMappingId" name="hiddenQValue" type="hidden" value=").+?(?=" />)', dom))]
def findLostPice(html):
	dom=str(html).replace('\n','').replace('\\u000a','').replace('\\u000d','').replace('\\u0009','').replace('\\','')
	lostPice,storePrice=0,0
	isFind= lambda x:x != None and x.group().strip() or 0
	for target_list in re.split('tr id=',dom)[1:]:
		if target_list.find(NEWEGGSSTORE[0])>0:storePrice =isFind(re.search('(?<=\$<strong>).+?(?=<\\/strong><sup>)', target_list))
		elif lostPice==0 :lostPice =isFind(re.search('(?<=\$<strong>).+?(?=<\\/strong><sup>)', target_list))
 
	return [lostPice,storePrice]    

# def findOffers(html):
# 	isFind= lambda x:x != None and x.group().strip() or 0
# 	return  int(isFind(re.search('(?<=value=").{0,5}(?=other option)',html)))+1

def findOffersLowPrice(html ,ac):
	AVC={'CollectibleLikeNew':'Collectible- Like New','CollectibleVeryGood':'Collectible- Very Good','NewItem':'New','Refurbished':'Refurbished','UsedAcceptable':'New','UsedGood':'Used- Good','UsedVeryGood':'Used- Very Good','UsedLikeNew':'Used- Like New'}
	isFind= lambda x:x != None and x.group().strip() or 0
	# if int(isFind(re.search('(?<=value=").{0,5}(?=other option)',html)))+1==1:return re.search('(?<=\$).{0,10}(?=\<\/span>)').group()
	for cs in re.split('<h5>',html)[2:]:
		print(re.split('</h5>',cs)[0].replace('\n','').replace(',','').replace('\'',''))
		print (re.split('</h5>',cs)[0].replace('\n','').replace(',','').replace('\'','').find(AVC[ac]))
		if re.split('</h5>',cs)[0].replace('\n','').replace(',','').replace('\'','').find(AVC[ac])>=0:
    		# print ( re.search('(?<=\$).{0,10}(?=\<\/span>)',cs).group())
			return re.search('(?<=\$).{0,10}(?=\<\/span>)',cs).group()
def find_offers(html):
	isFind= lambda x:x != None and x.group().strip() or "N"
	ret=[]
	# with open("asin",'a+',encoding='utf-8') as s:
	# 	s.write((html))
	# 	s.close()
	offers=isFind(re.search('\d{0,8}(?= other option)',html ))
	for cs in re.split('<h5>',html)[1:]:
		tp=(re.split('</h5>',cs)[0].replace('\\n\'','').replace('\'','').replace(',',''))
		price= isFind(re.search('(?<=class="a-offscreen">\$).{0,8}(?=<)',cs ))
		Shipsfrom=isFind(re.search('(?<=<span class="a-size-small a-color-base">).+?(?=<)',cs ))
		Sold_by=isFind(re.search('(?<=role="link">).+?(?=<)',cs.replace('\n','') )).replace('\\n\', \'','')
		sellerId=isFind(re.search('(?<=seller=).+?(?=\&)',cs ))
		# open('a.html','a+').writelines(cs)
		# ret+=''+tp+' , '+ price+' , '+ Shipsfrom+ ' , '+Sold_by+'   \n'
		ret.append([tp,price,Shipsfrom,Sold_by,sellerId ,offers])
	return ret


def et(html ,storelist):
	for cs in re.split('<h5>',html)[1:]:
		Shipsfrom=isFind(re.search('(?<=<span class="a-size-small a-color-base">).+?(?=<)',cs ))
def FindReviewerByHtml(upcHtml ,asin ,l):
	dom ,rets=str(upcHtml).replace('\n',''),[]
	isFind= lambda x:x != None and x.group().strip() or 'None'
	title= isFind(re.search('(?<=">).+', isFind(re.search('(?<=a data-hook="product-link" class="a-link-normal").+?(?=</a></h1>)', dom))))

	rank= isFind(re.search('(?<=">).{0,5}(?=out of 5 stars)',dom ))

	reviews= isFind(re.search('(?<=\|).{0,10}(?=global reviews)',dom )).replace(',','')

	for  itemStr in re.split('data-hook="review"',dom)[1:]:

		userRank= isFind(re.search('(?<=">).{0,5}(?=out of 5 stars)',itemStr ))

		Comment_time =isFind(re.search('(?<=on).{0,20},.{0,10}(?=</span>)',itemStr ))

		Configuration=isFind(re.search('(?<=Capacity:).{0,20}(?=</a>)',itemStr ))

		# Configuration=isFind(re.search('(?<=Capacity:).{0,20}(?=</a>)',itemStr ))

		review_txt=isFind(re.search('(?<=review-body).+?(?=</span>)',itemStr))

		# if itemStr.find('>Verified Purchase<')>=0:
		try:
			rets.append([asin, title,rank,reviews,userRank ,Comment_time,Configuration,review_txt,str(itemStr.find('>Verified Purchase<')>=0),str(itemStr.find('Early Reviewer Rewards')>=0),l])
		except Exception as e:pass
			# print e

			# print ' review_txt' +str(len(review_txt))
	# print reviews
	return  rets    

def findUpcByHtml(upcHtml ,upc ,asin):
	dom=str(upcHtml).replace('\n','')   
	keys=["microbial","virus","Anti","Anti-microbial","Anti microbial","Anti microbial",]
	try:
		isFind= lambda x:x != None and x.group().strip() or 'None'
		isBuybox=dom.find("a-box-group")
		ifHasKey=""
		ifHasnewmodel=dom.find('There is a newer model of this item')>=0 and True or False
		modelasin=ifHasnewmodel==False and 'none' or isFind(re.search('B0.{8}',re.split('There is a newer model of this item',dom)[-1]))
		modelasintitle=ifHasnewmodel==False and 'none' or isFind( re.search('(?<=alt=").+?(?=")',re.split('There is a newer model of this item',dom)[-1]))

		defaultAsin=(re.findall('(?<=data-defaultAsin=").+?(?=" )', dom))
		[ defaultAsin.append(asin ) for asin in (re.findall('(?<=<option value=".,).+?(?=" )',str(dom)))]
		# strct=isFind(re.search("(?<=sellerProfileTriggerId'>).+?(?=</a>)", dom))
    
		strct=isFind(re.search('(?<=tabular-buybox-text">).+?(?=</span>)', dom))
		# print (asin+strct)
		Stock = ''
		if dom.find('Currently unavailable')>0:Stock = 'Currently unavailable'
		elif dom.find('left in stock')>0:Stock = re.search('(?<=Only ).{0,10}(?= left in stock)', dom).group()
		else :Stock='in stock'     
		DateFirstAvailable = re.findall('(?<=td class="a-size-base prodDetAttrValue">).+?(?=</td>)', dom)

		DateFirstAvailable =DateFirstAvailable !=[] and DateFirstAvailable[-1].strip().replace("\\n",'').replace("', '",'') or 'None'
		offers =re.search('(?<=\().{0,5}(?=\) from)',dom)    
		offers =offers!=None and offers.group() or 0
		Td=len(re.findall('productDetails_',dom))

		Voice_command=None 
		if len (re.split('Voice command',dom))>1:
			Voice_command=isFind(re.search('>.+?(?=</span>)',re.split('Voice command',dom)[1]))


		name = re.search('(?<=<span id="productTitle" class="a-size-large product-title-word-break">).+?(?=</span>)', dom)
		name = name != None and name.group().strip() or 'None'

		TEXT_Aboutthisitem=isFind(re.search('(?<=a-unordered-list a-vertical a-spacing-mini").+?(?=See more product details)',dom))
		TEXT_ProductDescription=isFind(re.search('(?<=Product description).+?(?=Product information)',dom))

		for s in  keys:
			if name.find(s)>=0:ifHasKey=s
			if (TEXT_Aboutthisitem.find(s)>=0 or TEXT_Aboutthisitem.find(s)>=0 ):ifHasKey=True
			if (TEXT_ProductDescription.find(s)>=0 or TEXT_ProductDescription.find(s)>=0 ):ifHasKey=True
			
		# ht=isFind(re.search('(?<=<div id="productDescription").+?(?=   </p>)', dom)).replace('\\n','').replace('\'','').replace(',','').replace('  ','')
		# ht= ht[ht.find('<p>'):-1]
		# band= re.search('(?<=<a id="bylineInfo" class="a-link-normal" href="/).+?(?=/b/)', dom)
	#    / band = band != None and band.group().strip() or 'None'
		price = re.search('(?<=class="a-size-medium a-color-price">).+?(?=</span>)', dom)
		price = price != None and price.group().strip() or 'None'
		reviews = re.search('(?<=title=").{0,5}(?=out of 5 stars)', dom)
		reviews = reviews != None and reviews.group().strip() or '0'
		if dom.find("Be the first to review this item")>0:reviews="0"
		s,reviewsNumber= re.split('id="acrCustomerReviewText" class="a-size-base">',dom),None
		reviewsNumber = len(s) > 1 and re.split(" ", s[1])[0] or 'None'
		AnsweredQuestions = re.search('(?<=">).{0,30}(?=answered)', dom)
		AnsweredQuestions = AnsweredQuestions != None and AnsweredQuestions.group().strip() or 0
		sea = re.findall("(?<=<span>#).+?(?=</span>)", dom)
		BigSellersRank, BigSellersRankTit, SamlSellersRankTit, SamlSellersRank = '0', 'None', 'None', 'None'
		try:
			if len(sea)>0:
				BigSellersRank = re.search('(?<=).{0,10}(?=in)', sea[0])
				BigSellersRank=BigSellersRank != None and BigSellersRank.group() or '0'
				BigSellersRankTit = re.search('(?<=in).+(?=\(<a)', sea[0])
				BigSellersRankTit=BigSellersRankTit != None and BigSellersRankTit.group()  or 'None'
			if len(sea)>=1:
				SamlSellersRankTit = re.findall("(?<='>).+?(?=</a>)", sea[-1])[-1]
				SamlSellersRankTit=SamlSellersRankTit != None and re.findall("(?<='>).+?(?=</a>)", sea[-1])[-1] or 'None'
				SamlSellersRank = re.search("(?<=).{0,10}(?=in)", sea[-1])
				SamlSellersRank = SamlSellersRank != None and SamlSellersRank.group() or 'None'
		except Exception:
			BigSellersRank = '0'
			BigSellersRankTit='None'
			SamlSellersRankTit = 'None'
			SamlSellersRank = '0'
		 
		try:	
			if len(list(DateFirstAvailable)) < 30  and DateFirstAvailable != 'None':
				ri = DateFirstAvailable.split(' ')[1]
				if  int(DateFirstAvailable.split(' ')[1].replace(',',''))<10:ri='0'+ DateFirstAvailable.split(' ')[1]
				if DateFirstAvailable.find('January')>=0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'01'+ri
				elif DateFirstAvailable.find('February') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'02'+ri
				elif DateFirstAvailable.find('March') >= 0:DateFirstAvailable = DateFirstAvailable.split(',')[1] + '03' + ri
				elif DateFirstAvailable.find('April') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'04'+ri
				elif DateFirstAvailable.find('May') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'05'+ri
				elif DateFirstAvailable.find('June') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'06'+ri
				elif DateFirstAvailable.find('July') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'07'+ri    
				elif DateFirstAvailable.find('August') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'08'+ri
				elif DateFirstAvailable.find('September') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'09'+ri
				elif DateFirstAvailable.find('October') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'10'+ri
				elif DateFirstAvailable.find('November') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'11'+ri
				elif DateFirstAvailable.find('December') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'12'+ri
						 
		except Exception:DateFirstAvailable=DateFirstAvailable
		# print  upc+' '+ asin+'    '+name+'  '+reviews+'  '+reviewsNumber+'  '+AnsweredQuestions+'  '+BigSellersRankTit+':'+BigSellersRank+'   '+SamlSellersRankTit+':'+SamlSellersRank+'  '+ IsCustom +'  '+DateFirstAvailable
		# if BigSellersRank=='0' and DateFirstAvailable!='None':
		# with open(asin,'a+',encoding='utf-8') as s:
		# 	s.write((dom))
		# 	s.close()
		# print(offers)
		

		return ([upc,isBuybox,asin,name.replace("'",'').replace(",",'').replace('\\','').strip(),price,reviews,reviewsNumber,Stock,str(AnsweredQuestions).replace('<span class="a-size-base">',''),BigSellersRankTit,BigSellersRank.replace(',',''),SamlSellersRankTit,SamlSellersRank.replace(',',''),DateFirstAvailable,offers,strct,defaultAsin,ifHasnewmodel,modelasin,modelasintitle,Voice_command,Td,str(ifHasKey)])
	except Exception as es:
		print (es)
		return None
def parse_AsinHtml(upcHtml ,upc ,asin):
	dom=str(upcHtml).replace('\n','')   
	# keys=["microbial","virus","Anti","Anti-microbial","Anti microbial","Anti microbial",]
	try:
		isFind= lambda x:x != None and x.group().strip() or 'None'
		isBuybox=dom.find("a-box-group")
		# strct=isFind(re.search("(?<=sellerProfileTriggerId'>).+?(?=</a>)", dom))
		strct=isFind(re.search('(?<=tabular-buybox-text">).+?(?=</span>)', dom))
		print (strct)
		Stock = ''
		if dom.find('Currently unavailable')>0:Stock = 'Currently unavailable'
		elif dom.find('left in stock')>0:Stock = re.search('(?<=Only ).{0,10}(?= left in stock)', dom).group()
		else :Stock='in stock'     
		DateFirstAvailable = re.findall('(?<=td class="a-size-base prodDetAttrValue">).+?(?=</td>)', dom)

		DateFirstAvailable =DateFirstAvailable !=[] and DateFirstAvailable[-1].strip().replace("\\n",'').replace("', '",'') or 'None'
		offers =re.search('(?<=\().{0,5}(?=\) from)',dom)    
		offers =offers!=None and offers.group() or 0
		Td=len(re.findall('productDetails_',dom))

		Voice_command=None 
		if len (re.split('Voice command',dom))>1:
			Voice_command=isFind(re.search('>.+?(?=</span>)',re.split('Voice command',dom)[1]))


		name = re.search('(?<=<span id="productTitle" class="a-size-large product-title-word-break">).+?(?=</span>)', dom)
		name = name != None and name.group().strip() or 'None'

		# TEXT_Aboutthisitem=isFind(re.search('(?<=a-unordered-list a-vertical a-spacing-mini").+?(?=See more product details)',dom))
		# TEXT_ProductDescription=isFind(re.search('(?<=Product description).+?(?=Product information)',dom))

		# for s in  keys:
		# 	if name.find(s)>=0:ifHasKey=s
		# 	if (TEXT_Aboutthisitem.find(s)>=0 or TEXT_Aboutthisitem.find(s)>=0 ):ifHasKey=True
		# 	if (TEXT_ProductDescription.find(s)>=0 or TEXT_ProductDescription.find(s)>=0 ):ifHasKey=True
			
		# ht=isFind(re.search('(?<=<div id="productDescription").+?(?=   </p>)', dom)).replace('\\n','').replace('\'','').replace(',','').replace('  ','')
		# ht= ht[ht.find('<p>'):-1]
		# band= re.search('(?<=<a id="bylineInfo" class="a-link-normal" href="/).+?(?=/b/)', dom)
	#    / band = band != None and band.group().strip() or 'None'
		price = re.search('(?<=class="a-size-medium a-color-price">).+?(?=</span>)', dom)
		price = price != None and price.group().strip() or 'None'
		reviews = re.search('(?<=title=").{0,5}(?=out of 5 stars)', dom)
		reviews = reviews != None and reviews.group().strip() or '0'
		if dom.find("Be the first to review this item")>0:reviews="0"
		s,reviewsNumber= re.split('id="acrCustomerReviewText" class="a-size-base">',dom),None
		reviewsNumber = len(s) > 1 and re.split(" ", s[1])[0] or 'None'
		AnsweredQuestions = re.search('(?<=">).{0,30}(?=answered)', dom)
		AnsweredQuestions = AnsweredQuestions != None and AnsweredQuestions.group().strip() or 0
		sea = re.findall("(?<=<span>#).+?(?=</span>)", dom)
		BigSellersRank, BigSellersRankTit, SamlSellersRankTit, SamlSellersRank = '0', 'None', 'None', 'None'
		try:
			if len(sea)>0:
				BigSellersRank = re.search('(?<=).{0,10}(?=in)', sea[0])
				BigSellersRank=BigSellersRank != None and BigSellersRank.group() or '0'
				BigSellersRankTit = re.search('(?<=in).+(?=\(<a)', sea[0])
				BigSellersRankTit=BigSellersRankTit != None and BigSellersRankTit.group()  or 'None'
			if len(sea)>=1:
				SamlSellersRankTit = re.findall("(?<='>).+?(?=</a>)", sea[-1])[-1]
				SamlSellersRankTit=SamlSellersRankTit != None and re.findall("(?<='>).+?(?=</a>)", sea[-1])[-1] or 'None'
				SamlSellersRank = re.search("(?<=).{0,10}(?=in)", sea[-1])
				SamlSellersRank = SamlSellersRank != None and SamlSellersRank.group() or 'None'
		except Exception:
			BigSellersRank = '0'
			BigSellersRankTit='None'
			SamlSellersRankTit = 'None'
			SamlSellersRank = '0'
		 
		try:	
			if len(list(DateFirstAvailable)) < 30  and DateFirstAvailable != 'None':
				ri = DateFirstAvailable.split(' ')[1]
				if  int(DateFirstAvailable.split(' ')[1].replace(',',''))<10:ri='0'+ DateFirstAvailable.split(' ')[1]
				if DateFirstAvailable.find('January')>=0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'01'+ri
				elif DateFirstAvailable.find('February') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'02'+ri
				elif DateFirstAvailable.find('March') >= 0:DateFirstAvailable = DateFirstAvailable.split(',')[1] + '03' + ri
				elif DateFirstAvailable.find('April') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'04'+ri
				elif DateFirstAvailable.find('May') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'05'+ri
				elif DateFirstAvailable.find('June') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'06'+ri
				elif DateFirstAvailable.find('July') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'07'+ri    
				elif DateFirstAvailable.find('August') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'08'+ri
				elif DateFirstAvailable.find('September') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'09'+ri
				elif DateFirstAvailable.find('October') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'10'+ri
				elif DateFirstAvailable.find('November') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'11'+ri
				elif DateFirstAvailable.find('December') >= 0:DateFirstAvailable=DateFirstAvailable.split(',')[1]+'12'+ri
						 
		except Exception:DateFirstAvailable=DateFirstAvailable
		# print  upc+' '+ asin+'    '+name+'  '+reviews+'  '+reviewsNumber+'  '+AnsweredQuestions+'  '+BigSellersRankTit+':'+BigSellersRank+'   '+SamlSellersRankTit+':'+SamlSellersRank+'  '+ IsCustom +'  '+DateFirstAvailable
		# if BigSellersRank=='0' and DateFirstAvailable!='None':
		# with open(asin,'a+',encoding='utf-8') as s:
		# 	s.write((dom))
		# 	s.close()
		# print(offers)
		return ([upc,isBuybox,asin,name.replace("'",'').replace(",",'').replace('\\','').strip(),price,reviews,reviewsNumber,Stock,str(AnsweredQuestions).replace('<span class="a-size-base">',''),BigSellersRankTit,BigSellersRank.replace(',',''),SamlSellersRankTit,SamlSellersRank.replace(',',''),DateFirstAvailable,offers,strct])
	except Exception as es:
		print (es)
		return None




def find_customer_reviews(html):
	dom=str(html).replace('\n','') 
	isFind= lambda x:x != None and x.group().strip() or 'None'
	five_star=isFind(re.search('(?<=5 stars represent ).+?\%',dom))
	four_star=isFind(re.search('(?<=4 stars represent ).+?\%',dom))
	three_star=isFind(re.search('(?<=3 stars represent ).+?\%',dom))
	two_star=isFind(re.search('(?<=2 stars represent ).+?\%',dom))
	one_star=isFind(re.search('(?<=1 stars represent ).+?\%',dom))

	return [five_star,four_star,three_star,two_star,one_star]
def findNeweggItem(html):
	dom=str(html).replace('\n','')
	isFind= lambda x:x != None and x.group().strip() or 'None'
	itemId, title,reviews,reviewsNumber,AnsweredQuestions ,isRefurbished='','','',0,0,True
	itemId=isFind(re.search('(?<=<em>).+?(?=</em>)', dom))
	title =isFind(re.search('(?<=class="mini-features-desc"><a href="#">).+?(?=</a></div>)', dom))
	reviews =isFind(re.search('(?<=title=").{0,5}(?=out of 5 eggs)' , dom))
	reviewsNumber =isFind(re.search('(?<=\(<span>).+?(?=</span>\))' , dom))
	AnsweredQuestions=isFind(re.search('(?<=\(<span>).+?(?=</span>\))' , dom))
	isRefurbished =dom.find('<title>Refurbished') >0 and True or False
	return [itemId,title,reviews,reviewsNumber,AnsweredQuestions ,isRefurbished]
#  <div id="productDescription" class="a-section a-spacing-small">
def findProductDescription(upcHtml ,asin):
	dom=str(upcHtml).replace('\n','')
	isFind= lambda x:x != None and x.group().strip() or 'None'
	ht=isFind(re.search('(?<=<div id="productDescription").+?(?=   </p>)', dom)).replace('\\n','').replace('\'','').replace(',','').replace('  ','')
	return ht[ht.find('<p>'):-1]

# def findToken(upcHtml ):
    # return 
if __name__ == "__main__":
	print 	(parse_AsinHtml(str(open('a.txt','r').readlines()) ,'12','1'))