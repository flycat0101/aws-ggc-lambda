#!/usr/bin/python
import sys
import commands
from datetime import *
import time

import MySQLdb
import _mysql_exceptions

DB_HOST = "greengrass.co4tctnwmzmy.us-west-2.rds.amazonaws.com"
DB_PORT = 3306
DB_USERNAME = "root"
DB_PASSWORD = "PdXnW947JGYVWxDbXbn2BMpNWihHmcSr"
DB_DATABASE = "greengrass"

class InsertData:
	def insert_data(self, line):
		try:
			db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
		except _mysql_exceptions.OperationalError as e:
			print "Connection fails"
			return 0
		line = line.strip('\n')
		line = line.split(",")
		temp = line[0]
		time = line[1]
		sql = "INSERT INTO data VALUES (null, %s, %s)" % (temp, time)
		print sql
		cursor = db.cursor()

		try:
			cursor.execute(sql)
			db.commit()
		except:
			print "Insert sql fails"
			db.rollback()
			return 0
		finally:
			db.close()
			return 1

	def check_data(self, temp_dt):
		ret = 1
		number = 0
		f = open("/tmp/temp_data.txt","a+")
		lines = f.readlines()
		f.close()
		for line in lines:
			ret = self.insert_data(line)
			if ret == 0:
				break
			number = number + 1

	        if ret == 0:
			f = open("/tmp/temp_data.txt","w")
			for line in lines[number:]:
               			f.write(line)
			f.close()

		if ret == 1:
			f = open("/tmp/temp_data.txt","w")
			f.truncate(0)
			f.close()

#		dt = datetime.today()
#		datet = dt.strftime('%Y-%m-%d %H:%M:%S')
#		ret = self.insert_data(str(temp) + "," + "\"" + datet + "\"")
		ret = self.insert_data(temp_dt)
		if ret == 0:
			f = open("/tmp/temp_data.txt","a+")
			f.write(temp_dt)
               		f.write('\n')
       			f.close()

if __name__ == '__main__':
	insert = InsertData()
	insert.check_data(sys.argv[1])
