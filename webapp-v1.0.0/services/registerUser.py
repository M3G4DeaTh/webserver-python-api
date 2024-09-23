from infrastructure import database
import jwt
import bcrypt
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

def registerDevice(self):
    if isinstance(self, device.iotDevice):
        password = self.get_password()
        token = jwt.encode({"tag": str(self.get_tag())}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            databaseOBJ.writeRaw("INSERT INTO devices(tag, password, standard, status) VALUES('"+str(tag)+"', '"+str(hash)+"', '"+str(self.get_standard())+"', TRUE)")
            return True
        except:
            return False
    elif isinstance(self, users.users):
        password = self.get_password()
        token = jwt.encode({"tag": str(self.get_tag())}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            databaseOBJ.writeRaw("INSERT INTO users(tag, password, status) VALUES('"+str(tag)+"', '"+str(hash)+"', TRUE)")
            return True
        except:
            return False
        
def getRegister(self):
    if isinstance(self, device.iotDevice):
        deviceRegister = databaseOBJ.readRaw("SELECT tag, password, standard, status FROM devices WHERE ")
    elif isinstance(self, users.users):
