from models.model import Model

class Reservation(Model):
  PRIMARY_KEY = ['confirmation_code']
  TABLE_NAME = 'reservations'
