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
    password = PasswordField('password', [validators.Length(max=80, message='Password is to long, 80 characters is maximum'),
                                          validators.DataRequired(message='Password is required'),
                                          validators.EqualTo('repeat_password', message='Passwords must match')])
    repeat_password = PasswordField('repeat_password', [validators.Length(max=80, message='Repeated password is to long, '
                                                                                          '80 characters is maximum'),
                                                        validators.DataRequired(message='Repeated password is required')])
    active_fortnox = RadioField('active_fortnox', [validators.DataRequired(message='You must choose Yes/No for active fortnox')],
                                                    choices=[('true', 'Yes'), ('false', 'No')])
    gym_name = TextField('gym_name', [validators.Length(max=50, message='Gym name is to long, 50 characters is maximum'),
                                      validators.DataRequired(message='Gym name is required')])
    address = TextField('address', [validators.Length(max=50, message='Address is to long, 50 characters is maximum'),
                                    validators.DataRequired(message='Address is required')])
    phone = TextField('phone', [validators.Length(max=20, message='Phone number is to long, 20 characters is maxium'),
                                validators.DataRequired(message='Phone number is required')])
    zip_code = TextField('zip_code', [validators.Length(max=20, message='Zip code is to long, 20 characters is maximum'),
                                      validators.DataRequired(message='Zip code is required')])
    city = TextField('city', [validators.Length(max=50, message='City is to long, 50 characters is maximum'),
                              validators.DataRequired(message='City is required')])
    email = TextField('email', [validators.Length(max=50, message='Email is to long, 50 characters is maximum'),
                                validators.Email(message='Email not in valid format'),
                                validators.DataRequired(message='Email is required')])