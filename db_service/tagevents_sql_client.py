import pypyodbc
from db_service import sql_client_cfg as cfg
from db_models import sql_detailed_tagevent as tagevent
from db_models import sql_statistic_tagevent as statistic_tagevent
from datetime import datetime, timedelta
from flask import session


class TageventsSqlClient:
    """
    Class to Connect to the DB and Get Detailed/Statistic tagevents and Add tagevents

    __init__ - Creates connection string variables
    get_connection_string - Creates connection string from the variables
    get_detailed_tagevents - Get Detailed tagevents
    get_statistic_tagevents - Get Statistic tagevents
    add_tagevents - Add statistic and detailed tagevent
    """
    def __init__(self, username=''):
        """
        Init function that creates the variables for the connection string.
        If session exists, set username to the session variable Username.
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

    def get_detailed_tagevents(self, user_id=0, number_of_tagevents=20):
        """
        Takes user_id and number_of_tagevents as parameters
        Get limited number of tagevents detailed tagevent or get limited number of user specific tagevents.

        :param user_id: User id
        :param number_of_tagevents: How many tagevents.
        :type user_id: integer
        :type number_of_tagevents: integer
        :return: Array of Detailed tagevents
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetDetailedTagevents('" + str(user_id) + "','" + str(number_of_tagevents) + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()

            return_array = []
            # [:-8] is to remove unnecessary decimals
            for detailed_tagevent in value:
                return_array.append(tagevent.SQLDetailedTagevent(detailed_tagevent[0], detailed_tagevent[1],
                                                                 detailed_tagevent[2][:-8], detailed_tagevent[3]))

            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def get_statistic_tagevents(self, user_id=0):
        """
        Takes user_id as parameter
        Get all tagevents used for the statistic page

        :param user_id: User id
        :type user_id: integer
        :return: Array of Statistic tagevents
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetStatisticTagevents('" + str(user_id) + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()

            return_array = []
            # [:-8] is to remove unnecessary decimals
            for statistics_tagevent in value:
                return_array.append(statistic_tagevent.SQLStatisticTagevent(statistics_tagevent[0],
                                                                            statistics_tagevent[1][:-8],
                                                                            statistics_tagevent[2],
                                                                            statistics_tagevent[3]))
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def add_tagevents(self, detailed_tagevent):
        """
        Takes a representation of a detailed_tagevent as parameter
        Add Detailed and Statistic tagevents.

        :param detailed_tagevent: A representation of a Detailed Tagevent
        :type detailed_tagevent: Detailed Tagevent Class
        :return: True
        """
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()
            # [11:-13] Gets hour of the day.
            cursor.execute("{call AddDetailedTagevents('" + detailed_tagevent['tag_id'] + "','" +
                           detailed_tagevent['timestamp'] + "0" + "','" + detailed_tagevent['timestamp'][11:-13]
                           + "','" + detailed_tagevent['uid'] + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)
