from datetime import datetime


class SQLDetailedTagevent:
    """
        DetailedTagevent - This class is the representation of the database model DetailedTagevent.
    """
    def __init__(self, id=0, tag_id='', timestamp='', uid=0):
        """
        Called when creating a new DetailedTagevent class.

        :param id: Id of the event
        :param tag_id: The tag_id of the event
        :param timestamp: Time the event was created
        :param uid: Owner id of the event
        :type id: integer
        :type tag_id: string
        :type timestamp: datetime
        :type uid: foreign key, integer
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

