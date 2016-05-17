import pypyodbc
from db_service import sql_client_cfg as cfg
from db_models import sql_user as user
from flask import session
from datetime import datetime, timedelta


class UsersSqlClient:
    def __init__(self, username=''):
        if session.get('username') is not None:
            username = session['username']
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + username + ';'
        self.dbPassword = 'pwd=' + cfg.TENANT_PASSWORD + username

    def get_connection_string(self):
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def get_users(self, id=0):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetUser('" + str(id) + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return_array = []
            for users in value:
                return_array.append(user.SQLUser(users[0], users[1], users[2], users[3], users[4], users[5], users[6],
                                                 users[7], users[8], users[9], users[10], users[11], users[12],
                                                 users[13][:-12], users[14][:-12], users[15], users[16],
                                                 users[17][:-6]))
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def get_inactive_users(self):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetInactiveUsers()}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return_array = []
            for users in value:
                return_array.append(user.SQLUser(users[0], users[1], users[2], users[3], users[4], users[5], users[6],
                                                 users[7], users[8], users[9], users[10], users[11], users[12],
                                                 users[13][:-12], users[14][:-12], users[15], users[16],
                                                 users[17][:-6]))
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def does_user_exist(self, fortnox_id):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call DoesUserExists('" + fortnox_id + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            if value[0][0] is None:
                return True
            else:
                return False

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def search_user_on_tag(self, tag_id):
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

    def add_user(self, user_to_add):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()
            user_to_add['create_date'] = str(datetime.now())
            cursor.execute("{call AddUser('" + user_to_add['fortnox_id'] + "','" + user_to_add['firstname'] + "','" +
                           user_to_add['lastname'] + "','" + user_to_add['email'] + "','" +
                           user_to_add['phone'] + "','" + user_to_add['address'] + "','" +
                           user_to_add['address2'] + "','" + user_to_add['city'] + "','" +
                           user_to_add['zip_code'] + "','" + user_to_add['tag_id'] + "','" +
                           user_to_add['gender'] + "','" + user_to_add['ssn'] + "','" +
                           user_to_add['expiry_date'] + ' 00:00:00.0000000' + "','" +
                           user_to_add['create_date'] + "','" + user_to_add['status'] + "','" +
                           user_to_add['tagcounter'] + "','" + user_to_add['last_tag_timestamp'] + '0' + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def update_user(self, user_to_update):

        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            if user_to_update['id'] is 0:
                cursor.execute("{call GetUserId('" + user_to_update['fortnox_id'] + "')}")
                value = cursor.fetchall()[0][0]
                if value is not None:
                    user_to_update['id'] = value

            cursor.execute("{call UpdateUser('" + str(user_to_update['id']) + "','" +
                           user_to_update['firstname'] + "','" + user_to_update['lastname'] + "','" +
                           user_to_update['email'] + "','" + user_to_update['phone'] + "','" +
                           user_to_update['address'] + "','" + user_to_update['address2'] + "','" +
                           user_to_update['city'] + "','" + user_to_update['zip_code'] + "','" +
                           user_to_update['tag_id'] + "','" + user_to_update['gender'] + "','" +
                           user_to_update['ssn'] + "','" + user_to_update['expiry_date'] + ' 00:00:00.0000000' "','" +
                           user_to_update['status'] + "')}")

            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def remove_user(self, user_id):
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