import sqlite3
from log.write import sys_log

def database_loader(num):
    if num == 0:
        conn = sqlite3.connect('./database/search-index0.db', check_same_thread=False)
        sys_log("Loaded", "search-index0.db")
        return conn
    elif num == 1:
        conn = sqlite3.connect('./database/search-index1.db', check_same_thread=False)
        sys_log("Loaded", "search-index1.db")
        return conn
    elif num == 2:
        conn = sqlite3.connect('./database/search-index2.db', check_same_thread=False)
        sys_log("Loaded", "search-index2.db")
        return conn

def censorship_database_loader(num):
    if num == 0:
        conn = sqlite3.connect('./database/censorship0.db', check_same_thread=False)
        sys_log("Loaded", "censorship0.db")
        return conn
    if num == 1:
        conn = sqlite3.connect('./database/censorship1.db', check_same_thread=False)
        sys_log("Loaded", "censorship1.db")
        return conn
    if num == 2:
        conn = sqlite3.connect('./database/censorship2.db', check_same_thread=False)
        sys_log("Loaded", "censorship2.db")
        return conn
