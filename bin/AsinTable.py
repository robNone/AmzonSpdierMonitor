from ast import Delete
import sys
import  parse_ret 
sys.path.append('../db/')
from sqlite import sqlite


def Add_Asin_dao(asin_list,asin_type):
	for asin in asin_list:
		sqlstr='INSERT INTO ASINS VALUES ("'+asin+'" ,'+(asin_type)+')'
		try:
			sqlite().execute(sqlstr)
		except Exception as es :pass
	return count_Asin_dao()

def count_Asin_dao():
	sqlstr='select count(*)from ASINS '
	try:
		#2
		return	(sqlite().select(sqlstr))
	except Exception as es :pass
	return '1' 


def findAll_Asin_dao( asinType):
	sqlstr='select *from ASINS  where asinType ='+asinType
	try:
		return	(sqlite().select(sqlstr))
	except Exception as es :pass
	return '1' 

def Remove_Asin_dao(asin_list):
	for asin in asin_list:
		
		sqlstr='DELETE from ASINS where asin== "'+asin+'"'
		try:
			sqlite().execute(sqlstr)
		except Exception as es :pass
	return count_Asin_dao()

def find_Asin_dao(asin):
	sqlstr='select*from asinTable where asin="'+asin+'"  and asinType='
	return	parse_ret.parse_Asins(sqlite().select(sqlstr))
