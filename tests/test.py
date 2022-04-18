from passlib.hash import sha512_crypt as sha
password = sha.hash("password123")
print(password)
from database import db

mydb = db('dbuser', '127.0.0.1', 'dbpass', 'ARMS')
query = "update users set password = '{}' where username = 'amansingh'".format(password)

mydb.cursor.execute(query)
mydb.db.commit()