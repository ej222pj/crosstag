from flask.ext.wtf import Form
from wtforms import TextField, RadioField, DateField, validators, PasswordField
from wtforms.validators import Required


class EditGeneralInformation(Form):
    """
    A representation of the form for updating a tenants info.

    :param password: Tenants password for confirmation
    :param gym_name: Tenants Gym name
    :param address: Tenants Address
    :param phone: Tenants Phone
    :param zip_code: Tenants Zip
    :param city: Tenants City
    :param Email: Tenants Email
    """
    password = PasswordField('password', [validators.Length(max=80), validators.DataRequired()])
    gym_name = TextField('gym_name', [validators.Length(max=50), validators.DataRequired()])
    address = TextField('address', [validators.Length(max=50), validators.DataRequired()])
    phone = TextField('phone', [validators.Length(max=20), validators.DataRequired()])
    zip_code = TextField('zip_code', [validators.Length(max=20), validators.DataRequired()])
    city = TextField('city', [validators.Length(max=50), validators.DataRequired()])
    email = TextField('email', [validators.Length(max=50), validators.Email()])