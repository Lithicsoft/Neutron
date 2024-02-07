import sqlite3
from datetime import datetime

def Initializer_Database():
    conn = sqlite3.connect('./database/search-index.db')
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
    conn.close()

    return conn
