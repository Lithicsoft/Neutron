from library.database import Library_Remove_Data

def remove_data(conn, type, site_id):
    cursor = conn.cursor()

    Library_Remove_Data(cursor, type, site_id)

    conn.commit()

    cursor.close()