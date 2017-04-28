class Model:
    TABLE_NAME = None

    @classmethod
    def __columns_string(params):
        return ', '.join('{}'.format(key) for key in params.keys())

    @classmethod
    def __column_value_string(params):
        return ', '.join('{0}={1}'.format(key, value) for key, value in params.items())

    @classmethod
    def __column_value_and_string(params):
        return ' AND '.join('{0}={1}'.format(key, value) for key, value in params.items())

    @classmethod
    def create(cls, db, **params):
        columns = cls.__columns(params)
        values = ', '.join('{}'.format('%s') for value in params.values())
        query = "INSERT INTO {0} ({1}) VALUES({2});".format(cls.TABLE_NAME, columns, values)
        return db.execute(query,params.values())

    @classmethod
    def exists(cls, db, **params):
        cause = __column_value_and_string(params)
        query = "SELECT * FROM {0} WHERE {1}".format(cls.TABLE_NAME, cause)
        result = db.execute(query, params.values())
        return result.rowcount > 0

    @staticmethod
    def update(db, **params):
        # return db.execute(
        #     "UPDATE users SET first_name = %s, last_name = %s WHERE id = %s;",
        #     (params['first_name'], params['last_name'], params['id'])
        # )
        1

    @staticmethod
    def update_or_create(db, **params):
        # if User.exists(db, params['id']):
        #     User.update(db, **params)
        # else:
        #     User.create(db, **params)
        1
