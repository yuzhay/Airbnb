class Listing:

    @staticmethod
    def create(db, **params):
        return db.execute(
            "INSERT INTO listings (id, name, user_id) VALUES (%s, %s, %s);",
            (params['id'], params['name'], params['user_id'])
        )

    @staticmethod
    def exists(db, id):
        result = db.execute("SELECT id FROM listings WHERE id = %s", [id])
        return result.rowcount > 0

    @staticmethod
    def update(db, **params):
        return db.execute(
            "UPDATE listings SET name = %s, user_id = %s WHERE id = %s;",
            (params['name'], params['user_id'], params['id'])
        )

    @staticmethod
    def update_or_create(db, **params):
        if Listing.exists(db, params['id']):
            Listing.update(db, **params)
        else:
            Listing.create(db, **params)
