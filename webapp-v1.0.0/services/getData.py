from infrastructure import database
from model import users
import os
import json

#Database configuration
#databaseOBJ=database.postgresDatabase(user=os.environ['DBUSER'], password=os.environ['DBPASSWORD'], host=os.environ['DBHOST'], dbname=os.environ['DBNAME'])
databaseOBJ=database.postgresDatabase(host='localhost')

def getAllData(self: users.users):
    if self.get_logged():
        data = databaseOBJ.readRaw("SELECT id, id_device, TO_CHAR(date, 'DD/MM/YY HH24:MI:SS'), input01, input02, input03, input04, status FROM log ORDER BY id asc limit 5")
        columnName = databaseOBJ.readRaw("SELECT column_name\
                                FROM information_schema.columns\
                                WHERE table_schema = 'public'\
                                AND table_name = 'log';")
        register = {}
        if data != []:
            for x in range(len(data)):
                for i in range(len(columnName)):
                    if str(columnName[i][0]) in register:
                        register[str(columnName[i][0])].append(data[x][i])
                    else:
                        register[str(columnName[i][0])] = []
                        register[str(columnName[i][0])].append(data[x][i])
        print(register)
        return json.dumps(register, indent=4)
    else:
        return "Not logged"



def getData(self: users.users, id: str):
    if self.get_logged():
        data = databaseOBJ.readRaw("SELECT id, id_device, TO_CHAR(date, 'DD/MM/YY HH24:MI:SS'), input01, input02, input03, input04, status FROM log WHERE id_device = "+id+" ORDER BY id asc limit 5")
        columnName = databaseOBJ.readRaw("SELECT column_name\
                                        FROM information_schema.columns\
                                        WHERE table_schema = 'public'\
                                        AND table_name = 'log';")
        register = {}
        if data != []:
            for i in range(len(columnName)):
                register[str(columnName[i][0])] = []
                register[str(columnName[i][0])].append(data[0][i])
            return json.dumps(register, indent=4)
        else:
            return "Register Not Found"
    else:
        return "Not Logged"
