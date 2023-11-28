import sqlite3 ,sys

class sqlite(object):
	def __init__(self):
		self.dbName = 'G:/search/File/asin.db'
		self.comm=None
		self.cursor = None
	def dbClose(self):
		self.cursor.close()
		self.comm.close()
		
	def dbCon(self):
		self.comm = sqlite3.connect(self.dbName)
		self.cursor = self.comm.cursor()
	def select(self,sql):
		# print (sql)
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
	print  (sqlite().execute('INSERT INTO asinTable VALUES ("B09DN3H6KX","False","2021 Oculus Quest 2 All-In-One VR Headset 128GB, Touch Controllers, 1832x1920 up to 90 Hz Refresh Rate LCD, Mytrix Carrying Case, Earphone, Link Cable, Gray Grip Cover, Lens Cover, Silicone Face Cover","399.00","N","N","N","0","Tue Nov 16 13:11:58 2021","Brand: O C U L U S","#11,239 in Video Games #154 in GEM Box Microconsole#198 in PC Virtual Reality Headsets","True","NoBuybox","Tue Nov 16 12:19:17 2021","N")'))
