from datetime import datetime


class SQLUser:
    def __init__(self, id=0, fortnox_id=None, firstname='', lastname='', email='', phone='', address='',
                 address2='', city='', zip_code='', tag_id=None, gender='', ssn='', expiry_date=None,
                 create_date=None, status='', tagcounter=None, last_tag_timestamp=None):

        self.id = id
        self.fortnox_id = fortnox_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.address = address
        self.address2 = address2
        self.city = city
        self.zip_code = zip_code
        self.tag_id = tag_id
        self.ssn = ssn
        self.gender = gender
        self.create_date = create_date
        self.status = status
        self.tagcounter = tagcounter
        self.expiry_date = expiry_date

        if self.id is None:
            self.id = 0
        if self.status is None:
            self.status = 'Inactive'
        if self.fortnox_id is None:
            self.fortnox_id = ''
        if self.tag_id is None:
            self.tag_id = ''
        if self.expiry_date is None:
            self.expiry_date = ''
        if self.tagcounter is None:
            self.tagcounter = ''
        self.last_tag_timestamp = last_tag_timestamp
        if self.last_tag_timestamp is None:
            self.last_tag_timestamp = datetime.now()

    def dict(self):
        """

        :return: Dictionary representation of the user class.
        :rtype: Dictionary
        """
        return {'id': self.id, 'firstname': self.firstname,
                'lastname': self.lastname, 'email': self.email,
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
                'last_tag_timestamp': str(self.last_tag_timestamp)
                }
