from flask.ext.wtf import Form
from wtforms import TextField, RadioField, DateField, validators, PasswordField
from wtforms.validators import Required


class EditFortnoxInformation(Form):
    """
    A representation of the form for updating a Tenants Fortnox info.

    :param password: Tenants password for confirmation
    :param client_secret: Tenants client secret for Fortnox
    :param access_id: Tenants access id for Fortnox
    :type password: string (80)
    :type client_secret: string (200)
    :type access_id: string (200)
    """
    password = PasswordField('password', [validators.Length(max=80), validators.DataRequired()])
    client_secret = TextField('client_secret', [validators.Length(max=200), validators.DataRequired()])
    access_id = TextField('access_id', [validators.Length(max=200), validators.DataRequired()])