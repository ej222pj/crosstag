import pypyodbc
from db_service import sql_client_cfg as cfg
from db_models import sql_user as user
from flask import session
from datetime import datetime, timedelta


class UsersSqlClient:
    """
    Class to Connect to the DB and CRUD user and Search User.

    __init__ - Creates connection string variables
    get_connection_string - Creates connection string from the variables
    get_users - Get all or 1 user
    get_inactive_users - Get all active members that have not tagged for 2 weeks
    does_user_exist - Check if user exists when trying to add from Fortnox
    search_user_on_tag - Search for a user on the tag id
    add_user - Add new user
    update_user - Update user
    remove_user - Remove user
    search_user - Search for Users
    """
    def __init__(self, username=''):
        """
        Takes param username.
        Init function that creates the variables for the connection string.
        If session exists, set username to the session variable Username.

        :param username: The Tenants Username.
        :type username: string
        """
        if session.get('username') is not None:
            username = session['username']
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + username + ';'
        self.dbPassword = 'pwd=' + cfg.TENANT_PASSWORD + username

    def get_connection_string(self):
        """
        Creates a connection string for the DB from the variables created in init.

        :return: Connection String
        """
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def get_users(self, user_id=0):
        """
        Takes user_id as parameter
        Get all or specific user

        :param user_id: User id
        :type user_id: integer
        :return: Array of Users
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetUser('" + str(user_id) + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return_array = []
            # [:-12]/[:-12]/[:-6] Removes unnecessary decimals
            for users in value:
                return_array.append(user.SQLUser(users[0], users[1], users[2], users[3], users[4], users[5], users[6],
                                                 users[7], users[8], users[9], users[10], users[11], users[12],
                                                 users[13][:-12], users[14][:-12], users[15], users[16],
                                                 users[17][:-6]))
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def get_inactive_users(self):
        """
        Get all active members that have not tagged for 2 weeks

        :return: Array of Inactive Users
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetInactiveUsers()}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return_array = []
            # [:-12]/[:-12]/[:-6] Removes unnecessary decimals
            for users in value:
                return_array.append(user.SQLUser(users[0], users[1], users[2], users[3], users[4], users[5], users[6],
                                                 users[7], users[8], users[9], users[10], users[11], users[12],
                                                 users[13][:-12], users[14][:-12], users[15], users[16],
                                                 users[17][:-6]))
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def does_user_exist(self, fortnox_id):
        """
        Takes fortnox_id as parameter
        Checks if Users all ready exists when adding from Fortnox.

        :param fortnox_id: Fortnox id
        :type fortnox_id: integer
        :return: True or False
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call DoesUserExists('" + fortnox_id + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            # Return True if the User all ready exists in the database
            if value[0][0] is None:
                return True
            else:
                return False

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def search_user_on_tag(self, tag_id):
        """
        Takes tag_id as parameter
        Checks if the Tag Id is connected to a user when adding a new Tagevent

        :param tag_id: Tag Id
        :type tag_id: string
        :return: User Object
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()
            cursor.execute("{call SearchUserOnTag('" + tag_id + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return value

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def add_user(self, user):
        """
        Takes a representation of User class as parameter
        Adds a new User in the DB

        :param user: Representation of User class
        :type user: User class
        :return: Primary Key (id) of the new User
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()
            user['create_date'] = str(datetime.now())
            cursor.execute("{call AddUser('" + user['fortnox_id'] + "','" + user['firstname'] + "','" +
                           user['lastname'] + "','" + user['email'] + "','" +
                           user['phone'] + "','" + user['address'] + "','" +
                           user['address2'] + "','" + user['city'] + "','" +
                           user['zip_code'] + "','" + user['tag_id'] + "','" +
                           user['gender'] + "','" + user['ssn'] + "','" +
                           user['expiry_date'] + ' 00:00:00.0000000' + "','" +
                           user['create_date'] + "','" + user['status'] + "','" +
                           user['tagcounter'] + "','" + user['last_tag_timestamp'] + '0' + "')}")
            value = cursor.fetchall()[0]

            cursor.commit()
            cursor.close()
            my_connection.close()
            return int(value[0])

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def update_user(self, user):
        """
        Takes a representation of User class as parameter
        Updates a User in the DB

        :param user: Representation of User class
        :type user: User class
        :return: True
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            if user['id'] is 0:
                cursor.execute("{call GetUserId('" + user['fortnox_id'] + "')}")
                value = cursor.fetchall()[0][0]
                if value is not None:
                    user['id'] = value

            cursor.execute("{call UpdateUser('" + str(user['id']) + "','" +
                           user['firstname'] + "','" + user['lastname'] + "','" +
                           user['email'] + "','" + user['phone'] + "','" +
                           user['address'] + "','" + user['address2'] + "','" +
                           user['city'] + "','" + user['zip_code'] + "','" +
                           user['tag_id'] + "','" + user['gender'] + "','" +
                           user['ssn'] + "','" + user['expiry_date'] + ' 00:00:00.0000000' "','" +
                           user['status'] + "')}")

            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def remove_user(self, user_id):
        """
        Takes User Id as parameter
        Removes a User from the DB

        :param user_id: Id of the User to remove
        :type user_id:integer
        :return: True
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call DeleteUser('" + str(user_id) + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def search_user(self, search_user_object):
        """
        Takes a representation of User class as parameter
        Search for all Users in the DB that matches the object

        :param search_user_object: Representation of User class
        :type search_user_object: User class
        :return: Array with users
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call SearchUsers('" + search_user_object['firstname'] + "','" +
                           search_user_object['lastname'] + "','" + search_user_object['email'] + "','" +
                           search_user_object['city'] + "')}")

            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return_array = []
            for users in value:
                return_array.append(user.SQLUser(users[0], users[1], users[2],users[3], users[4], users[5], users[6],
                                                 users[7], users[8], users[9], users[10], users[11], users[12],
                                                 users[13][:-12], users[14][:-12], users[15], users[16],
                                                 users[17][:-6]))
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)