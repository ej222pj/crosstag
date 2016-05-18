from datetime import datetime

class SQLStatisticTagevent:
    """
        StatisticTagevent - This class is the representation of the database model StatisticTagevent.
    """
    def __init__(self, id=0, timestamp='', amount=0, clockstamp=0):
        """
        Called when creating a new StatisticTagevent class.

        :param id: Id of the evnet
        :param timestamp: Time the event was created
        :param amount: How many times the event occurred in 1 hour
        :param clockstamp: What hour the event as created
        :type id: integer
        :type timestamp: datetime
        :type amount: integer
        :type clockstamp: integer
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
        :return: Dictionary representation of the class
        :rtype: Dictionary
        """
        return {'id': str(self.id),
                'timestamp': self.timestamp,
                'amount': str(self.amount),
                'clockstamp': str(self.clockstamp)}
