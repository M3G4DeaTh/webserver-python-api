from infrastructure import database
from flask import Flask
import jwt
import bcrypt
import json
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
        
def alterRegister(devicetag: str = None, newpassword: str = None):
    if devicetag != '' and newpassword != '' and devicetag != None and newpassword != None:
        token = jwt.encode({"tag": devicetag}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        try:
            deviceRegister = databaseOBJ.readRaw("SELECT password FROM devices WHERE tag = '"+str(tag)+"'")
            if deviceRegister != []:
                if bcrypt.checkpw(newpassword.encode(), deviceRegister[0][0].encode()):
                    response.headers['Error: '] = "password cannot be the same"
                    return response
                else:
                    hash = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt())
                    databaseOBJ.writeRaw("UPDATE devices SET password = '"+str(hash)+"' WHERE tag = '"+str(tag)+"' ")
                    return True
            else:
                try:
                    deviceRegister = databaseOBJ.readRaw("SELECT password FROM users WHERE tag = '"+str(tag)+"'")
                    if deviceRegister != []:
                        if bcrypt.checkpw(newpassword.encode(), deviceRegister[0][0].encode()):
                            response = Flask.make_response('Response')
                            response.headers['Error: '] = "password cannot be the same"
                            return response
                        else:
                            hash = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt())
                            databaseOBJ.writeRaw("UPDATE users SET password = '"+str(hash)+"' WHERE tag = '"+str(tag)+"' ")
                            return True
                    else:
                        return False
                except:
                    return False
        except:
            return False
        
def alterStatus(devicetag: str, status: str = None):
    try:
        status = bool(status)
        token = jwt.encode({"tag": devicetag}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        deviceRegister = databaseOBJ.readRaw("SELECT status FROM devices WHERE tag = '"+str(tag)+"'")
        if deviceRegister != []:
            databaseOBJ.writeRaw("UPDATE devices SET status= "+str(status)+" where tag = '"+str(tag)+"'")
            return True
        else:
            try:
                deviceRegister = databaseOBJ.readRaw("SELECT status FROM users WHERE tag = '"+str(tag)+"'")
                if deviceRegister != []:
                    databaseOBJ.writeRaw("UPDATE users SET status= "+str(status)+" where tag = '"+str(tag)+"'")
                    return True
                else:
                    return False
            except:
                response = Flask.make_response('Response')
                response.headers['Error: '] = "DeviceId invalid"
                return response
    except:
        response = Flask.make_response('Response')
        response.headers['Error: '] = "status invalid"
        return response
def alterStandard(devicetag: str, standard: str = None):
    try:
        standard = float(standard)
        token = jwt.encode({"tag": devicetag}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        if databaseOBJ.writeRaw("UPDATE devices SET standard = '"+str(standard)+"' WHERE tag = '"+str(tag)+"'"):
            response = Flask.make_response('Response')
            response.headers['Succes: '] = "standard changed"
            return response
        else:
            response = Flask.make_response('Response')
            response.headers['Error: '] = "DeviceId invalid"
            return response
    except:
        response = Flask.make_response('Response')
        response.headers['Error: '] = "standard invalid"
        return response
        
def getRegister():
    data = databaseOBJ.readRaw("SELECT id, tag, standard, status from devices order by id asc")
    register = {}
    if data != []:
        for i in range(len(data)):
            register[str(data[i][0])] = []
            register[str(data[i][0])].append(data[i][1])
        return json.dumps(register, indent=4)
    else:
        return False