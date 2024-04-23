from library.connector import connect_to_mysql
from log.write import sys_log

def database_loader():
    conn = connect_to_mysql('Neutron')
    sys_log("Loaded", "Neutron")
    return conn