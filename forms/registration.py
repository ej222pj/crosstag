from flask.ext.wtf import Form
from wtforms import TextField, RadioField, PasswordField, validators

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
    username = TextField('username', [validators.Length(max=80, message='Username is to long, 80 characters is maximum')
                                    , validators.DataRequired(message='Username is required')])
    password = PasswordField('password', [validators.Length(max=80),
                                          validators.DataRequired(),
                                          validators.EqualTo('repeat_password', message='Passwords must match')])
    repeat_password = PasswordField('repeat_password', [validators.Length(max=80), validators.DataRequired()])
    active_fortnox = RadioField('active_fortnox', [validators.DataRequired()], choices=[('true', 'Yes'), ('false', 'No')])
    gym_name = TextField('gym_name', [validators.Length(max=50), validators.DataRequired()])
    address = TextField('address', [validators.Length(max=50), validators.DataRequired()])
    phone = TextField('phone', [validators.Length(max=20), validators.DataRequired()])
    zip_code = TextField('zip_code', [validators.Length(max=20), validators.DataRequired()])
    city = TextField('city', [validators.Length(max=50), validators.DataRequired()])
    email = TextField('email', [validators.Length(max=50), validators.Email()])