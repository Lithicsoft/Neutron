import sqlite3
from library.database import Library_Create_Virtual_Table

from log.write import sys_log

def Initializer_Virtual_Table():
    conn = sqlite3.connect('./database/search-index0.db')

    Library_Create_Virtual_Table(conn)
    
    conn.close()

    sys_log("Initializer Virtual Table", "search-index0.db")

    conn = sqlite3.connect('./database/search-index1.db')

    Library_Create_Virtual_Table(conn)
    
    conn.close()

    sys_log("Initializer Virtual Table", "search-index1.db")

    conn = sqlite3.connect('./database/search-index2.db')

    Library_Create_Virtual_Table(conn)
    
    conn.close()

    sys_log("Initializer Virtual Table", "search-index2.db")
