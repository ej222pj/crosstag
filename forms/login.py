from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators


class Login(Form):
    """
    A representation of the form for login.

    :param Username: Username of a tenant.
    :param Password: Password of a tenant.
    """
    username = TextField('username', [validators.Length(max=80), validators.DataRequired()])
    password = PasswordField('password', [validators.Length(max=80), validators.DataRequired()])