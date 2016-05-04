from flask.ext.wtf import Form
from wtforms import TextField, RadioField, DateField, validators
from wtforms.validators import Required


class NewUser(Form):
    """
    A representation of the form for adding a user.

    :param firstname: Firstname of the user.
    :param lastname: Lastname of the user.
    :param email: Emailaddress of the user.
    :param phone: Phonenumber of the user.
    :param address: Address 1 of the user.
    :param address2: Address 2 of the user.
    :param city: City of the user.
    :param zip_code: Zip code of the city.
    :param tag_id: Tag id of the user.
    :param expiry_date: Expire date of the users membership.
    :param gender: Gender of the user.
    :param status: Status of the users membership.

    """
    firstname = TextField('firstname', [validators.Length(max=25), validators.DataRequired()])
    lastname = TextField('lastname', [validators.Length(max=30), validators.DataRequired()])
    email = TextField('email', [validators.Length(max=120), validators.Email()])
    phone = TextField('phone', [validators.Length(max=20), validators.DataRequired()])
    address = TextField('address', [validators.Length(max=50), validators.DataRequired()])
    address2 = TextField('address2', [validators.Length(max=50)])
    city = TextField('city', [validators.Length(max=120), validators.DataRequired()])
    zip_code = TextField('zip_code', validators=[])
    tag_id = TextField('tag_id', validators=[])
    expiry_date = DateField('expiry_date', [validators.Optional()], format='%Y-%m-%d', description="DESC1")
    gender = RadioField('gender', [validators.DataRequired()], choices=[('male', 'male'), ('female', 'female'),
                                                                      ('unknown', 'unknown')])
    status = RadioField('status', [Required()],
                        choices=[('Active', 'active'), ('Inactive', 'inactive'), ('Frozen', 'frozen'), ('Free', 'free'),
                                 ('Special', 'special')])