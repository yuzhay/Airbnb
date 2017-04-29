from models.model import Model

class HostEarning(Model):
    PRIMARY_KEY = ['year', 'month']
    TABLE_NAME = 'host_earnings'
