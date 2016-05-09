import pypyodbc
from db_service import sql_client_cfg as cfg
from db_models import sql_tenant as tenant
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

    def get_tenants(self, username=''):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetMembers('" + username + "')}")
            values = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return_array = []
            for tenants in values:
                return_array.append(tenant.SQLTenant(tenants[0], tenants[1], tenants[2], tenants[3], tenants[4],
                                                     tenants[5], tenants[6], tenants[7], tenants[8], tenants[9],
                                                     tenants[10]))
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def update_tenant_information(self, tenant):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

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
