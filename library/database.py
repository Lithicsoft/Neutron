def Library_Create_Virtual_Table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS information_fts
                 (link TEXT, title TEXT, text TEXT, description TEXT, keywords TEXT, shorttext TEXT,
                 FULLTEXT(link, title, text, description, keywords, shorttext)) ENGINE=InnoDB''')
    cursor.close()
    
def Library_Update_Virtual_Table(conn):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM information_fts')
    cursor.execute('''INSERT INTO information_fts(link, title, text, description, keywords, shorttext)
                SELECT link, title, text, description, keywords, shorttext FROM information''')
    cursor.close()
    
def Library_Initializer_Database(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS information
                    (site_id INT, 
                    link TEXT, 
                    title TEXT, 
                    text TEXT, 
                    description TEXT, 
                    keywords TEXT, 
                    shorttext TEXT, 
                    added TIMESTAMP) ENGINE=InnoDB''')

    cursor.execute('''CREATE FULLTEXT INDEX idx_title ON information (title)''')
    cursor.execute('''CREATE FULLTEXT INDEX idx_text ON information (text)''')
    cursor.execute('''CREATE FULLTEXT INDEX idx_description ON information (description)''')
    cursor.execute('''CREATE FULLTEXT INDEX idx_keywords ON information (keywords)''')
    cursor.execute('''CREATE FULLTEXT INDEX idx_shorttext ON information (shorttext)''')

def Library_Get_Data_Count(cursor, link):
    cursor.execute('''SELECT COUNT(*) FROM information WHERE link = %s''', (link,))
    return cursor.fetchone()[0]

def Library_Edit_Data(cursor, link, title, text, description, keywords, shorttext, added, site_id):
    cursor.execute('''UPDATE information 
                              SET link=%s, title=%s, text=%s, description=%s, keywords=%s, shorttext=%s, added=%s
                              WHERE site_id=%s''', 
                           (link, title, text, description, keywords, shorttext, added, site_id))
    
def Library_Get_Max_ID(cursor):
    cursor.execute("SELECT MAX(site_id) FROM information")
    return cursor.fetchone()[0]

def Library_Insert_Data(cursor, site_id, link, title, text, description, keywords, shorttext, added):
    cursor.execute('''INSERT INTO information 
                              (site_id, link, title, text, description, keywords, shorttext, added) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                           (site_id, link, title, text, description, keywords, shorttext, added))
    
def Library_Remove_Data(cursor, site_id):
    cursor.execute("DELETE FROM information WHERE site_id = %s", (site_id,))
    cursor.execute("UPDATE information SET site_id = site_id - 1 WHERE site_id > %s", (site_id,))

def Library_Exact_Search(cursor, safe_keyword):
    cursor.execute('''SELECT * FROM information
                        WHERE title LIKE %s OR text LIKE %s OR description LIKE %s OR keywords LIKE %s OR shorttext LIKE %s''', 
                        ('%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%'))
    return cursor.fetchall()

def Library_Full_Text_Search(cursor, safe_keyword):
    cursor.execute('''SELECT * FROM information_fts
                        WHERE MATCH(site_id, link, title, text, description, keywords, shorttext, added) AGAINST (%s IN NATURAL LANGUAGE MODE)''', (safe_keyword,))
    return cursor.fetchall()
