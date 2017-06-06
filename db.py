import psycopg2

class Db(object):
    """Database driver"""

    _conn = None
    _cur = None

    def __init__(self, dbname, user, password, host='localhost'):
        try:
            self._conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
            self._conn.autocommit = True
        except psycopg2.OperationalError:
            print("Can't connect to the database")

        self._cur = self._conn.cursor()

    def __del__(self):
        self._conn.close()


    def execute(self, query, params=None):
        try:
            self._cur.execute(query, params)
        except:
            print("Can't execute '{0}'".format(query))

        return self._cur


    def executemany(self, query, params=None):
        try:
            self._cur.executemany(query, params)
        except:
            print("Can't execute many'{0}'".format(query))

        return self._cur
