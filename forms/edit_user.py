from flask.ext.wtf import Form
from wtforms import TextField, RadioField, DateField, validators
from wtforms.validators import Required


class EditUser(Form):
    """
    A representation of the form for editing a user.

    :param firstname: Firstname of the user.
    :param lastname: Lastname of the user.
    :param email: Emailaddress of the user.
    :param phone: Phonenumber of the user.
    :param address: Address 1 of the user.
    :param address2: Address 2 of the user.
    :param city: City of the user.
    :param zip_code: Zip code of the city.
    :param tag_id: Tag id of the user.
    :param gender: Gender of the user.
    :param expiry_date: Expire date of the users membership.
    :param status: Status of the users membership.
    :type firstname: string (25)
    :type lastname: string (30)
    :type email: string (120)
    :type phone: string (20)
    :type address: string (50)
    :type address2: string (50)
    :type city: string (120)
    :type zip_code: string (20)
    :type tag_id: string (20)
    :type gender: string (10)
    :type expiry_date: datetime
    :type status: string (10)

    """
    firstname = TextField('firstname', [validators.Length(max=25, message='Firstname to long, 25 characters is maximum'),
                                        validators.DataRequired(message='Firstname is required')])
    lastname = TextField('lastname', [validators.Length(max=30, message='Lastname to long, 30 characters is maximum'),
                                      validators.DataRequired(message='Lastname is required')])
    email = TextField('email', [validators.Length(max=120, message='Email to long, 120 characters is maximum'),
                                validators.Email(message='Email is not in valid format')])
    phone = TextField('phone', [validators.Length(max=20, message='Phone number to long, 20 characters is maximum'),
                                validators.DataRequired(message='Phone number is required')])
    address = TextField('address', [validators.Length(max=50, message='Address to long, 50 characters is maximum'),
                                    validators.DataRequired(message='Address is required')])
    address2 = TextField('address2', [validators.Length(max=50, message='Second address to long, 50 characters is maximum')])
    city = TextField('city', [validators.Length(max=120, message='City to long, 120 characters is maximum'),
                              validators.DataRequired(message='City is required')])
    zip_code = TextField('zip_code', [validators.Length(max=20, message='Zip code is to long, 20 characters is maximum'),
                                      validators.DataRequired(message='Zip code is required')])
    tag_id = TextField('tag_id', [validators.Length(max=20, message='Tag id to long, 20 characters is maximum')])
    gender = RadioField('gender', [validators.DataRequired(message='Gender is required')],
                        choices=[('male', 'male'), ('female', 'female'),
                                 ('unknown', 'unknown')])


    expiry_date = DateField('expiry_date', [validators.Optional()], format='%Y-%m-%d', description="DESC1")
    status = RadioField('status', [validators.DataRequired(message='Status is required')],
                    choices=[('Active', 'active'), ('Inactive', 'inactive'), ('Frozen', 'frozen'), ('Free', 'free'),
                             ('Special', 'special')])