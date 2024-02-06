import sqlite3

def Initializer_Database():
    conn = sqlite3.connect('./database/search-index.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS information
                    (name TEXT, address TEXT, text TEXT)''')

    conn.commit()
    conn.close()
