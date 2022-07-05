# -*- coding: utf-8 -*-
import json ,time

def  parse_Asins(asinList):
    js=[]
    for Asin,isDoge,title,price ,reviewe,storeName,storeId ,offers,dTime ,brand,ranks,isbuybox,us,Change_time ,d_time  in asinList:
        asinDic={}
        asinDic['Asin']=Asin
        asinDic['isDoge']=isDoge
        asinDic['title']=title
        if price!="None":
            asinDic['price']=float(price)
        else:
            asinDic['price']=-1
        asinDic['reviewe']=reviewe
        asinDic['storeName']=storeName
        asinDic['storeId']=storeId
        asinDic['offers']=offers
        asinDic['dTime']=time.mktime(time.strptime(dTime, '%a %b %d %H:%M:%S %Y'))
        asinDic['brand']=brand
        asinDic['ranks']=ranks
        asinDic['isbuybox']=isbuybox
        asinDic['us']=us
        if Change_time!=""and Change_time!="N":
            Change_time=time.mktime(time.strptime(Change_time, '%a %b %d %H:%M:%S %Y'))
        asinDic['Change_time']=Change_time
        if d_time!=""and d_time!="N":
            d_time=time.mktime(time.strptime(d_time, '%a %b %d %H:%M:%S %Y')        )
        asinDic['d_time']=d_time
        js.append(asinDic)
    return json.dumps(js)
    