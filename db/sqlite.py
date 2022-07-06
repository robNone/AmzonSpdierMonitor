# -*- coding: utf-8 -*-
import sqlite3 ,sys

class sqlite(object):
	def __init__(self):
		# self.dbName = '/root/search/File/asin.db'
		self.dbName = '/root/DB/asin.db'
		# self.dbName = 'G:/search/File/asin.db'
		self.comm=None
		self.cursor = None
	def dbClose(self):
		self.cursor.close()
		self.comm.close()
		
	def dbCon(self):
		self.comm = sqlite3.connect(self.dbName)
		self.cursor = self.comm.cursor()
	def select(self,sql):
		self.dbCon()
		self.cursor.execute(sql)
		values = self.cursor.fetchall()
		self.dbClose()
		return values
	def execute(self,sql):
		# print (sql)
		self.dbCon()
		self.cursor.execute(sql)
		self.comm.commit()
		self.dbClose()
if __name__ == "__main__":
	print  (sqlite().select("select * from asinTable"))
