from library.database import Library_Update_Virtual_Table
from log.write import sys_log

def Update_Virtual_Table(conn):
    Library_Update_Virtual_Table(conn, 'Text')
    Library_Update_Virtual_Table(conn, 'Image')
    Library_Update_Virtual_Table(conn, 'Video')

    conn.commit()

    sys_log("Update Virtual Table", "search_index")
