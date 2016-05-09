from flask.ext.wtf import Form
from wtforms import TextField, RadioField, DateField, validators, PasswordField
from wtforms.validators import Required


class EditTenant(Form):
    """
    A representation of the form for updating a tenants info.

    :param password: tenants old pass
    :param new_password: tenants new pass
    :param repeat_new_password: tenants new pass again
    :param active_fortnox: If the tenant got fortnox
    :param image: Gym image
    :param background_color: Background color
    """
    password = PasswordField('password', [validators.Length(max=80), validators.DataRequired()])
    new_password = PasswordField('new_password', [validators.Length(max=80), validators.DataRequired()])
    repeat_new_password = PasswordField('repeat_new_password', [validators.Length(max=80), validators.DataRequired()])
    active_fortnox = RadioField('active_fortnox', [validators.DataRequired()],
                                choices=[('true', 'Yes'), ('false', 'No')])
    image = TextField('image', [validators.Length(max=80), validators.DataRequired()])
    background_color = TextField('background_color', [validators.Length(max=80), validators.DataRequired()])