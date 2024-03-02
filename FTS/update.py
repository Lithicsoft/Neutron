from library.database import Library_Update_Virtual_Table
from log.write import sys_log

def Update_Virtual_Table(conn):
    Library_Update_Virtual_Table(conn)

    conn.commit()

    sys_log("Update Virtual Table", "search-index012.db")
