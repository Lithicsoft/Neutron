import sqlite3
from log.write import sys_log

def database_loader():
    conn = sqlite3.connect('./database/search-index.db')
    sys_log("Loaded", "search-index.db")
    return conn

def censorship_database_loader():
    conn = sqlite3.connect('./database/censorship.db')
    sys_log("Loaded", "censorship.db")
    return conn
