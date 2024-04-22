import getpass
import threading
import dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join('./')))
from account.database import create_users_database
from library.connector import connect_to_mysql
from library.deleter import delete_database
from account.username import get_username
from initializer.database import Initializer_Database
from log.write import sys_log
from account.loader import account_database_loader
from account.authentication import get_user_authentication

print('Welcome to Neutron Administrator Panel')

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
        print("Authentication:", row[4])
        print("--------------------")
        user_amount + 1
    
    print("User Amount: ", user_amount)

def get_authentication_from_id(user_id):
    account_cursor.execute("SELECT authentication FROM users WHERE id = %s", (user_id,))

    rows = account_cursor.fetchall()

    for row in rows:
        authentication = row[0]

    return authentication

def change_authentication_by_user_id(user_id, new_authentication):
    account_cursor.execute("UPDATE users SET authentication = %s WHERE id = %s", (new_authentication, user_id))
    account_conn.commit()

    sys_log("Changed User authentication", "Username: " + get_username(account_cursor, user_id) + " authentication: " + str(new_authentication))

username = input('Username: ')
password = getpass.getpass('Password: ')

authentication = get_user_authentication(account_cursor, username, password)

if authentication is None:
    print("Account does not exist.")
    exit()
elif authentication >= 1:
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
            config: Add the necessary API KEY environment variables to the servers, setup for MySQL and prepair the database.
            check: Lists the data that needs to be censored.
            sync: Synchronize the censored database and the parent database (requirement: no data that needs to be censored).
            log: Prints the server log.
            users-list: Lists the list of users.
            users-rel: Changes user authentication through their user id.
        ''')
    elif command == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
    elif command == "config":
        SG_API = input('SENDGRID API KEY: ')
        GSB_API = input('GOOGLE SAFE BROWSING API KEY: ')
        GOOGLE_API = input('GOOGLE GEMINI API KEY: ')
        SQLUSERNAME = input('MySQL USERNAME: ')
        SQLPASSWORD = getpass.getpass('MySQL PASSWORD: ')
        SQLHOSTNAME = input('MySQL HOSTNAME: ')
        SQLPORT = input('MySQL PORT: ')

        config_path = "./config"
        dotenv.set_key(config_path, "SG_API_KEY", SG_API)
        dotenv.set_key(config_path, "GSB_API_KEY", GSB_API)
        dotenv.set_key(config_path, "GOOGLE_API_KEY", GOOGLE_API)
        dotenv.set_key(config_path, "MYSQLUSERNAME", SQLUSERNAME)
        dotenv.set_key(config_path, "MYSQLPASSWORD", SQLPASSWORD)
        dotenv.set_key(config_path, "MYSQLHOSTNAME", SQLHOSTNAME)
        dotenv.set_key(config_path, "MYSQLPORT", SQLPORT)
        dotenv.load_dotenv()
        
        Initializer_Database()
    elif command == "log":
        with open('log.txt', 'r', encoding='utf-8') as file:
            for line in file:
                print(line.strip())
    elif command == "users-list":
        list_users_database()
    elif command == "users-auth":
        user_id = input('User ID: ')
        print("Current authentication: " + str(get_authentication_from_id(user_id)))
        new_authentication = input('Change authentication to: ')
        change_authentication_by_user_id(user_id, new_authentication)
        print('Changed authentication successfully.')
        