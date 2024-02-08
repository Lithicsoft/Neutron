import sqlite3

def Initializer_Virtual_Table():
    conn = sqlite3.connect('./database/search-index.db')

    conn.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS information_fts
                 USING FTS5(site_id, link, title, text, description, keywords, shorttext, added)''')
    
    conn.close()
