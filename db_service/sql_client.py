import pypyodbc
from db_service import sql_client_cfg as cfg


class SqlClient():

    def __init__(self, username=cfg.USERNAME, password=cfg.PASSWORD):
        self.dbDriver = 'Driver={SQL Server};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + username + ';'
        self.dbPassword = 'pwd=' + password

    def print_this_shit(self):
        print(self.dbDriver, self.dbServer, self.dbDatabase, self.dbUsername, self.dbPassword)

    def try_connection(self):
        print('try connection')
        try:
            connString = self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword
            print(connString)
            print('hej')
            myConnection = pypyodbc.connect(connString)
            print('Connection works!!!')
        except pypyodbc.DatabaseError as error:
            print(error.value)
            print('FATALITY, bummer')