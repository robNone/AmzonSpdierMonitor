from sqlite import sqlite
import re



a="""B09MQK3V51
B08289199B
B09MT21QM9
B09ML7RF2W
B09MYQH5QW


			"""
   
   
   
for item in re.findall("B0.{8}",a) :
	sqlstr='DELETE from  ASINS where ASIN ="'+item+'" '
	sqlite().execute(sqlstr)
