def Library_Create_Virtual_Table(conn):
    conn.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS information_fts
                 USING FTS5(site_id, link, title, text, description, keywords, shorttext, added)''')
    
def Library_Update_Virtual_Table(conn):
    conn.execute('DELETE FROM information_fts')
    conn.execute('''INSERT INTO information_fts(site_id, link, title, text, description, keywords, shorttext, added)
                SELECT site_id, link, title, text, description, keywords, shorttext, added FROM information''')
    
def Library_Initializer_Database(cursor):
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

def Library_Get_Data_Count(cursor, link):
    cursor.execute('''SELECT COUNT(*) FROM information WHERE link = ?''', (link,))
    return cursor.fetchone()[0]

def Library_Edit_Data(cursor, link, title, text, description, keywords, shorttext, added, site_id):
    cursor.execute('''UPDATE information 
                              SET link=?, title=?, text=?, description=?, keywords=?, shorttext=?, added=?
                              WHERE site_id=?''', 
                           (link, title, text, description, keywords, shorttext, added, site_id))
    
def Library_Get_Max_ID(cursor):
    cursor.execute("SELECT MAX(site_id) FROM information")
    return cursor.fetchone()[0]

def Library_Insert_Data(cursor, site_id, link, title, text, description, keywords, shorttext, added):
    cursor.execute('''INSERT INTO information 
                              (site_id, link, title, text, description, keywords, shorttext, added) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (site_id, link, title, text, description, keywords, shorttext, added))
    
def Library_Remove_Data(cursor, site_id):
    cursor.execute("DELETE FROM information WHERE site_id = ?", (site_id,))
    cursor.execute("UPDATE information SET site_id = site_id - 1 WHERE site_id > ?", (site_id,))

def Library_Exact_Search(cursor, safe_keyword):
    cursor.execute('''SELECT * FROM information
                        WHERE title LIKE ? OR text LIKE ? OR description LIKE ? OR keywords LIKE ? OR shorttext LIKE ?''', 
                        ('%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%'))
    return cursor.fetchall()

def Library_Full_Text_Search(cursor, safe_keyword):
    cursor.execute('''SELECT * FROM information_fts
                        WHERE information_fts MATCH ?''', (safe_keyword,))
    return cursor.fetchall()