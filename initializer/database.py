import sqlite3

def Initializer_Database():
    conn = sqlite3.connect('./database/search-index.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS information
                    (name TEXT, address TEXT, text TEXT)''')

    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_name ON information (name)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_address ON information (address)''')

    conn.commit()
    conn.close()

    return conn