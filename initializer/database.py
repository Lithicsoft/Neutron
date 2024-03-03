from library.cloner import clone_database
from library.connector import connect_to_mysql
from library.database import Library_Initializer_Database
from log.write import sys_log

from account.database import create_users_database

def Initializer_Censorship_Database():
    clone_database('search_index0', 'censorship0')
    clone_database('search_index1', 'censorship1')
    clone_database('search_index2', 'censorship2')


def Initializer_Database():
    conn = connect_to_mysql('search_index0')
    cursor = conn.cursor()

    Library_Initializer_Database(cursor)

    conn.commit()

    clone_database('search_index0', 'search_index1')
    clone_database('search_index0', 'search_index2')

    conn.close()

    Initializer_Censorship_Database()
    create_users_database()

    sys_log("Initializer Database", "search_index 0")
    sys_log("Initializer Database", "search_index 1")
    sys_log("Initializer Database", "search_index 2")
    sys_log("Initializer Censorship Database", "censorship")
    sys_log("Create Users Account Database", "users_account")
