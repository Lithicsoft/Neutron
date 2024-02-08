import sqlite3

def Update_Virtual_Table():
    conn = sqlite3.connect('./database/search-index.db')

    conn.execute('DELETE FROM information_fts')
    conn.execute('''INSERT INTO information_fts(site_id, link, title, text, description, keywords, shorttext, added)
                SELECT site_id, link, title, text, description, keywords, shorttext, added FROM information''')

    conn.commit()

    conn.close()
