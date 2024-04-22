from library.connector import connect_to_mysql
from log.write import sys_log

def create_users_database():
    conn = connect_to_mysql('users_account')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255),
            username VARCHAR(255),
            password VARCHAR(255),
            authentication INT DEFAULT -1,
            confirm INT DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

    sys_log("Created", "users_account")
