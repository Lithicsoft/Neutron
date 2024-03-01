from ..dbmanager import delete_information,update_information

def remove_data(conn, site_id):
    cursor = conn.cursor()

    delete_information(cursor, site_id)
    update_information(cursor, site_id)

    conn.commit()

    cursor.close()
