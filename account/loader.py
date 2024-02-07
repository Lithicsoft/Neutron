import sqlite3

def account_database_loader():
    conn = sqlite3.connect('./database/users-account.db')
    return conn
