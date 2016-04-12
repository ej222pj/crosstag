from flask.ext.wtf import Form
from wtforms import TextField, validators, IntegerField


class NewDebt(Form):
    """
    A representation of the form for creating a new debt.

    :param amount: Value of the product cost.
    :param product: Name of the product.
    :type amount: Integer
    :type amount: String (60)
    """
    amount = IntegerField('amount', validators=[])
    product = TextField('product', [validators.Length(max=60), validators.DataRequired()])
