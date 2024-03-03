import os
import pymysql

def clone_database(db_name, new_db_name):
    conn = pymysql.connect(host='localhost', user=os.environ.get('SQLUSERNAME'), password=os.environ.get('SQLPASSWORD'))
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name}")

    cursor.execute(f"USE {db_name}")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for table in tables:
        table = table[0]
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {new_db_name}.{table} LIKE {db_name}.{table}")
        cursor.execute(f"INSERT INTO {new_db_name}.{table} SELECT * FROM {db_name}.{table}")

    cursor.close()
    conn.close()
