from flask.ext.wtf import Form
from wtforms import TextField


class SearchUser(Form):
    """
    A representation of the form for searching a user.

    :param index: Index of the user in the database.
    :param name: Name of the user.
    :param email: Emailaddress of the user.
    :param phone: Phonenumber of the user.
    :param fortnox_id: Fortnox number of the user.
    """
    index = TextField('name', validators=[])
    name = TextField('name', validators=[])
    email = TextField('email', validators=[])
    phone = TextField('phone', validators=[])
    fortnox_id = TextField('fortnox_id', validators=[])
