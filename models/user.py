from models.model import Model

class User(Model):
  PRIMARY_KEY = ['id']
  TABLE_NAME = 'users'
