from flask.ext.wtf import Form
from wtforms import TextField, RadioField
from wtforms.validators import Required


class SearchUser(Form):
    index = TextField('name', validators=[])
    name = TextField('name', validators=[])
    email = TextField('email', validators=[])
    phone = TextField('phone', validators=[])
    fortnox_id = TextField('fortnox_id', validators=[])
    tag = TextField('tag', validators=[])
    gender = RadioField(
        'gender',
        [Required()],
        choices=[('male', 'male'), ('female', 'female'),
                 ('unknown', 'unknown')], default='unknown'
    )