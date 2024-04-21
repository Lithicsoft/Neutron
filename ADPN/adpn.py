import getpass
import threading
import dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join('./')))
from account.database import create_users_database
from library.connector import connect_to_mysql
from library.deleter import delete_database
from library.cloner import clone_database
from datetime import datetime
import run
from account.username import get_username
from initializer.database import Initializer_Database
from log.write import sys_log
from account.loader import account_database_loader
from account.reliability import get_user_reliability

print('Welcome to Neutron Administrator Panel')

def compare_databases():
    try:
        conn1 = connect_to_mysql("search_index")
        conn2 = connect_to_mysql("censorship")

        cur1 = conn1.cursor()
        cur2 = conn2.cursor()

        cur1.execute(f"SELECT * FROM information")
        cur2.execute(f"SELECT * FROM information")

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
        if not compare_databases():
            print("Databases cannot be synchronized when there are differences between them.")
            return
        else:
            delete_database("censorship")
            clone_database("search-index", "censorship")

            print("Synchronization successful.")
    except Exception as e:
        print("Error synchronizing databases:", str(e))


create_users_database()
account_conn = account_database_loader()
account_cursor = account_conn.cursor()

def list_users_database():
    account_cursor.execute("SELECT * FROM users")

    rows = account_cursor.fetchall()

    user_amount = 0

    for row in rows:
        print("ID:", row[0])
        print("Email:", row[1])
        print("Username:", row[2])
        print("Password:", row[3])
        print("Reliability:", row[4])
        print("--------------------")
        user_amount + 1
    
    print("User Amount: ", user_amount)

def get_reliability_from_id(user_id):
    account_cursor.execute("SELECT reliability FROM users WHERE id = %s", (user_id,))

    rows = account_cursor.fetchall()

    for row in rows:
        reliability = row[0]

    return reliability

def change_reliability_by_user_id(user_id, new_reliability):
    account_cursor.execute("UPDATE users SET reliability = %s WHERE id = %s", (new_reliability, user_id))
    account_conn.commit()

    sys_log("Changed User Reliability", "Username: " + get_username(account_cursor, user_id) + " Reliability: " + str(new_reliability))

username = input('Username: ')
password = getpass.getpass('Password: ')

reliability = get_user_reliability(account_cursor, username, password)

if reliability is None:
    print("Account does not exist.")
    exit()
elif reliability >= 4:
    print('Logged in successfully.')
else:
    print('You do not have sufficient rights to access the panel.')
    exit()

dotenv.load_dotenv()

while(True):
    command = input('>>> ')
    
    if command == "exit":
        exit()
    elif command == "help":
        print('''
            exit: Exit ADPN.
            help: This command.
            clear: Clear the terminal.
            start: Start the servers needed for MonoSearch.
            api-config: Add the necessary API KEY environment variables to the servers.
            check: Lists the data that needs to be censored.
            sync: Synchronize the censored database and the parent database (requirement: no data that needs to be censored).
            log: Prints the server log.
            users-list: Lists the list of users.
            users-rel: Changes user reliability through their user id.
        ''')
    elif command == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
    elif command == "start":
        if os.getenv('SG_API_KEY') is None or os.getenv('GSB_API_KEY') is None or os.getenv('GOOGLE_API_KEY') is None or os.getenv('SQLUSERNAME') is None or os.getenv('SQLPASSWORD') is None:
            print('The required API KEY to start the servers was not found, please use the "api-config" command to set the required environment API KEY variables.')
        else:
            yn = input('Do you want to start the server including: Search, Account [y/n]: ')
            if (yn != 'n'):
                    Initializer_Database()
                    thread = threading.Thread(target=run.start_server)
                    thread.start()
                    print('The server has been started successfully.')
                    sys_log('Start Server', str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    elif command == "api-config":
        SG_API = input('SENDGRID API KEY: ')
        GSB_API = input('GOOGLE SAFE BROWSING API KEY: ')
        GOOGLE_API = input('GOOGLE GEMINI API KEY: ')
        config_path = "./config"
        dotenv.set_key(config_path, "SG_API_KEY", SG_API)
        dotenv.set_key(config_path, "GSB_API_KEY", GSB_API)
        dotenv.set_key(config_path, "GOOGLE_API_KEY", GOOGLE_API)
        dotenv.load_dotenv()
    elif command == "check":
        compare_databases()
    elif command == "sync":
        synchronization_databases()
        print("Successful data synchronization.")
    elif command == "log":
        with open('log.txt', 'r', encoding='utf-8') as file:
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
        