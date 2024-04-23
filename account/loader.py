from library.connector import connect_to_mysql
from log.write import sys_log

def account_database_loader():
    conn = connect_to_mysql('Neutron')
    sys_log("Loaded", "Users account")
    return conn
