from library.connector import connect_to_mysql
from library.database import Library_Create_Virtual_Table

from log.write import sys_log

def Initializer_Virtual_Table():
    conn = connect_to_mysql('search_index0')

    Library_Create_Virtual_Table(conn)
    
    conn.close()

    sys_log("Initializer Virtual Table", "search_index0")

    conn = connect_to_mysql('search_index1')

    Library_Create_Virtual_Table(conn)
    
    conn.close()

    sys_log("Initializer Virtual Table", "search_index1")

    conn = connect_to_mysql('search_index2')

    Library_Create_Virtual_Table(conn)
    
    conn.close()

    sys_log("Initializer Virtual Table", "search_index2")
