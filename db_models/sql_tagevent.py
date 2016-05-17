from datetime import datetime


class SQLDetailedTagevent:
    """
    DetailedTagevent - A representation of the database model.
    """
    def __init__(self, id=0, tag_id='', timestamp='', uid=0):
        """
        Called when creating a new Detailedtagevent

        """

        self.id = id
        self.tag_id = tag_id
        self.timestamp = timestamp
        self.uid = uid

        if self.id is None:
            self.id = 0
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def dict(self):
        """

        :return: Dictionary representation of the tag class
        :rtype: Dictionary
        """
        return {'id': str(self.id),
                'tag_id': self.tag_id,
                'timestamp': str(self.timestamp),
                'uid': str(self.uid)}

