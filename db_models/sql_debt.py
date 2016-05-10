from datetime import datetime


class SQLDebt:
    """
        Debt - This class is the representation of the database model debt.

    """
    def __init__(self, amount, uid, product, create_date=None, id=0):
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
        self.id = id
        self.amount = amount
        self.uid = uid
        self.product = product
        self.create_date = create_date
        if self.create_date is None:
            self.create_date = datetime.now()
        if self.id is None:
            self.id = 0

    def dict(self):
        """
        :return: Dictionary representation of the class
        :rtype: Dictionary
        """
        return {'id': str(self.id),
                'amount': str(self.amount),
                'uid': str(self.uid),
                'product': self.product,
                'create_date': str(self.create_date)}
