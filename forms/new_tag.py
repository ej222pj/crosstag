from flask.ext.wtf import Form
from wtforms import TextField


class NewTag(Form):
    """
    A representation of the form for creating a new tag.

    :param tag_id: The number of the specific tag
    :type tag_id: String (20)
    """
    tag_id = TextField('tag_id', validators=[])