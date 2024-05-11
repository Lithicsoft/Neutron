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

def verification(conn, cursor, user_id, confirmation_code):
    cursor.execute("SELECT confirm FROM users WHERE id = %s", (user_id,))
    confirm_value = cursor.fetchall()[0][0]
    if int(confirmation_code) == confirm_value:
        cursor.execute("UPDATE users SET confirm = 0 WHERE id = %s", (user_id,))
        cursor.execute("UPDATE users SET authentication = 0 WHERE id = %s", (user_id,))
        conn.commit()
        return 'Your account has been successfully created.'
    else:
        return 'The verification code is incorrect, please check again.'
    
def check_existing_email(cursor, email):
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    return cursor.fetchone() is not None

def check_existing_username(cursor, username):
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    return cursor.fetchone() is not None

def add_user(conn, cursor, email, username, password, confirm):
    password = hashlib.md5(hashlib.sha256(password.encode('utf-8')).hexdigest().encode()).hexdigest()
    cursor.execute('''INSERT INTO users (email, username, password, confirm) VALUES (%s, %s, %s, %s)''', (email, username, password, confirm))
    conn.commit()

def update_password(conn, cursor, user_id, new_password):
    new_password = hashlib.md5(hashlib.sha256(new_password.encode('utf-8')).hexdigest().encode()).hexdigest()
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
    conn.commit()