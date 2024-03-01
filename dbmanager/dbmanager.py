import sqlite3

def select_from_information_longer(cursor, safe_keyword):
    cursor.execute('''SELECT * FROM information
                        WHERE title LIKE ? OR text LIKE ? OR description LIKE ? OR keywords LIKE ? OR shorttext LIKE ?''', 
                        ('%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%', '%' + safe_keyword + '%'))

    return cursor.fetchall()

def select_from_information_shorter(cursor, safe_keyword):
    cursor.execute('''SELECT * FROM information_fts
                WHERE information_fts MATCH ?''', (safe_keyword,))

    return cursor.fetchall()

def delete_information(cursor, site_id):
    cursor.execute("DELETE FROM information WHERE site_id = ?", (site_id,))

def update_information(cursor, site_id):
    cursor.execute("UPDATE information SET site_id = site_id - 1 WHERE site_id > ?", (site_id,))

def select_count_from_information(cursor, link):
    cursor.execute('''SELECT COUNT(*) FROM information WHERE link = ?''', (link,))
    return cursor.fetchone()[0]

def update_information_longer(cursor, link, title, text, description, keywords, shorttext, added, site_id):
    cursor.execute('''UPDATE information 
                              SET link=?, title=?, text=?, description=?, keywords=?, shorttext=?, added=?
                              WHERE site_id=?''', 
                           (link, title, text, description, keywords, shorttext, added, site_id))

def select_max(cursor):
    cursor.execute("SELECT MAX(site_id) FROM information")
    return cursor.fetchone()[0]

def insert_information(cursor, site_id, link, title, text, description, keywords, shorttext, added):
    cursor.execute('''INSERT INTO information 
                    (site_id, link, title, text, description, keywords, shorttext, added) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                (site_id, link, title, text, description, keywords, shorttext, added))

def create_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS information
                    (site_id INTEGER, 
                    link TEXT, 
                    title TEXT, 
                    text TEXT, 
                    description TEXT, 
                    keywords TEXT, 
                    shorttext TEXT, 
                    added TIMESTAMP)''')
    
def create_index(cursor, table_name):
    cursor.execute(f'''CREATE INDEX IF NOT EXISTS idx_{table_name} ON information ({table_name})''')

def create_virtual_table(conn):
    conn.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS information_fts
                 USING FTS5(site_id, link, title, text, description, keywords, shorttext, added)''')
