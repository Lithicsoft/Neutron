from library.database import Library_Get_Data_Count, Library_Get_ID

def content_exists(conn, table_name, link):
    cursor = conn.cursor()
    count = Library_Get_Data_Count(cursor, table_name, link)
    return count > 0

def Get_ID(conn, table_name, link):
    cursor = conn.cursor()

    if content_exists(conn, table_name, link):
        return Library_Get_ID(cursor, table_name, link)
    else:
        return None
