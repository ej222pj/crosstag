from flask import jsonify
from datetime import datetime
from crosstag_init import db


class User(db.Model):
    """
    User - A representation of the database model
    """
    index = db.Column(db.Integer, primary_key=True)
    fortnox_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(50))
    address2 = db.Column(db.String(50))
    city = db.Column(db.String(120))
    zip_code = db.Column(db.Integer)
    tag_id = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    ssn = db.Column(db.String(13))
    expiry_date = db.Column(db.Date)
    create_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    tagcounter = db.Column(db.Integer)
    last_tag_timestamp = db.Column(db.DateTime)

    def __init__(self, name, email, phone=None, address=None, address2=None, city=None, zip_code=None, tag_id=None, fortnox_id=None,
                 expiry_date=None, ssn=None, gender=None, status=None, last_tag_timestamp=None):
        """

        Called when creating a new user.

        :param name: Name of the user, Firstname & Lastname.
        :param email: Emailaddress of the user.
        :param phone: Phonenumber of the user.
        :param address: Address 1 of the user.
        :param address2: Address 2 of the user.
        :param city: City of the user.
        :param zip_code: Zip code of the city.
        :param tag_id: Tag id of the user.
        :param fortnox_id: Fortnox id of the user.
        :param expiry_date: Expire date of the users membership.
        :param ssn: Social security number of the user.
        :param gender: Gender of the user.
        :param status: Status of the users membership.
        :param last_tag_timestamp: Timestamp of the last tag in from the user.

        :type name: String (80)
        :type email: String (120)
        :type phone: String (20)
        :type address: String (50)
        :type address2: String (50)
        :type city: String (120)
        :type zip_code: Integer
        :type tag_id: String (20)
        :type fortnox_id: Integer
        :type expiry_date: Date
        :type ssn: String (13)
        :type gender: String (10)
        :type status: String (50)
        :type last_tag_timestamp: DateTime

        """
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.address2 = address2
        self.city = city
        self.zip_code = zip_code
        self.tag_id = tag_id
        self.fortnox_id = fortnox_id
        self.expiry_date = expiry_date
        self.ssn = ssn
        self.gender = gender
        self.create_date = datetime.now()
        self.status = status
        if(self.tagcounter is None):
            self.tagcounter = 0

    def dict(self):
        """

        :return: Dictionary representation of the user class.
        :rtype: Dictionary
        """
        return {'index': self.index, 'name': self.name,
                'email': self.email, 'tag_id': self.tag_id,
                'phone': self.phone, 'address': self.address,
                'address2': self.address2, 'city': self.city,
                'zip_code': self.zip_code,
                'tag_id': self.tag_id,
                'fortnox_id': self.fortnox_id,
                'expiry_date': str(self.expiry_date),
                'create_date': str(self.create_date),
                'ssn': self.ssn,
                'gender': self.gender,
                'status': self.status,
                'tagcounter': self.tagcounter,
                'last_tag_timestamp': self.last_tag_timestamp
                }

    def json(self):
        """

        :return: Json object of the dictionary representation
        :rtype: JSON
        """
        return jsonify(self.dict())
