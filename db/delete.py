import pymysql
import os
import numpy as np

db = pymysql.connect("localhost", "root", "", "Students")
cursor = db.cursor()

cursor.execute("SELECT studentName FROM Students WHERE studentId='6500000'")
values = cursor.fetchall()

cursor.execute("DELETE FROM Students WHERE studentId='6500000'") 
db.commit()