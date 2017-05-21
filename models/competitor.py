from models.model import Model

class Competitor(Model):
    PRIMARY_KEY = ['room_id', 'date']
    TABLE_NAME = 'competitors'
