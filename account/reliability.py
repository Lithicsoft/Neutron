import hashlib

def get_user_reliability(cursor, username, password):
    password = hashlib.md5(hashlib.sha256(password.encode('utf-8')).hexdigest().encode()).hexdigest()

    cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
    row = cursor.fetchone()

    if row:
        stored_password = row[0]
        if password == stored_password:
            cursor.execute('SELECT reliability FROM users WHERE username = %s', (username,))
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
