import hashlib

def get_user_authentication(cursor, username, password, hash=True):
    if hash:
        password = hashlib.md5(hashlib.sha256(password.encode('utf-8')).hexdigest().encode()).hexdigest()

    cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
    row = cursor.fetchone()

    if row:
        stored_password = row[0]
        if password == stored_password:
            cursor.execute('SELECT authentication FROM users WHERE username = %s', (username,))
            authentication_row = cursor.fetchone()
            if authentication_row:
                authentication_value = authentication_row[0]
                return authentication_value
            else:
                return None
        else:
            return None
    else:
        return None
