import pypyodbc
from db_service import sql_client_cfg as cfg
from datetime import datetime, timedelta
from db_models import sql_debt
from flask import session


class DebtSqlClient:
    """
    Class to Connect to the DB and /Create/Read/Delete a Debt

    __init__ - Creates connection string variables
    get_connection_string - Creates connection string from the variables
    get_debt - Get all Debts or the Debt of a specific User.
    add_dept - Add a new Debt for a User
    remove_debt - Remove 1 specific Debt
    """
    def __init__(self):
        """
        Init function that creates the variables for the connection string
        """
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + session['username'] + ';'
        self.dbPassword = 'pwd=' + cfg.TENANT_PASSWORD + session['username']

    def get_connection_string(self):
        """
        Creates a connection string for the DB from the variables created in init.

        :return: Connection String
        """
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def get_debt(self, user_id=0):
        """
        Takes an user_id as argument and get Debts depending on the user_id.
        If user_id is 0, get all. If user_id is > 0, get specific.

        :param user_id: Id of an user.
        :type user_id: integer
        :return: Representation of the class Debt
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetDebt('" + str(user_id) + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return_array = []
            # If the debts are for a specific user. Create a custom array.
            if user_id is not 0:
                for debt in value:
                    return_array.append(sql_debt.SQLDebt(debt[1], debt[4], debt[2], debt[3][:-11], debt[0]))
            else:
                for debt in value:
                    return_array.append({'amount': debt[0],
                                         'product': debt[1],
                                         'id': debt[2],
                                         'uid': debt[3],
                                         'create_date': debt[4][:-11],
                                         'firstname': debt[5],
                                         'lastname': debt[6]})
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def add_dept(self, debt):
        """
        Takes Debt as argument and then creates a new Debt.

        :param debt: A debt representation
        :type debt: debt class
        :return: true
        """
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
        """
        Takes debt_id as argument and then removes a Debt.

        :param debt_id: Id of a debt
        :type debt_id: integer
        :return: true
        """
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