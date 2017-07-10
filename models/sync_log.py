from datetime import datetime, date, time, timedelta


class SyncLog:

    @staticmethod
    def start(database, started_at=datetime.now()):
        return database.execute("INSERT INTO sync_log (started_at) VALUES (%s);", [started_at])

    @staticmethod
    def finish(database, ended_at=datetime.now()):
        return database.execute(
            "UPDATE sync_log SET ended_at = %s WHERE id = (SELECT MAX(id) FROM sync_log);", [
                ended_at]
        )
