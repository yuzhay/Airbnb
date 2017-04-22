class Thread:

    @staticmethod
    def create(db, **params):
        return db.execute(
            (
                "INSERT INTO threads "
                "(id, user_id, status, unread, responded, other_user_id, other_user_first_name, preview, updated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            ),
            (
                params['id'], params['user_id'], params['status'],
                params['unread'], params['responded'], params['other_user_id'],
                params['other_user_first_name'], params['preview'],
                params['updated_at']
            )
        )

    @staticmethod
    def exists(db, id):
        result = db.execute("SELECT id FROM threads WHERE id = %s", [id])
        return result.rowcount > 0

    @staticmethod
    def update(db, **params):
        return db.execute(
            (
                "UPDATE threads SET "
                "user_id = %s, status = %s, unread = %s, responded = %s, "
                "other_user_id = %s, other_user_first_name = %s, preview = %s, updated_at = %s "
                "WHERE id = %s"
            ),
            (
                params['user_id'], params['status'],
                params['unread'], params['responded'], params['other_user_id'],
                params['other_user_first_name'], params['preview'],
                params['updated_at'], params['id']
            )
        )

    @staticmethod
    def get_all(db):
        result = db.execute("SELECT * FROM threads")
        return result.fetchall()

    @staticmethod
    def update_or_create(db, **params):
        if Thread.exists(db, params['id']):
            Thread.update(db, **params)
        else:
            Thread.create(db, **params)
