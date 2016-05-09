import pypyodbc
from db_service import sql_client_cfg as cfg
from datetime import datetime, timedelta


class UpdateTenantInformationSqlClient():
    def __init__(self):
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + cfg.USERNAME + ';'
        self.dbPassword = 'pwd=' + cfg.PASSWORD

    def get_connection_string(self):
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def get_tenants(self):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetMembers('" + session['username'] + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return_array = []
            #for users in value:
             #   return_array.append(user.SQLUser(users[0], users[1], users[2],
             #                                    users[3], users[4], users[5],
              #                                   users[6], users[7], users[8],
               #                                  users[9], users[10], users[11],
                #                                 users[12], users[13], users[14],
                 #                                users[15], users[16], users[17]))
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def update_tenant_information(self, tenant):
        connection_string = self.get_connection_string()
        try:
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

    def do_login(self, username):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call LoginUser('" + username + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return value[0][0]

        except pypyodbc.DatabaseError as error:
            print(error.value)
