import random
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
 	
	"October":10,	
	"November":11,	
	"December":12,	
 
}
timeStr=''
Deliver='FREE delivery September 9 - 12. Order within 12 hrs 6 mins. Details'
i=True
if Deliver.find("fastest delivery")>=0:
	timeStr=Deliver.split("fastest delivery")[1].split('.')[0]
	i==False
else:
						
	timeStr=Deliver.replace("FREE delivery",'').split('.')[0]
day=str(timeStr.strip().split(' ')[-1])
if timeStr.find(',')<0:
	month=timeStr.strip().split(' ')[0].strip()
else:
	month=timeStr.strip().split(',')[1].strip().split(' ')[0]
if i and timeStr.find('-')>=0:
	od= timeStr.split('-')[0].split(' ')[-2]
	om=timeStr.split('-')[0].split(' ')[-3]
	timeStr='2022/'+str(DATADIC[om])+"/"+od +"-"+ '2022/'+str(DATADIC[month])+"/"+day 
else:
	timeStr='2022/'+str(DATADIC[month])+"/"+day
print(timeStr)