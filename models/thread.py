class Thread:

    @staticmethod
    def create(db, id, user_id, status, unread, responded, other_user_id,
        other_user_first_name, preview, updated_at):
        return db.execute(
            "INSERT INTO threads "
            + "(id, user_id, status, unread, responded, other_user_id, other_user_first_name, preview, updated_at) "
            + "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
            (id, user_id, status, unread, responded, other_user_id, other_user_first_name, preview, updated_at)
        )

    @staticmethod
    def exists(db, id):
        result = db.execute("SELECT id FROM threads WHERE id = %s", [id])
        return result.rowcount > 0
