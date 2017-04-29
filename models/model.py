class Model:
    TABLE_NAME = None
    PRIMARY_KEY = None

    @classmethod
    def create(cls, db, **params):
        columns = cls.__columns_string(params)
        values = ', '.join('{}'.format('%s') for value in params.values())
        query = "INSERT INTO {0} ({1}) VALUES({2});".format(cls.TABLE_NAME, columns, values)
        print(list(params.values()))
        return db.execute(query,list(params.values()))

    @classmethod
    def exists(cls, db, **params):
        primary_key = cls.__primary_key(params)
        primary_key_cause = cls.__column_value_and_string(primary_key)

        query = "SELECT * FROM {0} WHERE {1}".format(cls.TABLE_NAME, primary_key_cause)
        result = db.execute(query, list(params.values()))
        return result.rowcount > 0

    @classmethod
    def update(cls, db, **params):
        query = "UPDATE {0} SET {1} WHERE {2};"
        primary_key = cls.__primary_key(params)
        primary_key_cause = cls.__column_value_and_string(primary_key)
        query = query.format(
            cls.TABLE_NAME,
            cls.__column_value_string(params),
            primary_key_cause
        )

        return db.execute(query, list(params.values()))

    @classmethod
    def update_or_create(cls, db, **params):
        if cls.exists(db, **params):
            cls.update(db, **params)
        else:
            cls.create(db, **params)

    @classmethod
    def get(cls, db, **params):
        return cls.__select(db, **params).fetchone()

    @classmethod
    def __columns_string(cls, params):
        return ', '.join('{}'.format(key) for key in params.keys())

    @classmethod
    def __column_value_string(cls, params):
        return ', '.join('{0}=%s'.format(key, value) for key, value in params.items())

    @classmethod
    def __column_value_and_string(cls, params):
        return ' AND '.join('{0}={1}'.format(key, value) for key, value in params.items())

    @classmethod
    def __primary_key(cls, params):
        primary_key = {}
        for key in cls.PRIMARY_KEY:
            primary_key[key] = params[key]
        return primary_key

    @classmethod
    def __select(cls, db, **params):
        query = "SELECT * FROM {0} WHERE {1};"
        primary_key = cls.__primary_key(params)
        primary_key_cause = cls.__column_value_and_string(primary_key)
        query = query.format(cls.TABLE_NAME, primary_key_cause)

        result = db.execute(query, list(params.values()))
        return result
