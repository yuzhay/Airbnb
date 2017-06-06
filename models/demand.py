from models.model import Model

class Demand(Model):
    PRIMARY_KEY = ['listing_id', 'date']
    TABLE_NAME = 'demands'
