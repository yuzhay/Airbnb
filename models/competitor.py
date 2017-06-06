from models.model import Model

class Competitor(Model):
    """Competitor Model"""

    PRIMARY_KEY = ['room_id', 'date']
    TABLE_NAME = 'competitors'
