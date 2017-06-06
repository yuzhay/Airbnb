from models.model import Model

class ReservationRequest(Model):
    PRIMARY_KEY = ['id']
    TABLE_NAME = 'reservation_requests'
