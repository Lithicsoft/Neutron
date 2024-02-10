import sqlite3

from log.write import sys_log

def Update_Virtual_Table(conn):
    conn.execute('DELETE FROM information_fts')
    conn.execute('''INSERT INTO information_fts(site_id, link, title, text, description, keywords, shorttext, added)
                SELECT site_id, link, title, text, description, keywords, shorttext, added FROM information''')

    conn.commit()

    sys_log("Update Virtual Table", "search-index.db")
