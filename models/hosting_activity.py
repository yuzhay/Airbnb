
class HostingActivity:

    @staticmethod
    def create(db, **params):
        return db.execute(
            (
                "INSERT INTO host_activities "
                    "(year, month, nights_booked,  nights_unbooked, occupancy_rate, "
                    "nights_price_min, nights_price_max, cleaning_fees) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            ),
            (
                params['year'], params['month'], params['nights_booked'],
                params['nights_unbooked'], params['occupancy_rate'],
                params['nights_price_min'], params['nights_price_max'],
                params['cleaning_fees']
            )
        )

    @staticmethod
    def exists(db, year, month):
        result = db.execute("SELECT year, month FROM host_activities WHERE year = %s AND month = %s", [year, month])
        return result.rowcount > 0

    @staticmethod
    def update(db, **params):
        return db.execute(
            (
                "UPDATE host_activities SET nights_booked=%s,  "
                "nights_unbooked=%s, occupancy_rate=%s, nights_price_min=%s, "
                "nights_price_max=%s, cleaning_fees=%s WHERE year = %s AND month = %s;"
            ),
            (
                params['nights_booked'],
                params['nights_unbooked'], params['occupancy_rate'],
                params['nights_price_min'], params['nights_price_max'],
                params['cleaning_fees'], params['year'], params['month']
            )
        )

    @staticmethod
    def update_or_create(db, **params):
        if HostingActivity.exists(db, params['year'], params['month']):
            HostingActivity.update(db, **params)
        else:
            HostingActivity.create(db, **params)
