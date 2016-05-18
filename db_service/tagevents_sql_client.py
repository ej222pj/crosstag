import pypyodbc
from db_service import sql_client_cfg as cfg
from db_models import sql_detailed_tagevent as tagevent
from db_models import sql_statistic_tagevent as statistic_tagevent
from datetime import datetime, timedelta
from flask import session


class TageventsSqlClient:
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

    def get_detailed_tagevents(self, id=0, number_of_tagevents=20):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetDetailedTagevents('" + str(id) + "','" + str(number_of_tagevents) + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()

            return_array = []
            for detailed_tagevent in value:
                return_array.append(tagevent.SQLDetailedTagevent(detailed_tagevent[0], detailed_tagevent[1],
                                                                 detailed_tagevent[2][:-8], detailed_tagevent[3]))

            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def get_statistic_tagevents(self, id=0):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetStatisticTagevents('" + str(id) + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()

            return_array = []
            for statistics_tagevent in value:
                return_array.append(statistic_tagevent.SQLStatisticTagevent(statistics_tagevent[0],
                                                                            statistics_tagevent[1][:-8],
                                                                            statistics_tagevent[2],
                                                                            statistics_tagevent[3]))
            return return_array

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def add_tagevents(self, detailed_tagevent):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()
            cursor.execute("{call AddDetailedTagevents('" + detailed_tagevent['tag_id'] + "','" +
                           detailed_tagevent['timestamp'] + "0" + "','" + detailed_tagevent['timestamp'][11:-13]
                           + "','" + detailed_tagevent['uid'] + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)
