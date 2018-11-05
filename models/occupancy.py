from models.model import Model

class Occupancy(Model):
  PRIMARY_KEY = ['listing_id', 'year', 'month']
  TABLE_NAME = 'occupancy'
