from flask.ext.wtf import Form
from wtforms import TextField, RadioField, DateField, validators, PasswordField
from wtforms.validators import Required


class EditGeneralInformation(Form):
    """
    A representation of the form for updating a Tenants general info.

    :param password: Tenants password for confirmation
    :param gym_name: Tenants Gym name
    :param address: Tenants Address
    :param phone: Tenants Phone
    :param zip_code: Tenants Zip
    :param city: Tenants City
    :param Email: Tenants Email
    :type password: string (80)
    :type gym_name: string (50)
    :type address: string (50)
    :type phone: string (20)
    :type zip_code: string (20)
    :type city: string (50)
    :type Email: string (50)
    """
    password = PasswordField('password', [validators.Length(max=80, message='Password is to long, 80 characters is maximum'),
                                          validators.DataRequired(message='Password is required to save changes')])
    gym_name = TextField('gym_name', [validators.Length(max=50, message='Gym name is to long, 50 characters is maximum'),
                                      validators.DataRequired(message='Gym name is required')])
    address = TextField('address', [validators.Length(max=50, message='Address is to long, 50 characters is maximum'),
                                    validators.DataRequired(message='Address is required')])
    phone = TextField('phone', [validators.Length(max=20, message='Phone number is to long, 20 characters is maximum'),
                                validators.DataRequired(message='Phone number is required')])
    zip_code = TextField('zip_code', [validators.Length(max=20, message='Zip code is to long, 20 characters is maximum'),
                                      validators.DataRequired(message='Zip code is required')])
    city = TextField('city', [validators.Length(max=50, message='City is to long, 50 characters is maximum'),
                              validators.DataRequired(message='City is required')])
    email = TextField('email', [validators.Length(max=50, message='Email is to long, 50 characters is maximum'),
                                validators.Email(message='Email is not in valid format'),
                                validators.DataRequired(message='Email is required')])