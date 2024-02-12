from datetime import datetime
import os
import shutil
import sqlite3
import subprocess
from FTS.initializer import Initializer_Virtual_Table
from FTS.update import Update_Virtual_Table
from account.username import get_username
from atmt import ATMT_STRT
from initializer.database import Initializer_Database
from initializer.loader import database_loader
from log.write import sys_log
from account.loader import account_database_loader
from account.reliability import get_user_reliability

print('Welcome to Neutron Administrator Panel')

def compare_databases(num):
    if num == 0:
        try:
            conn1 = sqlite3.connect("./database/search-index0.db")
            conn2 = sqlite3.connect("./database/censorship0.db")

            cur1 = conn1.cursor()
            cur2 = conn2.cursor()

            table_name = "information"

            cur1.execute(f"SELECT * FROM {table_name}")
            cur2.execute(f"SELECT * FROM {table_name}")

            data1 = cur1.fetchall()
            data2 = cur2.fetchall()

            set1 = set(data1)
            set2 = set(data2)

            different_list = list(set2 - set1)

            result = {
                "Censorship:": different_list,
                "Search Index:": list(set1-set2)
            }

            print(result)

            conn1.close()
            conn2.close()

            if different_list:
                return False
            else:
                return True
        except Exception as e:
            print("Error comparing databases:", str(e))
            return False
    elif num == 1:
        try:
            conn1 = sqlite3.connect("./database/search-index1.db")
            conn2 = sqlite3.connect("./database/censorship1.db")

            cur1 = conn1.cursor()
            cur2 = conn2.cursor()

            table_name = "information"

            cur1.execute(f"SELECT * FROM {table_name}")
            cur2.execute(f"SELECT * FROM {table_name}")

            data1 = cur1.fetchall()
            data2 = cur2.fetchall()

            set1 = set(data1)
            set2 = set(data2)

            different_list = list(set2 - set1)

            result = {
                "Censorship:": different_list,
                "Search Index:": list(set1-set2)
            }

            print(result)

            conn1.close()
            conn2.close()

            if different_list:
                return False
            else:
                return True
        except Exception as e:
            print("Error comparing databases:", str(e))
            return False
    elif num == 2:
        try:
            conn1 = sqlite3.connect("./database/search-index2.db")
            conn2 = sqlite3.connect("./database/censorship2.db")

            cur1 = conn1.cursor()
            cur2 = conn2.cursor()

            table_name = "information"

            cur1.execute(f"SELECT * FROM {table_name}")
            cur2.execute(f"SELECT * FROM {table_name}")

            data1 = cur1.fetchall()
            data2 = cur2.fetchall()

            set1 = set(data1)
            set2 = set(data2)

            different_list = list(set2 - set1)

            result = {
                "Censorship:": different_list,
                "Search Index:": list(set1-set2)
            }

            print(result)

            conn1.close()
            conn2.close()

            if different_list:
                return False
            else:
                return True
        except Exception as e:
            print("Error comparing databases:", str(e))
            return False

def synchronization_databases():
    try:
        if not compare_databases(0) and not compare_databases(1) and not compare_databases(2):
            print("Databases cannot be synchronized when there are differences between them.")
            return
        else:
            os.remove("./database/censorship0.db")
            shutil.copy("./database/search-index0.db", "./database/censorship0.db")
            print("Synchronization successful.")

            os.remove("./database/censorship1.db")
            shutil.copy("./database/search-index1.db", "./database/censorship1.db")
            print("Synchronization successful.")

            os.remove("./database/censorship2.db")
            shutil.copy("./database/search-index2.db", "./database/censorship2.db")
            print("Synchronization successful.")
    except Exception as e:
        print("Error synchronizing databases:", str(e))

account_conn = account_database_loader()
account_cursor = account_conn.cursor()

def list_users_database():
    account_cursor.execute("SELECT * FROM users")

    rows = account_cursor.fetchall()

    for row in rows:
        print("ID:", row[0])
        print("Email:", row[1])
        print("Username:", row[2])
        print("Password:", row[3])
        print("Reliability:", row[4])
        print("--------------------")

def get_reliability_from_id(user_id):
    account_cursor.execute("SELECT reliability FROM users WHERE id = ?", (user_id,))

    rows = account_cursor.fetchall()

    for row in rows:
        reliability = row[0]

    return reliability

def change_reliability_by_user_id(user_id, new_reliability):
    account_cursor.execute("UPDATE users SET reliability = ? WHERE id = ?", (new_reliability, user_id))
    account_conn.commit()

    sys_log("Changed User Reliability", "Username: " + get_username(account_cursor, user_id) + " Reliability: " + str(new_reliability))

username = input('Username: ')
password = input('Password: ')

reliability = get_user_reliability(account_cursor, username, password)

if reliability is None:
    print("Account does not exist.")
    exit()
elif reliability >= 4:
    print('Logged in successfully.')
else:
    print('You do not have sufficient rights to access the panel.')
    exit()

while(True):
    command = input('>>> ')
    
    if command == "exit":
        exit()
    elif command == "start":
        yn = input('Do you want to start the server including: Search, Account [y/n]: ')
        if (yn != 'n'):
                Initializer_Database()
                Initializer_Virtual_Table()

                vt_conn = database_loader(0)
                Update_Virtual_Table(vt_conn)
                vt_conn.close()
                vt_conn = database_loader(1)
                Update_Virtual_Table(vt_conn)
                vt_conn.close()
                vt_conn = database_loader(2)
                Update_Virtual_Table(vt_conn)
                vt_conn.close()
                
                subprocess.call("start server1", shell=True)
                subprocess.call("start server2", shell=True)
                print('The server has been started successfully.')
                sys_log('Start Server', str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    elif command == "atmt":
        keyword = input('Keyword: ')
        ATMT_STRT(keyword)
    elif command == "check":
        compare_databases_num = input('Text(0), Image(1), Video(3): ')
        compare_databases(compare_databases_num)
    elif command == "sync":
        synchronization_databases()
        print("Successful data synchronization.")
    elif command == "sync-fts":
        vt_conn = database_loader(0)
        Update_Virtual_Table(vt_conn)
        vt_conn.close()
        vt_conn = database_loader(1)
        Update_Virtual_Table(vt_conn)
        vt_conn.close()
        vt_conn = database_loader(2)
        Update_Virtual_Table(vt_conn)
        vt_conn.close()
        print("Successful data synchronization.")
    elif command == "log":
        with open('log.txt', 'r') as file:
            for line in file:
                print(line.strip())
    elif command == "users-list":
        list_users_database()
    elif command == "users-rel":
        user_id = input('User ID: ')
        print("Current reliability: " + str(get_reliability_from_id(user_id)))
        new_reliability = input('Change reliability to: ')
        change_reliability_by_user_id(user_id, new_reliability)
        print('Changed reliability successfully.')
        