import os
import mysql.connector
from log.write import sys_log

def connect_to_mysql(database_name):
    config = {
        'user': os.environ.get('SQLUSERNAME'),
        'password': os.environ.get('SQLPASSWORD'),
        'host': 'localhost',
        'raise_on_warnings': True
    }

    try:
        connection = mysql.connector.connect(user=config['user'], password=config['password'], host=config['host'])
        cursor = connection.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {database_name}')
        connection.database = database_name
        sys_log('Database Connection', 'Successful')
        return connection
    except mysql.connector.Error as err:
        sys_log("Database Connection", f"Error: {err}")
        return None
