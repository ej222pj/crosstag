from datetime import datetime

class SQLUser:
    """
        User - This class is the representation of the database model User.
    """
    def __init__(self, id=0, fortnox_id=None, firstname='', lastname='', email='', phone='', address='',
                 address2='', city='', zip_code='', tag_id=None, gender='', ssn='', expiry_date=None,
                 create_date=None, status='', tagcounter=None, last_tag_timestamp=None):
        """
        Called when creating a new User class.

        :param id: Id of the User
        :param fortnox_id: Users fortnox ID
        :param firstname: Users firstname
        :param lastname: Users lastname
        :param email: Email to the User
        :param phone: Users phonenumber
        :param address: Address to the user
        :param address2: Second Address to the user
        :param city: City of the user
        :param zip_code: Zip Code to the User
        :param tag_id: Users tag id
        :param gender: Users gender
        :param ssn: Users SSN
        :param expiry_date: Expire date of the users membership
        :param create_date: Create date of the user
        :param status: Users gym status
        :param tagcounter: How many times the user have tagged this month
        :param last_tag_timestamp: When the last tagin occurred
        :type id: integer
        :type fortnox_id: string
        :type firstname: string
        :type lastname: string
        :type email: string
        :type phone: string
        :type address: string
        :type address2: string
        :type city: string
        :type zip_code: string
        :type tag_id: string
        :type gender: string
        :type ssn: string
        :type expiry_date: string
        :type create_date: string
        :type status: string
        :type tagcounter: integer
        :type last_tag_timestamp: datetime
        """
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
        return {'id': self.id,
                'firstname': self.firstname,
                'lastname': self.lastname,
                'email': self.email,
                'phone': self.phone,
                'address': self.address,
                'address2': self.address2,
                'city': self.city,
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
