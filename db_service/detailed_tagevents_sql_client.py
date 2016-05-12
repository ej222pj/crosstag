import pypyodbc
from db_service import sql_client_cfg as cfg
from datetime import datetime, timedelta
from flask import session


class DetailedTageventsSqlClient:
    def __init__(self):
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + session['username'] + ';'
        self.dbPassword = 'pwd=' + cfg.TENANT_PASSWORD + session['username']

    def get_connection_string(self):
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def get_detailed_tagevents(self, id=0, number_of_tagevents=20):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call GetDetailedTagevents('" + id + "','" + number_of_tagevents + "')}")
            value = cursor.fetchall()

            cursor.close()
            my_connection.close()
            return value

        except pypyodbc.DatabaseError as error:
            print(error.value)

    def add_detailed_tagevents(self, detailed_tagevent):
        connection_string = self.get_connection_string()
        try:
            my_connection = pypyodbc.connect(connection_string)
            cursor = my_connection.cursor()

            cursor.execute("{call AddDetailedTagevents('" + detailed_tagevent['tag_id'] + "','" +
                           detailed_tagevent['timestamp'] + "','" + detailed_tagevent['uid'] + "')}")
            cursor.commit()
            cursor.close()
            my_connection.close()
            return True

        except pypyodbc.DatabaseError as error:
            print(error.value)
