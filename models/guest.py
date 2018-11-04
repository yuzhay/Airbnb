from models.model import Model

class Guest(Model):
  PRIMARY_KEY = ['id']
  TABLE_NAME = 'guests'
