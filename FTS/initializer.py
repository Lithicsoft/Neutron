from library.connector import connect_to_mysql
from library.database import Library_Create_Virtual_Table

from log.write import sys_log

def Initializer_Virtual_Table():
    conn = connect_to_mysql('search_index')

    Library_Create_Virtual_Table(conn, 'Text')
    Library_Create_Virtual_Table(conn, 'Image')
    Library_Create_Virtual_Table(conn, 'Video')
    
    conn.close()

    sys_log("Initializer Virtual Table", "search_index")
