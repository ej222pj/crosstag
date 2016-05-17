from datetime import datetime
from crosstag_init import db
from db_models.user import User


class SQLStatisticTagevent:
    """
        Tagevent - A representation of the database model
    """
    def __init__(self, id=0, timestamp='', amount=0, clockstamp=0):
        """
        Called when creating a new Tagevent
        :return:
        """
        self.id = id
        self.timestamp = timestamp
        self.amount = amount
        self.clockstamp = clockstamp
        if self.id is None:
            self.id = 0
        if self.amount is None:
            self.amount = 0
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.clockstamp is None:
            self.clockstamp = self.timestamp.hour

    def dict(self):
        """

        :return: Dictionary representation of a tagevent
        :type: Dictionary
        """
        return {'id': str(self.id), 'timestamp': self.timestamp, 'amount': str(self.amount), 'clockstamp': str(self.clockstamp)}
