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
        try:
            standard = float(self.get_standard())
        except:
            return 'Invalid standard value!'
        hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            databaseOBJ.writeRaw("INSERT INTO devices(tag, password, standard, status) VALUES('"+str(tag)+"', '"+hash.decode()+"', '"+str(self.get_standard())+"', TRUE)")
            return 'New Device registered!'
        except:
            return 'Wrong data!'
    elif isinstance(self, users.users):
        password = self.get_password()
        token = jwt.encode({"tag": str(self.get_tag())}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            databaseOBJ.writeRaw("INSERT INTO users(tag, password, status) VALUES('"+str(tag)+"', '"+hash.decode()+"', TRUE)")
            return 'New User registered!'
        except:
            return 'Wrong data!'
        
def alterRegister(devicetag: str = None, newpassword: str = None):
    if devicetag != '' and newpassword != '' and devicetag != None and newpassword != None:
        token = jwt.encode({"tag": devicetag}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        try:
            deviceRegister = databaseOBJ.readRaw("SELECT password FROM devices WHERE tag = '"+str(tag)+"'")
            if deviceRegister != []:
                if bcrypt.checkpw(newpassword.encode(), deviceRegister[0][0].encode()):
                    return "Password cannot be the same"
                else:
                    hash = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt())
                    databaseOBJ.writeRaw("UPDATE devices SET password = '"+hash.decode()+"' WHERE tag = '"+str(tag)+"' ")
                    return 'Password updated!'
            else:
                try:
                    deviceRegister = databaseOBJ.readRaw("SELECT password FROM users WHERE tag = '"+str(tag)+"'")
                    if deviceRegister != []:
                        if bcrypt.checkpw(newpassword.encode(), deviceRegister[0][0].encode()):
                            return "Password cannot be the same"
                        else:
                            hash = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt())
                            databaseOBJ.writeRaw("UPDATE users SET password = '"+hash.decode()+"' WHERE tag = '"+str(tag)+"' ")
                            return 'Password updated!'
                    else:
                        return 'User not found!'
                except:
                    return 'Register not found!'
        except:
            return 'Register not found!'
        
def alterStatus(devicetag: str, status: str = None):
    try:
        status = int(status)
        return "status invalid"
    except:
        if status == 'True' or status == 'true':
            status = True
        elif status == 'False' or status == 'false':
            status = False
        else:
            return "status invalid"
        token = jwt.encode({"tag": devicetag}, "secret", algorithm="HS256")
        tag = token.split('.')
        tag = tag[1]
        deviceRegister = databaseOBJ.readRaw("SELECT status FROM devices WHERE tag = '"+str(tag)+"'")
        if deviceRegister != []:
            databaseOBJ.writeRaw("UPDATE devices SET status= "+str(status)+" where tag = '"+str(tag)+"'")
            return 'Status updated!'
        else:
            try:
                deviceRegister = databaseOBJ.readRaw("SELECT status FROM users WHERE tag = '"+str(tag)+"'")
                if deviceRegister != []:
                    databaseOBJ.writeRaw("UPDATE users SET status= "+str(status)+" where tag = '"+str(tag)+"'")
                    return 'Status updated!'
                else:
                    return 'Device not found!'
            except:
                return "DeviceId invalid"
    
def alterStandard(devicetag: str, standard: str = None):
    try:
        standard = float(standard)
    except:
        return "Invalid standard value!"
    token = jwt.encode({"tag": devicetag}, "secret", algorithm="HS256")
    tag = token.split('.')
    tag = tag[1]
    if databaseOBJ.writeRaw("UPDATE devices SET standard = '"+str(standard)+"' WHERE tag = '"+str(tag)+"'"):
        return "Standard changed"
    else:
        return "Invalid DeviceId!"
    
        
def getRegister():
    data = databaseOBJ.readRaw("SELECT id, tag, standard, status from devices order by id asc")

    register = {}
    if data != []:
        for i in range(len(data)):
            try:
                token = jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." + str(data[i][1]) + ".xq1bPmh_nulsbqL0UQdl4SOvCqU_s_4aHztWWKF51-w", "secret", algorithms=["HS256"])
            except Exception as e:
                print(e)
            register[str(data[i][0])] = []
            register[str(data[i][0])].append(token["tag"])
            register[str(data[i][0])].append(data[i][2])
            register[str(data[i][0])].append(data[i][3])
        return json.dumps(register, indent=4)
    else:
        return 'Error: id not Found'