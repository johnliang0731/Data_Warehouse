import pymysql

db = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456')

cursor = db.cursor()

cursor.execute("CREATE TABLE test (id int PRIMARY KEY, name varchar(20));")

data = cursor.fetchone()

print("Database version : %s " % data)

db.close()