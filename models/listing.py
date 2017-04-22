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

    @staticmethod
    def update(db, id, name, user_id):
        return db.execute(
            "UPDATE listings SET name = %s, user_id = %s WHERE id = %s;",
            (name, user_id, id)
        )

    @staticmethod
    def update_or_create(db, id, name, user_id):
        if Listing.exists(db, id):
            Listing.update(db, id, name, user_id)
        else:
            Listing.create(db, id, name, user_id)
