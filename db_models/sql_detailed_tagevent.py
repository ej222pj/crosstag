from datetime import datetime


class SQLDetailedTagevent:
    """
    DetailTagevent - A representation of the database model.
    """
    def __init__(self, tag):
        """
        Called when creating a new Detailedtagevent

        :param tag: Tagnumber of the tag
        :type tag: String (20)
        """
        self.tag_id = tag
        self.timestamp = datetime.now()
        users = User.query.filter_by(tag_id=self.tag_id)
        js = None
        for user in users:
            js = user.dict()

        if js is not None:
            self.uid = js['index']

    def dict(self):
        """

        :return: Dictionary representation of the tag class
        :rtype: Dictionary
        """
        return {'id': str(self.id), 'timestamp': str(self.timestamp),
                'tag_id': self.tag_id, 'uid': str(self.uid)}

