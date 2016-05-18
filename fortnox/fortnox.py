import http.client
import json
import requests
import fortnox_cfg as cfg


class Fortnox:
    """
    Class to Get/Insert/Uptade from and to Fortnox.
    It can be used to Remove, but we don't need remove in this case.
    This class will help with the "CRUD" functionality that fortnox API is offering us.

    get_all_customers - Get customers function to get all customers.
    get_customer_by_id - Get customer function to get a customer based on id.
    insert_customer_by_id - Creates a new customer on fortnox.
    update_customer - Updates a customer on fortnox.
    """
    def get_all_customers(self):
        """
        Creates a connection to the fortnox API and grabs all customers.

        :return: JSON object of an array with all customers.
        """
        try:
            page = 1
            customer_array = []
            # Can only get 1 page at the time.
            while True:
                r = requests.get(
                    url='https://api.fortnox.se/3/customers/?page='+str(page),
                    headers=cfg.fortnox
                )
                print('Response status: {status_code}'.format(status_code=r.status_code))
                content = json.loads(r.text)
                customer_array.append(content["Customers"])
                page += 1

                if content["MetaInformation"]["@TotalPages"] == content["MetaInformation"]["@CurrentPage"]:
                    break

            return customer_array
        except http.client.HTTPException:
            # Exception
            print('Exception during request')

    def get_customer_by_id(self, id):
        """
        Takes an id as argument and then creates a connection to the fortnox API and gets 1 customer.

        :param id: Id of an user from fortnox.
        :type id: integer
        :return: JSON object of the user
        """
        connection = http.client.HTTPSConnection('api.fortnox.se')
        connection.request('GET', '/3/customers/'+id+'/', None, cfg.fortnox)
        try:
            response = connection.getresponse()
            content = response.read()

            return content
        except http.client.HTTPException:
            # Exception
            print('Exception during request')

    def insert_customer(self, user):
        """
        Takes a user as argument and then creates a connection to the fortnox API to create a customer.

        :param user: An user representation
        :type user: User class
        """
        try:
            r = requests.post(
                url='https://api.fortnox.se/3/customers',
                headers=cfg.fortnox,
                data=json.dumps({
                    "Customer": {
                        "Name": user.name,
                        "Email": user.email,
                        "Address1": user.address,
                        "Address2": user.address2,
                        "City": user.city,
                        "ZipCode": user.zip_code
                    }
                })
            )
        except http.client.HTTPException as e:
            print('Exception during POST-request')

    def update_customer(self, user):
        """
        Takes an user as an argument and then creates a connection to the fortnox API to update a customer.

        :param user: An user representation
        :type user: User class
        """
        try:
            r = requests.put(
                url='https://api.fortnox.se/3/customers/'+str(user.fortnox_id)+'/',
                headers=cfg.fortnox,
                data=json.dumps({
                    "Customer": {
                        "Email": user.email,
                        "Address1": user.address,
                        "Address2": user.address2,
                        "City": user.city,
                        "ZipCode": user.zip_code
                    }
                })
            )
        except http.client.HTTPException as e:
            print('Exception during POST-request')
