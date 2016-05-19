from flask.ext.wtf import Form
from wtforms import TextField, validators, IntegerField


class NewDebt(Form):
    """
    A representation of the form for creating a new debt.

    :param amount: Value of the product cost.
    :param product: Name of the product.
    :type amount: integer
    :type product: string (60)
    """
    amount = IntegerField('amount', [validators.DataRequired(message='Amount is required and must be a number')])
    product = TextField('product', [validators.Length(max=60, message='Product name is to long, 60 characters is maximum'),
                                    validators.DataRequired(message='Product is required')])
