def get_user_reliability(cursor, username, password):
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()

    if row:
        stored_password = row[0]
        if password == stored_password:
            cursor.execute('SELECT reliability FROM users WHERE username = ?', (username,))
            reliability_row = cursor.fetchone()
            if reliability_row:
                reliability_value = reliability_row[0]
                return reliability_value
            else:
                return None
        else:
            return None
    else:
        return None
