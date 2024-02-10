def get_username(cursor, user_id):
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))

    rows = cursor.fetchall()

    for row in rows:
        username = row[0]

    return username 
