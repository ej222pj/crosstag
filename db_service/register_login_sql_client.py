import pypyodbc
from db_service import sql_client_cfg as cfg
from datetime import datetime, timedelta


class RegisterLoginSqlClient:
    """
    Class to Connect to the DB an /Create/Read/Delete a Debt

    __init__ - Creates connection string variables
    do_registration - Creates a new Tenant in the DB when a Tenant tries to register
    do_login - Tries to login the Tenant
    get_tenant_with_api_key - Checks if a Tenant exists when using the rest API
    """
    def __init__(self, username=cfg.USERNAME, password=cfg.PASSWORD):
        """
        Init function that creates the variables for the connection string
        """
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + username + ';'
        self.dbPassword = 'pwd=' + password

    def get_connection_string(self):
        """
        Creates a connection string for the DB from the variables created in init.

        :return: Connection String
        """
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def do_registration(self, tenant):
        """
        Takes a Tenant as argument and register it.

        :param tenant: A Tenant representation
        :type tenant: tenant class
        :return: True
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call CreateTenantLogin('" + tenant['username'] + "','" + tenant['password'] + "','" +
                           tenant['active_fortnox'] + "','" + tenant['gym_name'] + "','" + tenant['address'] + "','" +
                           tenant['phone'] + "','" + tenant['zip_code'] + "','" + tenant['city'] + "','" +
                           tenant['email'] + "','" + tenant['pass'] + "' )}")
            value = cursor.fetchall()[0]

            cursor.commit()
            cursor.close()
            my_connection.close()
            
            if value[0] is None:
                return False
            else:
                return True

        except pypyodbc.DatabaseError as error:
            print(error.value)
            print('FATALITY')

    def do_login(self, username):
        """
        Takes a username and checks if it exists in the DB.
        Gives back the Tenants password to check if it matches input password.

        :param username: A Tenant representation
        :type username: tenant class
        :return: Tenant password
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call LoginTenant('" + username + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return value[0][0]

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def get_tenant_with_api_key(self, api_key):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetTenantWithApiKey('" + api_key + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()

            return_array = []
            for username in value:
                return_array.append({'username': username[0]})


            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)
