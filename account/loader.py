from library.connector import connect_to_mysql
from log.write import sys_log

def account_database_loader():
    conn = connect_to_mysql('users_account')
    sys_log("Loaded", "users_account")
    return conn
