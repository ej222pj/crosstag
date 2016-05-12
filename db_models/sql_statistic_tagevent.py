from datetime import datetime


class SQLStatisticTagevent:
    """
    StatisticTagevent - A representation of the database model.
    """
    def __init__(self, id=0, timestamp='', amount=0, clockstamp=0):
        """
        Called when creating a new Statistictagevent

        """

        self.id = id
        self.timestamp = datetime.now()
        self.amount = amount
        self.clockstamp = clockstamp

    def dict(self):
        """

        :return: Dictionary representation of the tag class
        :rtype: Dictionary
        """
        return {'id': str(self.id),
                'timestamp': str(self.timestamp),
                'amount': str(self.amount),
                'clockstamp': str(self.clockstamp)}
