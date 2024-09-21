from infrastructure import database
import jwt
from model import device
from model import users
#Database configuration
#databaseOBJ=database.postgresDatabase(user=os.environ['DBUSER'], password=os.environ['DBPASSWORD'], host=os.environ['DBHOST'], dbname=os.environ['DBNAME'])
databaseOBJ=database.postgresDatabase(host='localhost')

def userValid(self):
    if isinstance(self, device.iotDevice):
        token = jwt.encode({"tag": str(self.get_tag())}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        verify = databaseOBJ.readRaw("select password, status from devices where tag='" + tag+ "';")
        if verify != [] and verify != '':
            return True
        else:
            return False
    elif isinstance(self, users.users):
        token = jwt.encode({"tag": str(self.get_tag())}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        verify = databaseOBJ.readRaw("select password, status from users where tag='" + tag+ "';")
        if verify != [] and verify != '':
            return True
        else:
            return False

def registerDevice(tag: str, password: str):
