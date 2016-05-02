import pypyodbc
from db_service import sql_client_cfg as cfg


class SqlClient():

    def __init__(self, username=cfg.USERNAME, password=cfg.PASSWORD):
        self.dbDriver = 'Driver={FreeTDS};'
        self.dbServer = 'Server=' + cfg.SERVER + ';'
        self.dbDatabase = 'Database=' + cfg.DATABASE + ';'
        self.dbUsername = 'uid=' + username + ';'
        self.dbPassword = 'pwd=' + password

    def get_connection_string(self):
        return self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword

    def do_registration(self, tenant):
            connection_string = self.get_connection_string()
            try:
                my_connection = pypyodbc.connect(connection_string)
                cursor = my_connection.cursor()

                cursor.execute('exec CreateUserLogin(?,?,?,?,?,?,?,?,?,?)',
                (tenant[0], tenant[1], tenant[2], tenant[3],tenant[4], tenant[5], tenant[6], tenant[7], tenant[8], tenant[9]))

            except pypyodbc.DatabaseError as error:
                print(error.value)
                print('FATALITY')

    def try_connection(self):
        print('try connection')
        try:
            connString = self.dbDriver + self.dbServer + self.dbDatabase + self.dbUsername + self.dbPassword
            myConnection = pypyodbc.connect(connString)
            print('Connection works!!!')
        except pypyodbc.DatabaseError as error:
            print(error.value)
            print('FATALITY, bummer')