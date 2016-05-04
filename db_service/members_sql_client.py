import pypyodbc
from db_service import sql_client_cfg as cfg
from datetime import datetime, timedelta


class MembersSqlClient():
    def __init__(self, username, password):
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + username + ';'
        self.dbPassword = 'pwd=' + password

    def get_connection_string(self):
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def get_member(self, id=0):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetUser('" + id + "')}")
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
            return value[0][0]

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def add_member(self, fortnox_id=0, firstname='', lastname='', email='', phone='', address='', address2='',
                    city='', zip_code=0, tag_id='', gender='', ssn='', expiry_date='2000-01-01 00:00:00.000000',
                    create_date=datetime.now(), status='', tagcounter=0, last_tag_timestamp='2000-01-01 00:00:00.000000'
                    ):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call AddUser('" + fortnox_id + "','" +  firstname + "','" +  lastname + "','" +
                           email + "','" +  phone + "','" +  address+ "','" + address2 + "','" + city + "','" +
                           zip_code + "','" +  tag_id + "','" +  gender + "','" +  ssn + "','" +  expiry_date + "','" +
                           create_date + "','" +  status + "','" +  tagcounter + "','" +  last_tag_timestamp + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def update_member(self, firstname, lastname, email, phone, address, address2, city, zip_code, tag_id, gender,
                       ssn, expiry_date, status, id=None, fortnox_id=None):

        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            if id is None:
                cursor.execute("{call UpdateFortnoxUser('" + fortnox_id + "','" + firstname + "','" + lastname + "','" +
                               email + "','" + phone + "','" + address + "','" + address2 + "','" + city + "','" +
                               zip_code + "','" + tag_id + "','" + gender + "','" + ssn + "','" + expiry_date + "','" +
                               status + "')}")
            else:
                cursor.execute("{call UpdateUser('" + id + "','" + firstname + "','" + lastname + "','" +
                               email + "','" + phone + "','" + address + "','" + address2 + "','" + city + "','" +
                               zip_code + "','" + tag_id + "','" + gender + "','" + ssn + "','" + expiry_date + "','" +
                               status + "')}")

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