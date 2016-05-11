from flask.ext.wtf import Form
from wtforms import TextField


class SearchUser(Form):
    """
    A representation of the form for searching a user.

    :param firstname: Firstname of the user.
    :param lastname: Lastname of the user.
    :param city: City of the user.
    :param email: Emailaddress of the user.
    """

    firstname = TextField('firstname', validators=[])
    lastname = TextField('lastname', validators=[])
    city = TextField('email', validators=[])
    email = TextField('email', validators=[])
