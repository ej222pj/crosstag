import pypyodbc
from db_service import sql_client_cfg as cfg
from flask import session
from datetime import datetime, timedelta


class MembersSqlClient():
    def __init__(self):
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + session['username'] + ';'
        self.dbPassword = 'pwd=' + cfg.TENANT_PASSWORD + session['username']

    def get_connection_string(self):
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def get_member(self, id=0):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetUser('" + str(id) + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return value

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def does_member_exist(self, fortnox_id):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call DoesMemberExists('" + fortnox_id + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            if value[0][0] is None:
                return True
            else:
                return False

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def add_member(self, member):
        connection_string = self.get_connection_string()
        try:
            print('Add med function')
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()
            member['create_date'] = str(datetime.now())
            cursor.execute("{call AddUser('" + member['fortnox_id'] + "','" + member['firstname'] + "','" +
                           member['lastname'] + "','" + member['email'] + "','" + member['phone'] + "','" +
                           member['address'] + "','" + member['address2'] + "','" + member['city'] + "','" +
                           member['zip_code'] + "','" + member['tag_id'] + "','" + member['gender'] + "','" +
                           member['ssn'] + "','" + member['expiry_date'] + ' 00:00:00.0000000' + "','" +
                           member['create_date'] + "','" + member['status'] + "','" + member['tagcounter'] + "','" +
                           member['last_tag_timestamp'] + '0' + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def update_member(self, member):

        connection_string = self.get_connection_string()
        try:
            print('update function')
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            if member['id'] is 0:
                cursor.execute("{call GetUserId('" + member['fortnox_id'] + "')}")
                value = cursor.fetchall()[0][0]
                if value is not None:
                    member['id'] = value

            cursor.execute("{call UpdateUser('" + str(member['id']) + "','" +
                           member['firstname'] + "','" + member['lastname'] + "','" + member['email'] + "','" +
                           member['phone'] + "','" + member['address'] + "','" + member['address2'] + "','" +
                           member['city'] + "','" + member['zip_code'] + "','" + member['tag_id'] + "','" +
                           member['gender'] + "','" + member['ssn'] + "','" +
                           member['expiry_date'] + ' 00:00:00.0000000' "','" + member['status'] + "')}")

            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def remove_member(self, id):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call DeleteUser('" + id + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)