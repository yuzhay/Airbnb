
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
