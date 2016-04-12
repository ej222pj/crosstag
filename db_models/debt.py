from flask import jsonify
from datetime import datetime
from crosstag_init import db


class Debt(db.Model):
    """
        Debt - This class is the representation of the database model debt.

    """
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    product = db.Column(db.VARCHAR(60))
    create_date = db.Column(db.Date)

    def __init__(self, amount=None, uid=None, product=None, create_date=None):
        """
        Called when creating a new debt class.

        :param amount: The value of product
        :param uid: Id of the user
        :param product: Name of the product
        :param create_date: Timestamp of creation
        :type amount: integer
        :type uid: foreign key, integer
        :type product: varchar (60)
        :type create_date: date
        """
        self.amount = amount
        self.uid = uid
        self.product = product
        self.create_date = datetime.now()

    def dict(self):
        """
        :return: Dictionary representation of the class
        :rtype: Dictionary
        """
        return {'id': self.id,
                'amount': self.amount,
                'uid': self.uid,
                'product': self.product,
                'create_date': str(self.create_date)}

    def json(self):
        """

        :return: Json object of the dictionary representation
        :rtype: JSON
        """
        return jsonify(self.dict())
