import sqlite3

def create_users_database():
    conn = sqlite3.connect('./database/users-account.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        email TEXT,
                        username TEXT,
                        password TEXT,
                        reliability INTGER DEFAULT 0
                    )''')
    conn.commit()
    conn.close()