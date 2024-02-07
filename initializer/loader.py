import sqlite3

def database_loader():
    conn = sqlite3.connect('./database/search-index.db')
    return conn

def censorship_database_loader():
    conn = sqlite3.connect('./database/censorship.db')
    return conn
