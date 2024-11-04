
import psycopg2
from psycopg2.extras import RealDictCursor

class postgresDatabase():
    def __init__(self, user='postgres', password='postgres', host='localhost', dbname='postgres'):
        self.lastError = None
        self.connectionString="user="+user+" password="+password+" host="+host+" dbname="+dbname

    def readRaw(self, sql, realdict=False):
        try:
            conn = psycopg2.connect(self.connectionString)
            if realdict:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql)
                data = cur.fetchall()
            else:
                cur = conn.cursor()
                cur.execute(sql)
                data = [list(row) for row in cur.fetchall()]
            cur.close()
            conn.close()
            return data
        except Exception as e:
            self.lastError = e
            return []

    def writeRaw(self, sql):
        try:
            conn = psycopg2.connect(self.connectionString)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()   
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(e)
            self.lastError = e
            return False
