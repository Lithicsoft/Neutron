def Library_Create_Virtual_Table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}_fts
                 (link TEXT, title TEXT, text TEXT, description TEXT, keywords TEXT, shorttext TEXT,
                 FULLTEXT(link, title, text, description, keywords, shorttext)) ENGINE=InnoDB''')
    cursor.close()
    
def Library_Update_Virtual_Table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table_name}_fts')
    cursor.execute(f'''INSERT INTO {table_name}_fts(link, title, text, description, keywords, shorttext)
                SELECT link, title, text, description, keywords, shorttext FROM {table_name}''')
    cursor.close()

def Library_Check_Index_Exists(cursor, table_name, index_name):
    cursor.execute(f'''SELECT COUNT(1) IndexIsThere 
                    FROM INFORMATION_SCHEMA.STATISTICS
                    WHERE table_schema=DATABASE() AND table_name='{table_name}' AND index_name='{index_name}';''')

    return cursor.fetchone()[0] == 0

def Library_Initializer_Database(cursor, table_name):
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                    (site_id INT, 
                    link TEXT, 
                    title TEXT, 
                    text TEXT, 
                    description TEXT, 
                    keywords TEXT, 
                    shorttext TEXT, 
                    added TIMESTAMP) ENGINE=InnoDB''')

    if Library_Check_Index_Exists(cursor, table_name, 'idx_title'):
        cursor.execute(f'''CREATE FULLTEXT INDEX idx_title ON {table_name} (title)''')
    if Library_Check_Index_Exists(cursor, table_name, 'idx_text'):
        cursor.execute(f'''CREATE FULLTEXT INDEX idx_text ON {table_name} (text)''')
    if Library_Check_Index_Exists(cursor, table_name, 'idx_description'):
        cursor.execute(f'''CREATE FULLTEXT INDEX idx_description ON {table_name} (description)''')
    if Library_Check_Index_Exists(cursor, table_name, 'idx_keywords'):
        cursor.execute(f'''CREATE FULLTEXT INDEX idx_keywords ON {table_name} (keywords)''')
    if Library_Check_Index_Exists(cursor, table_name, 'idx_shorttext'):
        cursor.execute(f'''CREATE FULLTEXT INDEX idx_shorttext ON {table_name} (shorttext)''')

def Library_Get_Data_Count(cursor, table_name, link):
    cursor.execute(f'''SELECT COUNT(*) FROM {table_name} WHERE link = %s''', (link,))
    return cursor.fetchone()[0]

def Library_Edit_Data(cursor, table_name, link, title, text, description, keywords, shorttext, added, site_id):
    cursor.execute(f'''UPDATE {table_name} 
                              SET link=%s, title=%s, text=%s, description=%s, keywords=%s, shorttext=%s, added=%s
                              WHERE site_id=%s''', 
                           (link, title, text, description, keywords, shorttext, added, site_id))
    
def Library_Get_Max_ID(cursor, table_name):
    cursor.execute(f"SELECT MAX(site_id) FROM {table_name}")
    return cursor.fetchone()[0]

def Library_Insert_Data(cursor, table_name, site_id, link, title, text, description, keywords, shorttext, added):
    cursor.execute(f'''INSERT INTO {table_name} 
                              (site_id, link, title, text, description, keywords, shorttext, added) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                           (site_id, link, title, text, description, keywords, shorttext, added))
    
def Library_Remove_Data(cursor, table_name, site_id):
    cursor.execute(f"DELETE FROM {table_name} WHERE site_id = %s", (site_id,))
    cursor.execute(f"UPDATE {table_name} SET site_id = site_id - 1 WHERE site_id > %s", (site_id,))

def Library_Exact_Search(cursor, table_name, safe_keyword):
    cursor.execute(f'''SELECT * FROM {table_name}
                        WHERE title LIKE %s OR text LIKE %s OR description LIKE %s OR keywords LIKE %s OR shorttext LIKE %s''', 
                        ('%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%'))
    return cursor.fetchall()

def Library_Full_Text_Search(cursor, table_name, safe_keyword):
    cursor.execute(f'''SELECT * FROM {table_name}_fts
                        WHERE MATCH(link, title, text, description, keywords, shorttext) AGAINST (%s IN NATURAL LANGUAGE MODE)''', (safe_keyword,))
    return cursor.fetchall()
