from models.model import Model

class HostingActivity(Model):
    PRIMARY_KEY = ['year', 'month']
    TABLE_NAME = 'hosting_activities'