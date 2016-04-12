from flask import jsonify
from datetime import datetime
from crosstag_init import db
from db_models.user import User


class Tagevent(db.Model):
    """
        Tagevent - A representation of the database model
    """
    tagid = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    amount = db.Column(db.Integer)
    clockstamp = db.Column(db.Integer)

    def __init__(self):
        """
        Called when creating a new Tagevent
        :return:
        """
        self.timestamp = datetime.now()
        self.clockstamp = self.timestamp.hour

    def dict(self):
        """

        :return: Dictionary representation of a tagevent
        :type: Dictionary
        """
        return {'tagid': self.tagid, 'timestamp': str(self.timestamp), 'amount': self.amount, 'clockstamp': str(self.clockstamp)}

    def json(self):
        """

        :return: Json object of the dictionary representation
        :rtype: JSON
        """
        return jsonify(self.dict())
