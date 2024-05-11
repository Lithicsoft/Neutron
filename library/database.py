def Library_Check_Index_Exists(cursor, index_name):
    cursor.execute('''SELECT COUNT(1) IndexIsThere 
                    FROM INFORMATION_SCHEMA.STATISTICS
                    WHERE table_schema=DATABASE() AND table_name='information' AND index_name=%s;''', (index_name,))

    return cursor.fetchone()[0] == 0

def Library_Initializer_Database(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS information
                    (site_id INT, 
                    link TEXT, 
                    title TEXT, 
                    text LONGTEXT, 
                    description TEXT, 
                    keywords TEXT, 
                    shorttext TEXT, 
                    added TIMESTAMP,
                    type TEXT) ENGINE=InnoDB''')

    if Library_Check_Index_Exists(cursor, 'idx_fulltext'):
        cursor.execute('''CREATE FULLTEXT INDEX idx_fulltext ON information (link, title, text, description, keywords, shorttext, type)''')

def Library_Get_Data_Count(cursor, type, link):
    cursor.execute('''SELECT COUNT(*) FROM information WHERE link = %s AND type = %s''', (link, type,))
    return cursor.fetchone()[0]

def content_exists(conn, type, link):
    cursor = conn.cursor()
    count = Library_Get_Data_Count(cursor, type, link)
    return count > 0

def Library_Edit_Data(cursor, type, link, title, text, description, keywords, shorttext, added, site_id):
    cursor.execute('''UPDATE information 
                              SET link=%s, title=%s, text=%s, description=%s, keywords=%s, shorttext=%s, added=%s, type=%s
                              WHERE site_id=%s''', 
                           (link, title, text, description, keywords, shorttext, added, type, site_id,))
    
def Library_Get_Max_ID(cursor):
    cursor.execute("SELECT MAX(site_id) FROM information")
    return cursor.fetchone()[0]

def Library_Insert_Data(cursor, type, site_id, link, title, text, description, keywords, shorttext, added):
    cursor.execute('''INSERT INTO information 
                              (site_id, link, title, text, description, keywords, shorttext, added, type) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                           (site_id, link, title, text, description, keywords, shorttext, added, type,))
    
def Library_Remove_Data(cursor, type, site_id):
    cursor.execute("DELETE FROM information WHERE site_id = %s AND type = %s", (site_id, type,))
    cursor.execute("UPDATE information SET site_id = site_id - 1 WHERE site_id > %s", (site_id,))

def Library_Get_ID(cursor, type, link):
    cursor.execute("SELECT site_id FROM information WHERE link = %s AND type = %s", (link, type,))
    return cursor.fetchone()[0]

def Library_Full_Text_Domain_Search(cursor, type, safe_keyword, domain, page):
    offset = (page - 1) * 15
    cursor.execute('''SELECT * FROM information
                        WHERE MATCH(link, title, text, description, keywords, shorttext, type) AGAINST (%s IN NATURAL LANGUAGE MODE) AND type = %s AND link = %s
                        LIMIT 15 OFFSET %s''', (safe_keyword, type, domain, offset))
    return cursor.fetchall()

def Library_Full_Text_Search(cursor, type, safe_keyword, page):
    offset = (page - 1) * 15
    cursor.execute('''SELECT * FROM information
                        WHERE MATCH(link, title, text, description, keywords, shorttext, type) AGAINST (%s IN NATURAL LANGUAGE MODE) AND type = %s
                        LIMIT 15 OFFSET %s''', (safe_keyword, type, offset))
    return cursor.fetchall()
