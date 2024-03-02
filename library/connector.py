import mysql.connector
from log.write import sys_log

def connect_to_mysql(database_name):
    config = {
        'user': 'username',
        'password': 'password',
        'host': 'localhost',
        'database': database_name,
        'raise_on_warnings': True
    }

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            sys_log('Database Connection', 'Successful')
            return connection
    except mysql.connector.Error as err:
        sys_log("Database Connection", f"Error: {err}")
        return None
