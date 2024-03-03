import os
import pymysql

def delete_database(db_name):
    conn = pymysql.connect(host='localhost', user=os.environ.get('SQLUSERNAME'), password=os.environ.get('SQLPASSWORD'))
    cursor = conn.cursor()

    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")

    cursor.close()
    conn.close()
