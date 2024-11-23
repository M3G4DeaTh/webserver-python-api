import jwt
import bcrypt
import os
from infrastructure import database
from model import device
from model import users


#Database configuration
databaseOBJ=database.postgresDatabase(user=os.environ['DBUSER'], password=os.environ['DBPASSWORD'], host=os.environ['DBHOST'], dbname=os.environ['DBNAME'])
# databaseOBJ=database.postgresDatabase(host='localhost')


def login(self):
    if isinstance(self, device.iotDevice):
        password = self.get_password()
        token = jwt.encode({"tag": str(self.get_tag())}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        
        credentials = databaseOBJ.readRaw("select password, status from devices where tag='" + tag+ "';")
    elif isinstance(self, users.users):
        password = self.get_password()
        token = jwt.encode({"tag": str(self.get_tag())}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        print(tag)
        credentials = databaseOBJ.readRaw("select password, status from users where tag='" + tag+ "';")
    if credentials != []:
        
        if bcrypt.checkpw(password.encode(), credentials[0][0].encode()) and bool(credentials[0][1]):
            print(credentials)
            self.set_logged(True)
            
            return True
        else:
            
            self.set_logged(False)
            return False
    else:
        self.set_logged(False)
        return False
            
