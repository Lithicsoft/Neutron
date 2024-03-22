from library.database import Library_Get_ID, content_exists

def Get_ID(conn, type, link):
    cursor = conn.cursor()

    if content_exists(conn, type, link):
        return Library_Get_ID(cursor, type, link)
    else:
        return None
