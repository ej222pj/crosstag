from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators


class Login(Form):
    """
    A representation of the form for login.

    :param Username: Username of a tenant.
    :param Password: Password of a tenant.
    """
    username = TextField('username', [validators.Length(max=80, message='Username is to long, 80 characters is maximum'),
                                      validators.DataRequired(message='Username is required')])
    password = PasswordField('password', [validators.Length(max=80, message='Password is to long, 80 characters is maximum'),
                                          validators.DataRequired(message='Password is required')])