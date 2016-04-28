from flask.ext.wtf import Form
from wtforms import TextField, RadioField, DateField, validators


class Register(Form):
    """
    A representation of the form for creating a new user.

    :param username: Username of the tenant
    :param password: password of the user.
    :param repeat_password: Repeted password
    :param active_fortnox: Does the tenant have fortnox.
    :param gym_name: Tenants gymname
    :param phone: Phonenumber of the tenant.
    :param address: Address of the tenant.
    :param zip_code: Zip code of the tenant.
    :param city: City of the tenant.
    :param email: email of the tenant.
    """
    username = TextField('username', [validators.Length(max=80), validators.DataRequired()])
    password = TextField('password', [validators.Length(max=80), validators.DataRequired()])
    repeat_password = TextField('repeat_password', [validators.Length(max=80), validators.DataRequired()])
    active_fortnox = RadioField('active_fortnox', [validators.DataRequired()], choices=[('Yes', 'true'), ('No', 'false')])
    gym_name = TextField('gym_name', [validators.Length(max=50), validators.DataRequired()])
    address = TextField('address', [validators.Length(max=50), validators.DataRequired()])
    phone = TextField('phone', [validators.Length(max=20), validators.DataRequired()])
    zip_code = TextField('zip_code', [validators.Length(max=20), validators.DataRequired()])
    city = TextField('city', [validators.Length(max=50), validators.DataRequired()])
    email = TextField('email', [validators.Length(max=50), validators.Email()])