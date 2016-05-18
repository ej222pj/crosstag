class SQLTenant:
    """
        Tenant - This class is the representation of the database model Tenant.
    """
    def __init__(self, id=0, username='', active_fortnox='false', image='', background_color='', api_key='',
                 general_info_id='', gym_name='', address='', phone='', zip_code='', city='', email=''):
        """
        Called when creating a new Tenant class.

        :param id: Id of the Tenant
        :param username: Tenants username
        :param active_fortnox: If tenant got fortnox of not
        :param image: Image url
        :param background_color: Design choice for the Tenant
        :param api_key: Tenants api key to the Rest Api
        :param general_info_id: Id to the tenants information
        :param gym_name: Tenants gym name
        :param address: Address to the gym
        :param phone: Phone to the gym or the owner
        :param zip_code: Zip Code to the gym
        :param city: City the gym is located in
        :param email: Email to the gym
        :type id: integer
        :type username: string
        :type active_fortnox: string
        :type image: string
        :type background_color: string
        :type api_key: string
        :type general_info_id: integer
        :type gym_name: string
        :type address: string
        :type phone: string
        :type zip_code: string
        :type city: string
        :type email: string
        """
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
