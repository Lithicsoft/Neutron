import sqlite3

def remove_data(conn, site_id):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM information WHERE site_id = ?", (site_id,))
    cursor.execute("UPDATE information SET site_id = site_id - 1 WHERE site_id > ?", (site_id,))

    conn.commit()

    cursor.close()