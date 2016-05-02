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

                cursor.execute("{call CreateUserLogin('"+ tenant['username'] +"','"+ tenant['password']+"','"+ tenant['active_fortnox']+"','"+
                tenant['gym_name']+"','"+ tenant['address']+"','"+ tenant['phone']+"','"+ tenant['zip_code']+"','"+
                tenant['city']+"','"+ tenant['email']+"','"+ tenant['pass']+"' )}")

                #cursor.execute('exec CreateUserLogin(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                #(tenant['username'], tenant['password'], tenant['active_fortnox'],
                 #tenant['gym_name'], tenant['address'], tenant['phone'], tenant['zip_code'],
                 #tenant['city'], tenant['email'], tenant['pass']))

                cursor.commit()
                cursor.close()
                my_connection.close()

                return True

            except pypyodbc.DatabaseError as error:
                print(error.value)
                print('FATALITY')
