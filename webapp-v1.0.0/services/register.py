from infrastructure import database
from datetime import datetime
from model import device
# date capture
now = datetime.now()
#Database configuration
#databaseOBJ=database.postgresDatabase(user=os.environ['DBUSER'], password=os.environ['DBPASSWORD'], host=os.environ['DBHOST'], dbname=os.environ['DBNAME'])
databaseOBJ=database.postgresDatabase(host='localhost')

# Services
def statusVerify(self: device.iotDevice):
    if self.get_logged() == True:
        try:
            tagVerify = databaseOBJ.readRaw("SELECT standard FROM devices WHERE tag ='"+self.get_tag()+"'")
        except:
            return False
        if self.get_input01() >= float(tagVerify[0][0]) and self.get_input02() >= float(tagVerify[0][0]) and self.get_input03() >= float(tagVerify[0][0]) and self.get_input04() >= float(tagVerify[0][0]):
            self.set_status(True)
            return True
        else:
            self.set_status(False)
            return False
    else:
        return False
        
def dataRegister(self: device.iotDevice):
    if self.get_logged() == True:
        if self.get_status() != '' and self.get_status() != []:
            try:
                databaseOBJ.writeRaw("INSERT INTO log(id_device, input01, input02, input03, input04, date, status) values((select id from devices where tag = '"+self.get_tag()+"'), "+str(self.get_input01())+", "+str(self.get_input02())+", "+str(self.get_input03())+", "+str(self.get_input04())+", '"+str(now)+"', '"+str(self.get_status())+"')")
                return True
            except:
                return False
        else:
            return False
    else:
        return False
    
    