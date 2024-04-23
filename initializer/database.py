from library.connector import connect_to_mysql
from library.database import Library_Initializer_Database
from log.write import sys_log

from account.database import create_users_database

def Initializer_Database():
    conn = connect_to_mysql('Neutron')
    cursor = conn.cursor()

    Library_Initializer_Database(cursor)

    conn.commit()

    conn.close()

    create_users_database()

    sys_log("Initializer Database", "Neutron")
    sys_log("Create Users Account", "Users account")
