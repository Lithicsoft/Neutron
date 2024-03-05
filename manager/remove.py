from library.database import Library_Remove_Data

def remove_data(conn, table_name, site_id):
    cursor = conn.cursor()

    Library_Remove_Data(cursor,table_name, site_id)

    conn.commit()

    cursor.close()