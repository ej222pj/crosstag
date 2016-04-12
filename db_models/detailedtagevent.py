from flask import jsonify
from datetime import datetime
from crosstag_init import db
from db_models.user import User


class DetailedTagevent(db.Model):
    """
    DetailTagevent - A representation of the database model.
    """
    index = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime)
    uid = db.Column(db.Integer, db.ForeignKey('user.index'))

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
        return {'index': self.index, 'timestamp': str(self.timestamp),
                'tag_id': self.tag_id, 'uid': self.uid}

    def json(self):
        """

        :return: Json object of the dictionary representation
        :rtype: JSON
        """
        return jsonify(self.dict())
