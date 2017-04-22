
class User:

    @staticmethod
    def create(db, **params):
        return db.execute(
            "INSERT INTO users (id, first_name, last_name) VALUES (%s, %s, %s);",
            (params['id'], params['first_name'], params['last_name'])
        )

    @staticmethod
    def exists(db, id):
        result = db.execute("SELECT id FROM users WHERE id = %s", [id])
        return result.rowcount > 0

    @staticmethod
    def update(db, **params):
        return db.execute(
            "UPDATE users SET first_name = %s, last_name = %s WHERE id = %s;",
            (params['first_name'], params['last_name'], params['id'])
        )

    @staticmethod
    def update_or_create(db, **params):
        if User.exists(db, params['id']):
            User.update(db, **params)
        else:
            User.create(db, **params)
