import pypyodbc
from db_service import sql_client_cfg as cfg
from datetime import datetime, timedelta
from db_models import sql_debt
from flask import session

class DebtSqlClient():
    def __init__(self,):
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + session['username'] + ';'
        self.dbPassword = 'pwd=' + cfg.TENANT_PASSWORD + session['username']

    def get_connection_string(self):
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def get_debt(self, user_id=0):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetDebt('" + str(user_id) + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return_array = []
            if user_id is not 0:
                for debt in value:
                    return_array.append(sql_debt.SQLDebt(debt[1], debt[4], debt[2], debt[3], debt[0]))
            else:
                for debt in value:
                    return_array.append({'amount': debt[0],
                                         'product': debt[1],
                                         'id': debt[2],
                                         'uid': debt[3],
                                         'create_date': debt[4][:-17],
                                         'firstname': debt[5],
                                         'lastname': debt[6]})
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def add_dept(self, debt):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call AddDebt('" + debt['amount'] + "','" + debt['product'] + "','" +
                           debt['create_date'] + "','" + debt['uid'] + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def remove_debt(self, debt_id):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call DeleteDebt('" + str(debt_id) + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)