from library.database import Library_Remove_Data


def remove_data(conn, site_id):
    cursor = conn.cursor()

    Library_Remove_Data(cursor, site_id)

    conn.commit()

    cursor.close()