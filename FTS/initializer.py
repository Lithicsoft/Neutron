import sqlite3

from log.write import sys_log

from ..dbmanager import create_virtual_table

def Initializer_Virtual_Table():
    conn = sqlite3.connect('./database/search-index0.db')

    create_virtual_table(conn)
    
    conn.close()

    sys_log("Initializer Virtual Table", "search-index0.db")

    conn = sqlite3.connect('./database/search-index1.db')

    create_virtual_table(conn)
    
    conn.close()

    sys_log("Initializer Virtual Table", "search-index1.db")

    conn = sqlite3.connect('./database/search-index2.db')

    create_virtual_table(conn)
    
    conn.close()

    sys_log("Initializer Virtual Table", "search-index2.db")
