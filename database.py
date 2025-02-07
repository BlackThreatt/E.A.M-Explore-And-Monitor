from dataclasses import field
from traceback import print_tb
import mysql.connector

class db:
    
    def __init__(self, user, host, password, database):
        try:
            self.db = mysql.connector.connect(user=user, host=host, password=password, database=database,  auth_plugin='mysql_native_password')
            self.cursor = self.db.cursor()
            print ('[result] Database connected!')
            
        except Exception as e:
            print ('[error] error connecting database!')
            print(e)

    def user(self, username, api):
        try:
            query = "select * from users where username='{}' and api_key='{}'".format(username, api)
            self.cursor.execute(query)
            output = self.cursor.fetchall()
            return output[0]
        except Exception as e:
            print('[error] ' + e)

    def get_apikeys(self):
        query = 'select api_key from users'
        self.cursor.execute(query)
        output = self.cursor.fetchall()
        dummy = []
        for api in output:
            dummy.append(api[0])
        return dummy

    def add_user(self, username, password, first_name, last_name, email, phone_number, api_key):
        
        try:
            query = "insert into users (username, password, first_name, last_name, email, phone_number, last_login, api_key) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', now(), '{6}');".format(username, password, first_name, last_name, email, phone_number, api_key)
            # print(query)
            self.cursor.execute(query)
            self.db.commit()
            return "success"
        except Exception as e:
            print( e)
    
    def update_values(self, apikey, fieldname, deviceID, temp, moisture, humidity, light):
        try:
            self.cursor.execute("select api_key from users;")
            output = self.cursor.fetchall()
            dummy = []
            for i in output:
                dummy.append(i[0])
            if apikey in dummy:
                
                query = 'insert into {0} (deviceID, temperature, moisture, humidity, light, date_time) values("{1}", {2}, 0, {3}, {4}, now());'.format(fieldname, deviceID, temp, humidity, light)
                self.cursor.execute(query)
                self.db.commit()
                query = 'update Node set temperature={0}, humidity={1}, light={2}, moisture=0 where deviceID="{3}";'.format(temp, humidity, light, deviceID)
                self.cursor.execute(query)
                self.db.commit()
                return True

            else:
                print("not available")

        except Exception as e:
            print("[ERROR!]")
            print(e)