class SQLTenant:
    def __init__(self, id=0, username='', active_fortnox='false', image='', background_color='', api_key='',
                 general_info_id='', gym_name='', address='', phone='', zip_code='', city='', email=''):

        self.id = id
        self.username = username
        self.active_fortnox = active_fortnox
        self.image = image
        self.background_color = background_color
        self.api_key = api_key
        self.general_info_id = general_info_id
        self.gym_name = gym_name
        self.address = address
        self.phone = phone
        self.zip_code = zip_code
        self.city = city
        self.email = email

        if self.id is None:
            self.id = 0

    def dict(self):
        """

        :return: Dictionary representation of the user class.
        :rtype: Dictionary
        """
        return {'id': self.id,
                'username': self.username,
                'active_fortnox': self.active_fortnox,
                'image': self.image,
                'background_color': self.background_color,
                'api_key': self.api_key,
                'general_info_id': self.general_info_id,
                'gym_name': self.gym_name,
                'address': self.address,
                'phone': self.phone,
                'zip_code': self.zip_code,
                'city': self.city,
                'email': self.email
                }
