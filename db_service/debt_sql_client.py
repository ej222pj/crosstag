import pypyodbc
from db_service import sql_client_cfg as cfg
from datetime import datetime, timedelta


class DebtSqlClient():
    def __init__(self, username, password):
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + username + ';'
        self.dbPassword = 'pwd=' + password

    def get_connection_string(self):
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def get_debt(self, id=0):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetDebt('" + id + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return value

        except pypyodbc.DatabaseError as error:
            print(error.value)


    def add_dept(self, amount, product='', create_date=datetime.now(), uid=0):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call AddDebt('" + amount + "','" +  product + "','" +  create_date + "','" + uid + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)


    def remove_debt(self, id):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call DeleteDebt('" + id + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)