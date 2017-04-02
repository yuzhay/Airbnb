class Listing:

    @staticmethod
    def create(db, id, name, user_id):
        return db.execute(
            "INSERT INTO listings (id, name, user_id) VALUES (%s, %s, %s);",
            (id, name, user_id)
        )

    @staticmethod
    def exists(db, id):
        result = db.execute("SELECT id FROM listings WHERE id = %s", [id])
        return result.rowcount > 0
