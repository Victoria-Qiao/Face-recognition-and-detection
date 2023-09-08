import pymysql
import os
import numpy as np

db = pymysql.connect("localhost", "root", "", "Students",password = "XIAOLAN12conan")
vector = []
sid = []
try:
	with db.cursor() as cursor:
		sql = "select matrix,studentId from students"
		cursor.execute(sql)
		result = cursor.fetchall()
		for i in result:
			h = np.frombuffer(i[0],dtype = np.float64)
			vector.append(h)
			sid.append(i[1])
		vector = np.array(vector)

finally:
	db.close()
