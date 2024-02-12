import sqlite3
from log.write import sys_log

from account.database import create_users_database

def Initializer_Censorship_Database():
    source_conn1 = sqlite3.connect('./database/search-index0.db')

    destination_conn1 = sqlite3.connect('./database/censorship0.db')

    source_conn1.backup(destination_conn1)

    source_conn1.close()
    destination_conn1.close()

    source_conn2 = sqlite3.connect('./database/search-index1.db')

    destination_conn2 = sqlite3.connect('./database/censorship1.db')

    source_conn2.backup(destination_conn2)

    source_conn2.close()
    destination_conn2.close()

    source_conn3 = sqlite3.connect('./database/search-index2.db')

    destination_conn3 = sqlite3.connect('./database/censorship2.db')

    source_conn3.backup(destination_conn3)

    source_conn3.close()
    destination_conn3.close()

def Initializer_Database():
    conn = sqlite3.connect('./database/search-index0.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS information
                    (site_id INTEGER, 
                    link TEXT, 
                    title TEXT, 
                    text TEXT, 
                    description TEXT, 
                    keywords TEXT, 
                    shorttext TEXT, 
                    added TIMESTAMP)''')

    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_title ON information (title)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_text ON information (text)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_description ON information (description)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_keywords ON information (keywords)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_shorttext ON information (shorttext)''')

    conn.commit()

    conn1 = sqlite3.connect('./database/search-index1.db')
    conn2 = sqlite3.connect('./database/search-index2.db')

    conn.backup(conn1)
    conn.backup(conn2)

    conn.close()
    conn1.close()
    conn2.close()

    Initializer_Censorship_Database()
    create_users_database()

    sys_log("Initializer Database", "search-index0.db")
    sys_log("Initializer Database", "search-index1.db")
    sys_log("Initializer Database", "search-index2.db")
    sys_log("Initializer Censorship Database", "censorship.db")
    sys_log("Create Users Account Database", "users-account.db")
