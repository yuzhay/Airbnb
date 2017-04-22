
class User:

    @staticmethod
    def create(db, id, first_name, last_name):
        return db.execute(
            "INSERT INTO users (id, first_name, last_name) VALUES (%s, %s, %s);",
            (id, first_name, last_name)
        )

    @staticmethod
    def exists(db, id):
        result = db.execute("SELECT id FROM users WHERE id = %s", [id])
        return result.rowcount > 0

    @staticmethod
    def update(db, id, first_name, last_name):
        return db.execute(
            "UPDATE users SET first_name = %s, last_name = %s WHERE id = %s;",
            (first_name, last_name, id)
        )

    @staticmethod
    def update_or_create(db, id, first_name, last_name):
        if User.exists(db, id):
            User.update(db, id, first_name, last_name)
        else:
            User.create(db, id, first_name, last_name)
