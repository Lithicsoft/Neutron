def get_user_id(cursor, username):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))

    rows = cursor.fetchall()

    for row in rows:
        userid = row[0]

    return userid 