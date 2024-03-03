from library.connector import connect_to_mysql
from log.write import sys_log

def database_loader(num):
    if num == 0:
        conn = connect_to_mysql('search_index0')
        sys_log("Loaded", "search_index0")
        return conn
    elif num == 1:
        conn = connect_to_mysql('search_index1')
        sys_log("Loaded", "search_index1")
        return conn
    elif num == 2:
        conn = connect_to_mysql('search_index2')
        sys_log("Loaded", "search_index2")
        return conn

def censorship_database_loader(num):
    if num == 0:
        conn = connect_to_mysql('censorship0')
        sys_log("Loaded", "censorship0")
        return conn
    if num == 1:
        conn = connect_to_mysql('censorship1')
        sys_log("Loaded", "censorship1")
        return conn
    if num == 2:
        conn = connect_to_mysql('censorship2')
        sys_log("Loaded", "censorship2")
        return conn
