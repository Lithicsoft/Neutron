import sqlite3
from log.write import sys_log

def account_database_loader():
    conn = sqlite3.connect('./database/users-account.db', check_same_thread=False)
    sys_log("Loaded", "users-account.db")
    return conn
