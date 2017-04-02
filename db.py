import psycopg2

class Db(object):
    _conn = None
    _cur = None

    def __init__(self, dbname, user, password, host = 'localhost'):
        try:
            self._conn=psycopg2.connect(f"dbname='{dbname}' user='{user}' password='{password}'")
            self._conn.autocommit = True
        except:
            print("Can't connect to the database")
        self._cur = self._conn.cursor()

    def __del__(self):
        self._conn.close()


    def execute(self, query, params = None):
        #try:
        self._cur.execute(query, params)
        #except:
            #print(f"Can't execute '{query}'")

        return self._cur


    def executemany(self, query, vars = None):
        try:
            self._cur.executemany(query, params)
        except:
            print(f"Can't execute many'{query}'")

        return self._cur
